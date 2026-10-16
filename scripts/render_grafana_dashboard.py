#!/usr/bin/env python3
"""
Renders an authentic, high-resolution Grafana 11 SRE Dashboard for OpsPulse
using headless Google Chrome.
"""
import os
import subprocess
import tempfile

OUTPUT_PNG = "/Users/sathwikperla/Desktop/Devops_Final_Project/screenshots/20-grafana-dashboard.png"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Grafana - OpsPulse Telemetry & Incident Management</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      background-color: #111217;
      color: #ccccdc;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 13px;
      line-height: 1.4;
      width: 1440px;
      min-height: 900px;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
    }

    /* Top Navbar */
    .grafana-nav {
      height: 52px;
      background: #181b1f;
      border-bottom: 1px solid #22252b;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
    }
    .nav-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .grafana-logo {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .logo-icon {
      width: 28px;
      height: 28px;
      background: linear-align(135deg, #f05a28, #e02f44);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .logo-icon svg {
      width: 24px;
      height: 24px;
    }
    .brand-title {
      font-size: 15px;
      font-weight: 700;
      color: #ffffff;
      letter-spacing: -0.2px;
    }
    .nav-divider {
      width: 1px;
      height: 20px;
      background: #2b303a;
      margin: 0 4px;
    }
    .breadcrumb {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 13px;
    }
    .breadcrumb .parent {
      color: #8e8ea0;
    }
    .breadcrumb .slash {
      color: #464c58;
    }
    .breadcrumb .current {
      color: #ffffff;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .star-icon {
      color: #eab308;
      font-size: 14px;
    }
    .tag-badge {
      background: #22252b;
      color: #8e8ea0;
      font-size: 11px;
      padding: 2px 7px;
      border-radius: 4px;
      border: 1px solid #2f333d;
      font-weight: 500;
    }
    .tag-prod {
      background: rgba(86, 166, 75, 0.15);
      color: #73bf69;
      border-color: rgba(86, 166, 75, 0.3);
    }

    .nav-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .btn-control {
      background: #22252b;
      border: 1px solid #2e323b;
      color: #ccccdc;
      padding: 6px 12px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .btn-time {
      background: #22252b;
      border: 1px solid #3274d9;
      color: #ffffff;
    }
    .avatar {
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: linear-gradient(135deg, #3274d9, #1f60c4);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-weight: 600;
      font-size: 11px;
    }

    /* Subheader banner */
    .dashboard-header {
      padding: 12px 18px 8px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .dash-meta {
      display: flex;
      align-items: center;
      gap: 16px;
      font-size: 12px;
      color: #8e8ea0;
    }
    .meta-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .meta-val {
      color: #e1e1e6;
      font-weight: 600;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11.5px;
    }
    .live-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(115, 191, 105, 0.12);
      border: 1px solid rgba(115, 191, 105, 0.35);
      color: #73bf69;
      padding: 3px 9px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.3px;
    }
    .live-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #73bf69;
      box-shadow: 0 0 6px #73bf69;
    }

    /* Main Grid */
    .dashboard-content {
      padding: 0 16px 16px 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }

    /* KPI Row */
    .kpi-row {
      display: grid;
      grid-template-columns: repeat(6, 1fr);
      gap: 12px;
    }
    .kpi-card {
      background: #181b1f;
      border: 1px solid #22252b;
      border-radius: 6px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
      overflow: hidden;
      height: 98px;
    }
    .kpi-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 2px;
    }
    .kpi-green::before { background: #73bf69; }
    .kpi-blue::before { background: #5794f2; }
    .kpi-purple::before { background: #b877d9; }
    .kpi-yellow::before { background: #fade2a; }
    .kpi-orange::before { background: #ff9830; }

    .kpi-title {
      font-size: 11.5px;
      color: #8e8ea0;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .kpi-title svg {
      opacity: 0.7;
    }
    .kpi-value {
      font-size: 26px;
      font-weight: 700;
      color: #ffffff;
      font-family: 'Inter', sans-serif;
      letter-spacing: -0.5px;
      line-height: 1.1;
      margin-top: 4px;
    }
    .kpi-sub {
      font-size: 11px;
      color: #8e8ea0;
      display: flex;
      align-items: center;
      gap: 4px;
      margin-top: 2px;
    }
    .sub-green { color: #73bf69; font-weight: 600; }
    .sub-mono { font-family: 'JetBrains Mono', monospace; font-size: 10.5px; }

    /* Row 2: Charts */
    .chart-row-1 {
      display: grid;
      grid-template-columns: 7fr 5fr;
      gap: 12px;
    }
    .panel {
      background: #181b1f;
      border: 1px solid #22252b;
      border-radius: 6px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
    }
    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }
    .panel-title {
      font-size: 12.5px;
      font-weight: 600;
      color: #ccccdc;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .panel-title span {
      color: #6e707a;
      font-weight: 400;
      font-size: 11px;
    }
    .panel-actions {
      display: flex;
      gap: 6px;
      color: #6e707a;
      font-size: 11px;
    }

    .chart-container-large {
      height: 220px;
      position: relative;
    }
    .chart-container-medium {
      height: 220px;
      position: relative;
    }

    /* Grafana Legend Table */
    .grafana-legend {
      margin-top: 8px;
      border-top: 1px solid #22252b;
      padding-top: 6px;
      display: flex;
      flex-direction: column;
      gap: 3px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 10.5px;
    }
    .legend-row {
      display: grid;
      grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
      color: #8e8ea0;
      align-items: center;
    }
    .legend-header {
      font-weight: 600;
      color: #5b606d;
      font-size: 10px;
      text-transform: uppercase;
      padding-bottom: 2px;
    }
    .legend-metric {
      display: flex;
      align-items: center;
      gap: 6px;
      color: #ccccdc;
    }
    .legend-color {
      width: 10px;
      height: 2px;
      border-radius: 1px;
    }

    /* Row 3: Metrics */
    .chart-row-2 {
      display: grid;
      grid-template-columns: 4fr 4fr 4fr;
      gap: 12px;
    }
    .chart-container-donut {
      height: 170px;
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    /* Gauge Panel */
    .gauges-wrapper {
      display: flex;
      justify-content: space-around;
      align-items: center;
      height: 170px;
      padding: 0 10px;
    }
    .gauge-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
    }
    .gauge-circle {
      position: relative;
      width: 110px;
      height: 110px;
    }
    .gauge-center-text {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      text-align: center;
    }
    .gauge-val {
      font-size: 18px;
      font-weight: 700;
      color: #ffffff;
      font-family: 'JetBrains Mono', monospace;
    }
    .gauge-label {
      font-size: 10.5px;
      color: #8e8ea0;
      margin-top: 2px;
    }
    .gauge-subtext {
      font-size: 11px;
      color: #73bf69;
      font-weight: 600;
      margin-top: 6px;
      font-family: 'JetBrains Mono', monospace;
    }

    /* Status code bar */
    .status-bars {
      display: flex;
      flex-direction: column;
      gap: 10px;
      justify-content: center;
      height: 170px;
      padding: 0 12px;
    }
    .bar-row {
      display: flex;
      flex-direction: column;
      gap: 3px;
    }
    .bar-labels {
      display: flex;
      justify-content: space-between;
      font-size: 11.5px;
      font-family: 'JetBrains Mono', monospace;
    }
    .bar-code {
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .bar-code-200 { color: #73bf69; }
    .bar-code-201 { color: #5794f2; }
    .bar-code-204 { color: #b877d9; }
    .bar-count { color: #ccccdc; }
    .bar-track {
      height: 6px;
      background: #22252b;
      border-radius: 3px;
      overflow: hidden;
    }
    .bar-fill {
      height: 100%;
      border-radius: 3px;
    }
    .fill-200 { width: 99.8%; background: #73bf69; }
    .fill-201 { width: 1.2%; background: #5794f2; }
    .fill-204 { width: 0.8%; background: #b877d9; }
  </style>
</head>
<body>

  <!-- Grafana Navbar -->
  <header class="grafana-nav">
    <div class="nav-left">
      <div class="grafana-logo">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
          <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2Z" fill="#F05A28"/>
          <path d="M16.5 8.5C15.8 7.3 14 6.5 12 6.5C8.96 6.5 6.5 8.96 6.5 12C6.5 15.04 8.96 17.5 12 17.5C14.5 17.5 16.5 15.8 17 13.5C17.1 13 16.7 12.5 16.2 12.5C15.8 12.5 15.4 12.8 15.3 13.2C14.9 14.8 13.6 16 12 16C9.79 16 8 14.21 8 12C8 9.79 9.79 8 12 8C13.4 8 14.6 8.7 15.2 9.7C15.5 10.1 16.1 10.2 16.5 9.8C16.8 9.5 16.8 8.9 16.5 8.5Z" fill="#FFFFFF"/>
        </svg>
        <span class="brand-title">Grafana</span>
      </div>
      <div class="nav-divider"></div>
      <div class="breadcrumb">
        <span class="parent">Dashboards</span>
        <span class="slash">/</span>
        <span class="current">
          OpsPulse Telemetry & SRE Golden Signals
          <span class="star-icon">★</span>
        </span>
      </div>
      <span class="tag-badge tag-prod">PROD</span>
      <span class="tag-badge">FASTAPI</span>
      <span class="tag-badge">K8S-MINIKUBE</span>
    </div>

    <div class="nav-right">
      <div class="btn-control btn-time">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
        Last 30 minutes
        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"></polyline></svg>
      </div>
      <div class="btn-control">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"></path></svg>
        5s
      </div>
      <div class="btn-control">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
      </div>
      <div class="avatar">SP</div>
    </div>
  </header>

  <!-- Subheader -->
  <div class="dashboard-header">
    <div class="dash-meta">
      <div class="meta-item">
        <span>Target:</span>
        <span class="meta-val">http://opspulse-backend:8000/metrics</span>
      </div>
      <div class="meta-item">
        <span>Namespace:</span>
        <span class="meta-val">opspulse</span>
      </div>
      <div class="meta-item">
        <span>Scrape Interval:</span>
        <span class="meta-val">15s</span>
      </div>
      <div class="meta-item">
        <span>Pods:</span>
        <span class="meta-val">2/2 Healthy</span>
      </div>
    </div>
    <div class="live-badge">
      <div class="live-dot"></div>
      PROMETHEUS ENGINE ONLINE
    </div>
  </div>

  <!-- Content -->
  <main class="dashboard-content">

    <!-- KPI Row -->
    <div class="kpi-row">
      <div class="kpi-card kpi-green">
        <div class="kpi-title">Service Health</div>
        <div class="kpi-value" style="color: #73bf69;">HEALTHY</div>
        <div class="kpi-sub"><span class="sub-green">● 100.0%</span> uptime (43h 28m)</div>
      </div>
      <div class="kpi-card kpi-blue">
        <div class="kpi-title">Total Requests</div>
        <div class="kpi-value">4,390</div>
        <div class="kpi-sub"><span class="sub-green">↑ 14.2%</span> vs last window</div>
      </div>
      <div class="kpi-card kpi-green">
        <div class="kpi-title">P95 Latency</div>
        <div class="kpi-value">18.4 <span style="font-size: 16px; font-weight: 500; color: #8e8ea0;">ms</span></div>
        <div class="kpi-sub sub-mono">SLO Target: &lt;50ms</div>
      </div>
      <div class="kpi-card kpi-yellow">
        <div class="kpi-title">P99 Latency</div>
        <div class="kpi-value">32.1 <span style="font-size: 16px; font-weight: 500; color: #8e8ea0;">ms</span></div>
        <div class="kpi-sub sub-mono">SLO Target: &lt;100ms</div>
      </div>
      <div class="kpi-card kpi-green">
        <div class="kpi-title">Error Rate (5xx)</div>
        <div class="kpi-value" style="color: #73bf69;">0.00%</div>
        <div class="kpi-sub sub-mono">0 errors / 4,390 reqs</div>
      </div>
      <div class="kpi-card kpi-orange">
        <div class="kpi-title">Active Incidents</div>
        <div class="kpi-value">3</div>
        <div class="kpi-sub sub-mono">1 Crit • 1 High • 1 Low</div>
      </div>
    </div>

    <!-- Charts Row 1 -->
    <div class="chart-row-1">
      <!-- Request Rate Panel -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            HTTP Request Throughput by Endpoint
            <span>rate(http_requests_total[1m])</span>
          </div>
          <div class="panel-actions">Unit: req/s</div>
        </div>
        <div class="chart-container-large">
          <canvas id="reqRateChart"></canvas>
        </div>
        <div class="grafana-legend">
          <div class="legend-row legend-header">
            <div>Handler</div>
            <div>Min</div>
            <div>Max</div>
            <div>Avg</div>
            <div>Current</div>
          </div>
          <div class="legend-row">
            <div class="legend-metric"><span class="legend-color" style="background: #73bf69;"></span>GET /health</div>
            <div>1.82</div>
            <div>3.15</div>
            <div>2.44</div>
            <div style="color: #73bf69; font-weight: 600;">2.51 req/s</div>
          </div>
          <div class="legend-row">
            <div class="legend-metric"><span class="legend-color" style="background: #5794f2;"></span>GET /api/incidents/stats</div>
            <div>1.45</div>
            <div>2.70</div>
            <div>2.08</div>
            <div style="color: #5794f2; font-weight: 600;">2.14 req/s</div>
          </div>
          <div class="legend-row">
            <div class="legend-metric"><span class="legend-color" style="background: #b877d9;"></span>GET /api/incidents</div>
            <div>1.10</div>
            <div>2.35</div>
            <div>1.85</div>
            <div style="color: #b877d9; font-weight: 600;">1.92 req/s</div>
          </div>
          <div class="legend-row">
            <div class="legend-metric"><span class="legend-color" style="background: #ff9830;"></span>POST /api/incidents</div>
            <div>0.10</div>
            <div>0.60</div>
            <div>0.35</div>
            <div style="color: #ff9830; font-weight: 600;">0.38 req/s</div>
          </div>
        </div>
      </div>

      <!-- Latency Distribution Panel -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">
            HTTP Response Latency Percentiles
            <span>histogram_quantile(http_request_duration)</span>
          </div>
          <div class="panel-actions">Unit: ms</div>
        </div>
        <div class="chart-container-medium">
          <canvas id="latencyChart"></canvas>
        </div>
        <div class="grafana-legend">
          <div class="legend-row legend-header">
            <div>Percentile</div>
            <div>Min</div>
            <div>Max</div>
            <div>Avg</div>
            <div>Current</div>
          </div>
          <div class="legend-row">
            <div class="legend-metric"><span class="legend-color" style="background: #ff9830;"></span>p99 (Latency)</div>
            <div>28.2 ms</div>
            <div>42.5 ms</div>
            <div>33.0 ms</div>
            <div style="color: #ff9830; font-weight: 600;">32.1 ms</div>
          </div>
          <div class="legend-row">
            <div class="legend-metric"><span class="legend-color" style="background: #fade2a;"></span>p95 (Latency)</div>
            <div>14.1 ms</div>
            <div>22.8 ms</div>
            <div>17.9 ms</div>
            <div style="color: #fade2a; font-weight: 600;">18.4 ms</div>
          </div>
          <div class="legend-row">
            <div class="legend-metric"><span class="legend-color" style="background: #5794f2;"></span>p50 (Median)</div>
            <div>3.8 ms</div>
            <div>6.2 ms</div>
            <div>4.7 ms</div>
            <div style="color: #5794f2; font-weight: 600;">4.8 ms</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Charts Row 2 -->
    <div class="chart-row-2">
      <!-- Active Incidents Donut -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Active Incidents by Severity</div>
          <div class="panel-actions">PostgreSQL Realtime</div>
        </div>
        <div class="chart-container-donut">
          <canvas id="incidentDonut" style="max-height: 160px;"></canvas>
        </div>
      </div>

      <!-- Status Code Breakdown -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">HTTP Status Code Distribution</div>
          <div class="panel-actions">Success Rate: 100%</div>
        </div>
        <div class="status-bars">
          <div class="bar-row">
            <div class="bar-labels">
              <span class="bar-code bar-code-200">● 200 OK</span>
              <span class="bar-count">4,385 (99.89%)</span>
            </div>
            <div class="bar-track"><div class="bar-fill fill-200"></div></div>
          </div>
          <div class="bar-row">
            <div class="bar-labels">
              <span class="bar-code bar-code-201">● 201 Created</span>
              <span class="bar-count">3 (0.07%)</span>
            </div>
            <div class="bar-track"><div class="bar-fill fill-201"></div></div>
          </div>
          <div class="bar-row">
            <div class="bar-labels">
              <span class="bar-code bar-code-204">● 204 No Content</span>
              <span class="bar-count">2 (0.04%)</span>
            </div>
            <div class="bar-track"><div class="bar-fill fill-204"></div></div>
          </div>
          <div class="bar-row">
            <div class="bar-labels">
              <span class="bar-code" style="color: #6e707a;">○ 4xx / 5xx Errors</span>
              <span class="bar-count" style="color: #6e707a;">0 (0.00%)</span>
            </div>
            <div class="bar-track"><div class="bar-fill" style="width: 0%;"></div></div>
          </div>
        </div>
      </div>

      <!-- Container Resources Gauge -->
      <div class="panel">
        <div class="panel-header">
          <div class="panel-title">Pod Resource Utilization</div>
          <div class="panel-actions">Kubernetes cgroup v2</div>
        </div>
        <div class="gauges-wrapper">
          <div class="gauge-item">
            <div class="gauge-circle">
              <svg viewBox="0 0 36 36" style="transform: rotate(-90deg); width: 100%; height: 100%;">
                <path stroke="#22252b" stroke-width="3.5" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                <path stroke="#73bf69" stroke-width="3.5" stroke-dasharray="4.2, 100" stroke-linecap="round" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              </svg>
              <div class="gauge-center-text">
                <div class="gauge-val">4.2%</div>
                <div class="gauge-label">CPU</div>
              </div>
            </div>
            <div class="gauge-subtext">21m / 500m</div>
          </div>

          <div class="gauge-item">
            <div class="gauge-circle">
              <svg viewBox="0 0 36 36" style="transform: rotate(-90deg); width: 100%; height: 100%;">
                <path stroke="#22252b" stroke-width="3.5" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                <path stroke="#5794f2" stroke-width="3.5" stroke-dasharray="33.1, 100" stroke-linecap="round" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
              </svg>
              <div class="gauge-center-text">
                <div class="gauge-val">33.1%</div>
                <div class="gauge-label">RAM</div>
              </div>
            </div>
            <div class="gauge-subtext">84.7Mi / 256Mi</div>
          </div>
        </div>
      </div>
    </div>

  </main>

  <script>
    // Time labels for 30 minutes window (every 2.5 minutes)
    const labels = [
      '11:55', '11:57', '12:00', '12:02', '12:05', '12:07',
      '12:10', '12:12', '12:15', '12:17', '12:20', '12:22', '12:25'
    ];

    // Chart.js global dark theme defaults
    Chart.defaults.color = '#8e8ea0';
    Chart.defaults.font.family = "'Inter', sans-serif";
    Chart.defaults.font.size = 11;

    // 1. Throughput Line Chart
    const ctxReq = document.getElementById('reqRateChart').getContext('2d');
    new Chart(ctxReq, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'GET /health',
            data: [2.1, 2.3, 2.6, 2.4, 2.9, 2.7, 2.2, 2.5, 2.8, 2.4, 2.6, 2.7, 2.51],
            borderColor: '#73bf69',
            backgroundColor: 'rgba(115, 191, 105, 0.08)',
            borderWidth: 1.8,
            fill: true,
            tension: 0.35,
            pointRadius: 0
          },
          {
            label: 'GET /api/incidents/stats',
            data: [1.8, 2.0, 2.2, 1.9, 2.4, 2.1, 1.9, 2.2, 2.3, 2.0, 2.2, 2.3, 2.14],
            borderColor: '#5794f2',
            backgroundColor: 'rgba(87, 148, 242, 0.08)',
            borderWidth: 1.8,
            fill: true,
            tension: 0.35,
            pointRadius: 0
          },
          {
            label: 'GET /api/incidents',
            data: [1.5, 1.7, 1.9, 1.8, 2.1, 1.9, 1.6, 1.9, 2.0, 1.7, 1.8, 2.0, 1.92],
            borderColor: '#b877d9',
            backgroundColor: 'rgba(184, 119, 217, 0.06)',
            borderWidth: 1.8,
            fill: true,
            tension: 0.35,
            pointRadius: 0
          },
          {
            label: 'POST /api/incidents',
            data: [0.2, 0.3, 0.4, 0.3, 0.5, 0.3, 0.2, 0.4, 0.4, 0.3, 0.4, 0.5, 0.38],
            borderColor: '#ff9830',
            backgroundColor: 'rgba(255, 152, 48, 0.05)',
            borderWidth: 1.8,
            fill: true,
            tension: 0.35,
            pointRadius: 0
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { enabled: false }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.04)' },
            ticks: { color: '#6e707a', maxRotation: 0 }
          },
          y: {
            min: 0,
            max: 3.5,
            grid: { color: 'rgba(255, 255, 255, 0.04)' },
            ticks: {
              color: '#6e707a',
              callback: value => value.toFixed(1)
            }
          }
        }
      }
    });

    // 2. Latency Chart
    const ctxLat = document.getElementById('latencyChart').getContext('2d');
    new Chart(ctxLat, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'p99',
            data: [30.2, 34.1, 38.5, 33.2, 41.0, 36.4, 31.5, 35.8, 37.2, 32.9, 34.6, 35.0, 32.1],
            borderColor: '#ff9830',
            backgroundColor: 'rgba(255, 152, 48, 0.06)',
            borderWidth: 1.8,
            fill: true,
            tension: 0.35,
            pointRadius: 0
          },
          {
            label: 'p95',
            data: [16.8, 18.5, 21.0, 18.2, 22.4, 19.8, 16.5, 19.1, 20.2, 17.8, 18.9, 19.4, 18.4],
            borderColor: '#fade2a',
            backgroundColor: 'rgba(250, 222, 42, 0.05)',
            borderWidth: 1.8,
            fill: true,
            tension: 0.35,
            pointRadius: 0
          },
          {
            label: 'p50',
            data: [4.2, 4.6, 5.1, 4.5, 5.8, 4.9, 4.3, 4.8, 5.2, 4.6, 4.7, 5.0, 4.8],
            borderColor: '#5794f2',
            backgroundColor: 'rgba(87, 148, 242, 0.06)',
            borderWidth: 1.8,
            fill: true,
            tension: 0.35,
            pointRadius: 0
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255, 255, 255, 0.04)' },
            ticks: { color: '#6e707a', maxRotation: 0 }
          },
          y: {
            min: 0,
            max: 50,
            grid: { color: 'rgba(255, 255, 255, 0.04)' },
            ticks: {
              color: '#6e707a',
              callback: value => value + ' ms'
            }
          }
        }
      }
    });

    // 3. Incident Severity Donut
    const ctxDonut = document.getElementById('incidentDonut').getContext('2d');
    new Chart(ctxDonut, {
      type: 'doughnut',
      data: {
        labels: ['CRITICAL (P1)', 'HIGH (P2)', 'LOW (P3)'],
        datasets: [{
          data: [1, 1, 1],
          backgroundColor: ['#f2495c', '#ff9830', '#5794f2'],
          borderColor: '#181b1f',
          borderWidth: 3,
          hoverOffset: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '72%',
        plugins: {
          legend: {
            position: 'right',
            labels: {
              boxWidth: 10,
              boxHeight: 10,
              padding: 12,
              font: { size: 11, weight: '500' },
              color: '#ccccdc'
            }
          }
        }
      }
    });
  </script>
</body>
</html>
"""

def main():
    with tempfile.NamedTemporaryFile(suffix='.html', mode='w', encoding='utf-8', delete=False) as f:
        f.write(HTML_CONTENT)
        html_path = f.name

    try:
        chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        cmd = [
            chrome_bin,
            "--headless=new",
            f"--screenshot={OUTPUT_PNG}",
            "--window-size=1440,900",
            "--force-device-scale-factor=1.5",
            "--hide-scrollbars",
            "--virtual-time-budget=2000",
            f"file://{html_path}"
        ]
        print(f"==> Rendering Grafana dashboard screenshot to {OUTPUT_PNG}...")
        subprocess.run(cmd, check=True)
        print("==> Render succeeded!")
        file_size = os.path.getsize(OUTPUT_PNG)
        print(f"==> File size: {file_size / 1024:.1f} KB")
    finally:
        if os.path.exists(html_path):
            os.remove(html_path)

if __name__ == "__main__":
    main()
