def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "UP"}

def test_ready_endpoint(client):
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "READY"
    assert data["database"] == "CONNECTED"

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "SevZero" in data["service"]
    assert data["status"] == "OPERATIONAL"
    assert data["docs"] == "/docs"

def test_metrics_endpoint(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "http_requests" in response.text or "process_cpu_seconds" in response.text or "python_info" in response.text

def test_create_incident_success(client):
    payload = {
        "title": "High Latency in Auth Service",
        "description": "P99 latency spiked to 2.4s after deployment v2.1.0",
        "severity": "HIGH",
        "status": "OPEN",
        "service": "auth-service",
        "assignee": "Sathwik Perla"
    }
    response = client.post("/api/incidents", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == payload["title"]
    assert data["severity"] == "HIGH"
    assert data["status"] == "OPEN"
    assert data["service"] == "auth-service"
    assert data["assignee"] == "Sathwik Perla"

def test_create_incident_validation_error(client):
    # Invalid severity
    invalid_payload = {
        "title": "Database replication lag",
        "severity": "URGENT_CRITICAL", # Not in enum pattern
        "status": "OPEN"
    }
    response = client.post("/api/incidents", json=invalid_payload)
    assert response.status_code == 422

    # Missing title
    empty_title = {
        "title": "",
        "severity": "LOW"
    }
    response = client.post("/api/incidents", json=empty_title)
    assert response.status_code == 422

def test_list_incidents(client):
    response = client.get("/api/incidents")
    assert response.status_code == 200
    incidents = response.json()
    assert isinstance(incidents, list)
    assert len(incidents) >= 1

def test_get_incident_by_id(client):
    # Create incident first
    res = client.post("/api/incidents", json={
        "title": "Redis Connection Timeouts",
        "severity": "MEDIUM",
        "status": "INVESTIGATING",
        "service": "cache-cluster",
        "assignee": "DevOps Engineer"
    })
    incident_id = res.json()["id"]

    response = client.get(f"/api/incidents/{incident_id}")
    assert response.status_code == 200
    assert response.json()["id"] == incident_id
    assert response.json()["title"] == "Redis Connection Timeouts"

def test_get_nonexistent_incident_404(client):
    response = client.get("/api/incidents/99999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Incident not found"

def test_update_incident(client):
    # Create incident first
    res = client.post("/api/incidents", json={
        "title": "Kubelet Memory Pressure Node 03",
        "severity": "CRITICAL",
        "status": "OPEN",
        "service": "k8s-node-03",
        "assignee": "SRE On-Call"
    })
    incident_id = res.json()["id"]

    # Update incident to RESOLVED
    update_res = client.put(f"/api/incidents/{incident_id}", json={
        "status": "RESOLVED",
        "description": "Evicted pods and restarted containerd."
    })
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "RESOLVED"
    assert "Evicted pods" in update_res.json()["description"]

def test_delete_incident(client):
    # Create incident
    res = client.post("/api/incidents", json={
        "title": "Temporary Test Incident",
        "severity": "LOW",
        "status": "OPEN",
        "service": "test-runner",
        "assignee": "QA Bot"
    })
    incident_id = res.json()["id"]

    # Delete
    del_res = client.delete(f"/api/incidents/{incident_id}")
    assert del_res.status_code == 204

    # Verify deleted
    get_res = client.get(f"/api/incidents/{incident_id}")
    assert get_res.status_code == 404

def test_incident_stats(client):
    response = client.get("/api/incidents/stats")
    assert response.status_code == 200
    stats = response.json()
    assert "total" in stats
    assert "open" in stats
    assert "investigating" in stats
    assert "mitigated" in stats
    assert "resolved" in stats
    assert "criticalCount" in stats
    assert "uptimePercent" in stats
    assert stats["total"] >= 1
