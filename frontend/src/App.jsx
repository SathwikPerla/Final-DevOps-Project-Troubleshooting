import React, { useState, useEffect } from "react";

const API_BASE = "";

export default function App() {
  const [incidents, setIncidents] = useState([]);
  const [stats, setStats] = useState({
    total: 0,
    open: 0,
    investigating: 0,
    mitigated: 0,
    resolved: 0,
    criticalCount: 0,
    uptimePercent: 99.95,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [backendStatus, setBackendStatus] = useState("CHECKING");

  // Filters
  const [statusFilter, setStatusFilter] = useState("ALL");
  const [severityFilter, setSeverityFilter] = useState("ALL");
  const [searchTerm, setSearchTerm] = useState("");

  // Modal State
  const [modalOpen, setModalOpen] = useState(false);
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    severity: "HIGH",
    status: "OPEN",
    service: "api-gateway",
    assignee: "Sathwik Perla",
  });

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Check health
      try {
        const hRes = await fetch(`${API_BASE}/health`);
        if (hRes.ok) setBackendStatus("CONNECTED");
        else setBackendStatus("DEGRADED");
      } catch (e) {
        setBackendStatus("OFFLINE");
      }

      // Fetch incidents
      const incRes = await fetch(`${API_BASE}/api/incidents`);
      if (!incRes.ok) throw new Error(`HTTP ${incRes.status}: Failed to fetch incidents`);
      const incData = await incRes.json();
      setIncidents(incData);

      // Fetch stats
      const statsRes = await fetch(`${API_BASE}/api/incidents/stats`);
      if (statsRes.ok) {
        const statsData = await statsRes.json();
        setStats(statsData);
      }
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch(`${API_BASE}/api/incidents`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      if (!res.ok) throw new Error("Failed to create incident");
      setModalOpen(false);
      setFormData({
        title: "",
        description: "",
        severity: "HIGH",
        status: "OPEN",
        service: "api-gateway",
        assignee: "Sathwik Perla",
      });
      await loadData();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleStatusChange = async (id, newStatus) => {
    try {
      const res = await fetch(`${API_BASE}/api/incidents/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status: newStatus }),
      });
      if (!res.ok) throw new Error("Failed to update status");
      await loadData();
    } catch (err) {
      alert(err.message);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm(`Delete incident #${id}?`)) return;
    try {
      const res = await fetch(`${API_BASE}/api/incidents/${id}`, {
        method: "DELETE",
      });
      if (!res.ok) throw new Error("Failed to delete incident");
      await loadData();
    } catch (err) {
      alert(err.message);
    }
  };

  // Filtered incidents
  const filtered = incidents.filter((inc) => {
    if (statusFilter !== "ALL" && inc.status !== statusFilter) return false;
    if (severityFilter !== "ALL" && inc.severity !== severityFilter) return false;
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      const matchTitle = inc.title.toLowerCase().includes(term);
      const matchService = inc.service.toLowerCase().includes(term);
      const matchAssignee = inc.assignee.toLowerCase().includes(term);
      if (!matchTitle && !matchService && !matchAssignee) return false;
    }
    return true;
  });

  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-logo">OP</div>
          <div>
            <div className="brand-name">OpsPulse</div>
            <div className="brand-badge">DEVOPS SRE v1.0</div>
          </div>
        </div>

        <nav className="nav-section">
          <div className="nav-item active">
            <span>⚡ Incidents & Alerts</span>
          </div>
          <div className="nav-item" onClick={() => window.open("/docs", "_blank")}>
            <span>📖 API Swagger Docs</span>
          </div>
          <div className="nav-item" onClick={() => window.open("/metrics", "_blank")}>
            <span>📊 Prometheus Metrics</span>
          </div>
          <div className="nav-item" onClick={() => window.open("/health", "_blank")}>
            <span>💚 Health Endpoint</span>
          </div>
        </nav>

        <div className="sidebar-footer">
          <div className="cluster-pill">
            <span className={`status-dot ${backendStatus === "CONNECTED" ? "" : "dot-offline"}`}></span>
            <span>API: {backendStatus}</span>
          </div>
          <div style={{ fontSize: "11px", color: "var(--text-muted)" }}>
            Cluster: AWS EKS ap-south-1
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <div className="main-wrapper">
        <header className="topbar">
          <div className="topbar-left">
            <h1 className="page-title">Service Reliability Dashboard</h1>
            <span className="environment-tag">PRODUCTION CLUSTER</span>
          </div>
          <div className="topbar-right">
            <button className="btn btn-secondary" onClick={loadData}>
              ↻ Refresh
            </button>
            <button className="btn btn-primary" onClick={() => setModalOpen(true)}>
              + Report Incident
            </button>
          </div>
        </header>

        <main className="content-body">
          {error && (
            <div style={{ background: "rgba(239, 68, 68, 0.2)", border: "1px solid #ef4444", padding: "12px 16px", borderRadius: "10px", color: "#fca5a5" }}>
              ⚠️ Backend Error: {error}. Check if backend container/service is running.
            </div>
          )}

          {/* Metric Cards */}
          <section className="metrics-grid">
            <div className="metric-card">
              <div className="metric-header">
                <span>TOTAL INCIDENTS</span>
                <span>📋</span>
              </div>
              <div className="metric-value">{stats.total}</div>
              <div className="metric-sub">Across all microservices</div>
            </div>

            <div className="metric-card">
              <div className="metric-header">
                <span>ACTIVE / OPEN</span>
                <span style={{ color: "#ef4444" }}>●</span>
              </div>
              <div className="metric-value" style={{ color: "#f87171" }}>
                {stats.open + stats.investigating}
              </div>
              <div className="metric-sub">{stats.investigating} currently investigating</div>
            </div>

            <div className="metric-card">
              <div className="metric-header">
                <span>CRITICAL SEVERITY</span>
                <span style={{ color: "#ef4444" }}>🚨</span>
              </div>
              <div className="metric-value" style={{ color: stats.criticalCount > 0 ? "#ef4444" : "#10b981" }}>
                {stats.criticalCount}
              </div>
              <div className="metric-sub">P0 / P1 production alerts</div>
            </div>

            <div className="metric-card">
              <div className="metric-header">
                <span>RESOLVED / MITIGATED</span>
                <span style={{ color: "#10b981" }}>✓</span>
              </div>
              <div className="metric-value" style={{ color: "#34d399" }}>
                {stats.resolved + stats.mitigated}
              </div>
              <div className="metric-sub">
                {stats.total > 0 ? Math.round(((stats.resolved + stats.mitigated) / stats.total) * 100) : 100}% resolution rate
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-header">
                <span>SYSTEM UPTIME SLA</span>
                <span style={{ color: "#6366f1" }}>📈</span>
              </div>
              <div className="metric-value" style={{ color: "#a5b4fc" }}>
                {stats.uptimePercent}%
              </div>
              <div className="metric-sub">Rolling 30-day availability</div>
            </div>
          </section>

          {/* Filter Bar */}
          <section className="filter-bar">
            <div className="search-box">
              <span>🔍</span>
              <input
                type="text"
                placeholder="Search by title, service, assignee..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
            </div>

            <div className="filters-group">
              <select className="select-custom" value={statusFilter} onChange={(e) => setStatusFilter(e.target.value)}>
                <option value="ALL">All Statuses</option>
                <option value="OPEN">Open</option>
                <option value="INVESTIGATING">Investigating</option>
                <option value="MITIGATED">Mitigated</option>
                <option value="RESOLVED">Resolved</option>
              </select>

              <select className="select-custom" value={severityFilter} onChange={(e) => setSeverityFilter(e.target.value)}>
                <option value="ALL">All Severities</option>
                <option value="CRITICAL">Critical</option>
                <option value="HIGH">High</option>
                <option value="MEDIUM">Medium</option>
                <option value="LOW">Low</option>
              </select>
            </div>
          </section>

          {/* Table Container */}
          <section className="table-container">
            <div className="table-header-title">
              <h3>Incident Log ({filtered.length})</h3>
              <span style={{ fontSize: "12px", color: "var(--text-muted)" }}>
                Auto-refreshed every 30s
              </span>
            </div>

            {loading && incidents.length === 0 ? (
              <div className="empty-state">
                <p>Loading incidents from backend...</p>
              </div>
            ) : filtered.length === 0 ? (
              <div className="empty-state">
                <div className="empty-state-icon">🛡️</div>
                <p>No incidents match the active filters or database is clean.</p>
                <button className="btn btn-secondary btn-sm" onClick={() => setModalOpen(true)}>
                  Create First Incident
                </button>
              </div>
            ) : (
              <table className="incident-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Incident & Service</th>
                    <th>Severity</th>
                    <th>Status</th>
                    <th>Assignee</th>
                    <th>Created</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {filtered.map((inc) => (
                    <tr key={inc.id}>
                      <td className="incident-id">#{inc.id}</td>
                      <td>
                        <div className="incident-title-cell">
                          <span className="incident-title-text">{inc.title}</span>
                          <span className="service-tag">⚙️ {inc.service}</span>
                          {inc.description && (
                            <span style={{ fontSize: "12px", color: "var(--text-muted)", marginTop: "2px" }}>
                              {inc.description.length > 70 ? `${inc.description.slice(0, 70)}...` : inc.description}
                            </span>
                          )}
                        </div>
                      </td>
                      <td>
                        <span className={`badge badge-${inc.severity.toLowerCase()}`}>
                          <span className="badge-dot"></span>
                          {inc.severity}
                        </span>
                      </td>
                      <td>
                        <select
                          className={`select-custom status-badge status-${inc.status.toLowerCase()}`}
                          style={{ border: "none", cursor: "pointer", fontWeight: "600" }}
                          value={inc.status}
                          onChange={(e) => handleStatusChange(inc.id, e.target.value)}
                        >
                          <option value="OPEN">OPEN</option>
                          <option value="INVESTIGATING">INVESTIGATING</option>
                          <option value="MITIGATED">MITIGATED</option>
                          <option value="RESOLVED">RESOLVED</option>
                        </select>
                      </td>
                      <td>
                        <div className="assignee-cell">
                          <div className="avatar">
                            {inc.assignee.split(" ").map((n) => n[0]).join("").slice(0, 2).toUpperCase()}
                          </div>
                          <span>{inc.assignee}</span>
                        </div>
                      </td>
                      <td style={{ fontSize: "12px", color: "var(--text-muted)", fontFamily: "var(--font-mono)" }}>
                        {new Date(inc.created_at).toLocaleDateString([], { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })}
                      </td>
                      <td>
                        <div className="row-actions">
                          {inc.status !== "RESOLVED" && (
                            <button
                              className="btn btn-secondary btn-sm"
                              title="Resolve incident"
                              onClick={() => handleStatusChange(inc.id, "RESOLVED")}
                            >
                              ✓ Resolve
                            </button>
                          )}
                          <button
                            className="action-icon-btn danger"
                            title="Delete incident"
                            onClick={() => handleDelete(inc.id)}
                          >
                            🗑
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </section>
        </main>
      </div>

      {/* Create Modal */}
      {modalOpen && (
        <div className="modal-overlay" onClick={() => setModalOpen(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Report New Production Incident</h3>
              <button className="modal-close" onClick={() => setModalOpen(false)}>
                ✕
              </button>
            </div>

            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label>Incident Title *</label>
                <input
                  type="text"
                  required
                  placeholder="e.g., Elevated 502 Errors on Ingress Gateway"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                />
              </div>

              <div className="form-row" style={{ marginTop: "12px" }}>
                <div className="form-group">
                  <label>Affected Service</label>
                  <select
                    value={formData.service}
                    onChange={(e) => setFormData({ ...formData, service: e.target.value })}
                  >
                    <option value="api-gateway">api-gateway</option>
                    <option value="auth-service">auth-service</option>
                    <option value="payment-gateway">payment-gateway</option>
                    <option value="k8s-ingress">k8s-ingress</option>
                    <option value="postgres-cluster">postgres-cluster</option>
                    <option value="redis-cache">redis-cache</option>
                    <option value="notification-worker">notification-worker</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>Severity Level</label>
                  <select
                    value={formData.severity}
                    onChange={(e) => setFormData({ ...formData, severity: e.target.value })}
                  >
                    <option value="CRITICAL">CRITICAL (P0 - Service Down)</option>
                    <option value="HIGH">HIGH (P1 - Core Feature Degraded)</option>
                    <option value="MEDIUM">MEDIUM (P2 - Non-critical Bug)</option>
                    <option value="LOW">LOW (P3 - Minor Inconvenience)</option>
                  </select>
                </div>
              </div>

              <div className="form-row" style={{ marginTop: "12px" }}>
                <div className="form-group">
                  <label>Initial Status</label>
                  <select
                    value={formData.status}
                    onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  >
                    <option value="OPEN">OPEN</option>
                    <option value="INVESTIGATING">INVESTIGATING</option>
                    <option value="MITIGATED">MITIGATED</option>
                    <option value="RESOLVED">RESOLVED</option>
                  </select>
                </div>

                <div className="form-group">
                  <label>On-Call Assignee</label>
                  <input
                    type="text"
                    required
                    value={formData.assignee}
                    onChange={(e) => setFormData({ ...formData, assignee: e.target.value })}
                  />
                </div>
              </div>

              <div className="form-group" style={{ marginTop: "12px" }}>
                <label>Description & Diagnostic Details</label>
                <textarea
                  rows="3"
                  placeholder="Detail symptoms, error spikes, pod logs, or affected endpoints..."
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                ></textarea>
              </div>

              <div className="modal-footer">
                <button type="button" className="btn btn-secondary" onClick={() => setModalOpen(false)}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary">
                  Submit Incident
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
