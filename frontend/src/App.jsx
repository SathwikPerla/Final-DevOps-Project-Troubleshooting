import React, { useState, useEffect } from "react";

const API_BASE = "";

// Handcrafted SVG Icons (Clean, modern, zero emojis)
function IconZap() {
  return (
    <svg className="nav-icon" viewBox="0 0 24 24">
      <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
    </svg>
  );
}

function IconBook() {
  return (
    <svg className="nav-icon" viewBox="0 0 24 24">
      <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
      <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
    </svg>
  );
}

function IconChart() {
  return (
    <svg className="nav-icon" viewBox="0 0 24 24">
      <line x1="18" y1="20" x2="18" y2="10" />
      <line x1="12" y1="20" x2="12" y2="4" />
      <line x1="6" y1="20" x2="6" y2="14" />
    </svg>
  );
}

function IconPulse() {
  return (
    <svg className="nav-icon" viewBox="0 0 24 24">
      <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
    </svg>
  );
}

function IconClipboard() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
      <rect x="8" y="2" width="8" height="4" rx="1" ry="1" />
    </svg>
  );
}

function IconAlert() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="12" cy="12" r="10" />
      <line x1="12" y1="8" x2="12" y2="12" />
      <line x1="12" y1="16" x2="12.01" y2="16" />
    </svg>
  );
}

function IconAlertTriangle() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" />
      <line x1="12" y1="9" x2="12" y2="13" />
      <line x1="12" y1="17" x2="12.01" y2="17" />
    </svg>
  );
}

function IconCheck() {
  return (
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  );
}

function IconTrending() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
      <polyline points="17 6 23 6 23 12" />
    </svg>
  );
}

function IconSearch() {
  return (
    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="var(--text-muted)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <circle cx="11" cy="11" r="8" />
      <line x1="21" y1="21" x2="16.65" y2="16.65" />
    </svg>
  );
}

function IconRefresh() {
  return (
    <svg className="btn-icon" viewBox="0 0 24 24">
      <path d="M21.5 2v6h-6M2.5 22v-6h6M2 11.5a10 10 0 0 1 18.8-4.3M22 12.5a10 10 0 0 1-18.8 4.2" />
    </svg>
  );
}

function IconTrash() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="3 6 5 6 21 6" />
      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
    </svg>
  );
}

function IconClose() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="6" x2="6" y2="18" />
      <line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  );
}

function IconShield() {
  return (
    <svg className="empty-state-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
  );
}

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
            <div className="brand-name">SevZero</div>
            <div className="brand-badge">SRE INCIDENTS v1.0</div>
          </div>
        </div>

        <nav className="nav-section">
          <div className="nav-item active">
            <IconZap />
            <span>Incidents & Alerts</span>
          </div>
          <div className="nav-item" onClick={() => window.open("/docs", "_blank")}>
            <IconBook />
            <span>API Documentation</span>
          </div>
          <div className="nav-item" onClick={() => window.open("/metrics", "_blank")}>
            <IconChart />
            <span>Prometheus Metrics</span>
          </div>
          <div className="nav-item" onClick={() => window.open("/health", "_blank")}>
            <IconPulse />
            <span>Health Endpoint</span>
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
              <IconRefresh />
              <span>Refresh</span>
            </button>
            <button className="btn btn-primary" onClick={() => setModalOpen(true)}>
              <span>+ Report Incident</span>
            </button>
          </div>
        </header>

        <main className="content-body">
          {error && (
            <div style={{ background: "rgba(200, 90, 84, 0.15)", border: "1px solid #c85a54", padding: "12px 16px", borderRadius: "9px", color: "#fca5a5" }}>
              Backend Error: {error}. Check if backend container/service is running.
            </div>
          )}

          {/* Metric Cards */}
          <section className="metrics-grid">
            <div className="metric-card">
              <div className="metric-header">
                <span>TOTAL INCIDENTS</span>
                <div className="metric-icon-wrap">
                  <IconClipboard />
                </div>
              </div>
              <div className="metric-value">{stats.total}</div>
              <div className="metric-sub">Across all microservices</div>
            </div>

            <div className="metric-card">
              <div className="metric-header">
                <span>ACTIVE / OPEN</span>
                <div className="metric-icon-wrap" style={{ color: "#cf7c38", background: "rgba(207, 124, 56, 0.12)" }}>
                  <IconAlert />
                </div>
              </div>
              <div className="metric-value" style={{ color: "#f5a770" }}>
                {stats.open + stats.investigating}
              </div>
              <div className="metric-sub">{stats.investigating} currently investigating</div>
            </div>

            <div className="metric-card">
              <div className="metric-header">
                <span>CRITICAL SEVERITY</span>
                <div className="metric-icon-wrap" style={{ color: "#c85a54", background: "rgba(200, 90, 84, 0.12)" }}>
                  <IconAlertTriangle />
                </div>
              </div>
              <div className="metric-value" style={{ color: stats.criticalCount > 0 ? "#fca5a5" : "#a7f3d0" }}>
                {stats.criticalCount}
              </div>
              <div className="metric-sub">P0 / P1 production alerts</div>
            </div>

            <div className="metric-card">
              <div className="metric-header">
                <span>RESOLVED / MITIGATED</span>
                <div className="metric-icon-wrap" style={{ color: "#5a8d67", background: "rgba(90, 141, 103, 0.12)" }}>
                  <IconCheck />
                </div>
              </div>
              <div className="metric-value" style={{ color: "#a7f3d0" }}>
                {stats.resolved + stats.mitigated}
              </div>
              <div className="metric-sub">
                {stats.total > 0 ? Math.round(((stats.resolved + stats.mitigated) / stats.total) * 100) : 100}% resolution rate
              </div>
            </div>

            <div className="metric-card">
              <div className="metric-header">
                <span>SYSTEM UPTIME SLA</span>
                <div className="metric-icon-wrap">
                  <IconTrending />
                </div>
              </div>
              <div className="metric-value" style={{ color: "var(--accent-biscuit)" }}>
                {stats.uptimePercent}%
              </div>
              <div className="metric-sub">Rolling 30-day availability</div>
            </div>
          </section>

          {/* Filter Bar */}
          <section className="filter-bar">
            <div className="search-box">
              <IconSearch />
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
                <IconShield />
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
                          <span className="service-tag">{inc.service}</span>
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
                          className={`table-status-select status-${inc.status.toLowerCase()}`}
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
                              <IconCheck />
                              <span>Resolve</span>
                            </button>
                          )}
                          <button
                            className="action-icon-btn danger"
                            title="Delete incident"
                            onClick={() => handleDelete(inc.id)}
                          >
                            <IconTrash />
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
                <IconClose />
              </button>
            </div>

            <form onSubmit={handleCreate}>
              <div className="form-group">
                <label>Incident Title *</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Ingress Controller Latency Spike"
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
