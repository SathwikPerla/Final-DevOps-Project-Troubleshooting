from contextlib import asynccontextmanager
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .config import settings
from .db import Base, engine, get_db
from .models import Incident
from .schemas import IncidentCreate, IncidentOut, IncidentUpdate, StatsOut

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="Enterprise DevOps Incident & Reliability Management System API",
    lifespan=lifespan,
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expose Prometheus /metrics endpoint
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.get("/", tags=["System"])
def root():
    return {
        "service": settings.app_name,
        "version": "1.0.0",
        "status": "OPERATIONAL",
        "docs": "/docs",
        "health": "/health",
        "ready": "/ready",
        "metrics": "/metrics",
    }

@app.get("/health", tags=["System"])
def health():
    return {"status": "UP"}

@app.get("/ready", tags=["System"])
def ready(db: Session = Depends(get_db)):
    try:
        db.execute(select(func.count(Incident.id)))
        return {"status": "READY", "database": "CONNECTED"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(exc)}",
        )

@app.get("/api/incidents/stats", response_model=StatsOut, tags=["Incidents"])
def get_stats(db: Session = Depends(get_db)):
    rows = db.execute(select(Incident.status, func.count(Incident.id)).group_by(Incident.status)).all()
    counts = {s: count for s, count in rows}
    
    crit_count = db.scalar(select(func.count(Incident.id)).where(Incident.severity == "CRITICAL", Incident.status != "RESOLVED")) or 0
    total = sum(counts.values())
    resolved = counts.get("RESOLVED", 0)
    uptime = 99.95 if total == 0 else round(max(95.0, 100.0 - (crit_count * 0.4)), 2)

    return StatsOut(
        total=total,
        open=counts.get("OPEN", 0),
        investigating=counts.get("INVESTIGATING", 0),
        mitigated=counts.get("MITIGATED", 0),
        resolved=resolved,
        criticalCount=crit_count,
        uptimePercent=uptime,
    )

@app.get("/api/incidents", response_model=list[IncidentOut], tags=["Incidents"])
def list_incidents(
    status_filter: Optional[str] = Query(None, alias="status"),
    severity_filter: Optional[str] = Query(None, alias="severity"),
    service_filter: Optional[str] = Query(None, alias="service"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    query = select(Incident)
    if status_filter:
        query = query.where(Incident.status == status_filter)
    if severity_filter:
        query = query.where(Incident.severity == severity_filter)
    if service_filter:
        query = query.where(Incident.service.ilike(f"%{service_filter}%"))
    
    query = query.order_by(Incident.id.desc()).limit(limit).offset(offset)
    return list(db.scalars(query))

@app.get("/api/incidents/{incident_id}", response_model=IncidentOut, tags=["Incidents"])
def get_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    return incident

@app.post("/api/incidents", response_model=IncidentOut, status_code=status.HTTP_201_CREATED, tags=["Incidents"])
def create_incident(payload: IncidentCreate, db: Session = Depends(get_db)):
    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident

@app.put("/api/incidents/{incident_id}", response_model=IncidentOut, tags=["Incidents"])
def update_incident(incident_id: int, payload: IncidentUpdate, db: Session = Depends(get_db)):
    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    
    for key, value in payload.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(incident, key, value)
    
    db.commit()
    db.refresh(incident)
    return incident

@app.delete("/api/incidents/{incident_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Incidents"])
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.get(Incident, incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    
    db.delete(incident)
    db.commit()
    return None
