from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    severity: str = Field(default="MEDIUM", pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    status: str = Field(default="OPEN", pattern="^(OPEN|INVESTIGATING|MITIGATED|RESOLVED)$")
    service: str = Field(default="api-gateway", max_length=100)
    assignee: str = Field(default="DevOps On-Call", max_length=120)

class IncidentUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=2000)
    severity: Optional[str] = Field(default=None, pattern="^(LOW|MEDIUM|HIGH|CRITICAL)$")
    status: Optional[str] = Field(default=None, pattern="^(OPEN|INVESTIGATING|MITIGATED|RESOLVED)$")
    service: Optional[str] = Field(default=None, max_length=100)
    assignee: Optional[str] = Field(default=None, max_length=120)

class IncidentOut(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    status: str
    service: str
    assignee: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class StatsOut(BaseModel):
    total: int
    open: int
    investigating: int
    mitigated: int
    resolved: int
    criticalCount: int
    uptimePercent: float
