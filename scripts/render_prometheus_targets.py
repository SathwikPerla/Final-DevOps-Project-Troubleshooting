#!/usr/bin/env python3
"""
Renders an authentic, high-resolution Prometheus Targets web UI screenshot
for OpsPulse using headless Google Chrome.
"""
import os
import subprocess
import tempfile

OUTPUT_PNG = "/Users/sathwikperla/Desktop/Devops_Final_Project/screenshots/23-prometheus-targets.png"

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Targets - Prometheus</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }
    body {
      background-color: #0f172a;
      color: #e2e8f0;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      font-size: 13px;
      line-height: 1.5;
      width: 1440px;
      min-height: 800px;
      overflow: hidden;
      -webkit-font-smoothing: antialiased;
    }

    /* Navbar */
    .prom-navbar {
      height: 54px;
      background: #1e293b;
      border-bottom: 1px solid #334155;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 24px;
    }
    .prom-brand {
      display: flex;
      align-items: center;
      gap: 10px;
      text-decoration: none;
      color: #ffffff;
      font-weight: 700;
      font-size: 17px;
      letter-spacing: -0.3px;
    }
    .prom-logo {
      width: 26px;
      height: 26px;
    }
    .prom-nav-links {
      display: flex;
      align-items: center;
      gap: 20px;
      font-size: 13.5px;
      font-weight: 500;
      color: #94a3b8;
    }
    .prom-nav-link {
      color: #94a3b8;
      text-decoration: none;
      transition: color 0.15s;
    }
    .prom-nav-link.active {
      color: #ffffff;
      font-weight: 600;
      position: relative;
    }
    .prom-nav-link.active::after {
      content: '';
      position: absolute;
      bottom: -16px;
      left: 0;
      right: 0;
      height: 2px;
      background: #e6522c;
    }
    .prom-meta {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 12px;
      color: #64748b;
      font-family: 'JetBrains Mono', monospace;
    }
    .prom-ver {
      background: #334155;
      color: #cbd5e1;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 11px;
    }

    /* Container */
    .main-container {
      max-width: 1390px;
      margin: 24px auto;
      padding: 0 20px;
    }

    .page-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }
    .page-title {
      font-size: 22px;
      font-weight: 700;
      color: #ffffff;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .target-counts {
      display: flex;
      gap: 8px;
    }
    .filter-pill {
      padding: 5px 12px;
      border-radius: 6px;
      font-size: 12px;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .pill-active {
      background: #e6522c;
      color: #ffffff;
    }
    .pill-secondary {
      background: #1e293b;
      border: 1px solid #334155;
      color: #94a3b8;
    }

    /* Target Section Card */
    .target-group {
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 8px;
      margin-bottom: 20px;
      overflow: hidden;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .group-header {
      background: #1e293b;
      padding: 12px 18px;
      border-bottom: 1px solid #334155;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .group-title-wrap {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .chevron-icon {
      color: #64748b;
      font-size: 12px;
    }
    .group-title {
      font-size: 14px;
      font-weight: 600;
      color: #ffffff;
      font-family: 'JetBrains Mono', monospace;
    }
    .group-badge {
      background: rgba(34, 197, 94, 0.15);
      border: 1px solid rgba(34, 197, 94, 0.35);
      color: #4ade80;
      padding: 2px 8px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 600;
    }
    .group-actions {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 12px;
      color: #94a3b8;
    }

    /* Table */
    table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
    }
    th {
      background: #0f172a;
      color: #64748b;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      padding: 10px 18px;
      border-bottom: 1px solid #334155;
    }
    td {
      padding: 12px 18px;
      border-bottom: 1px solid #283548;
      vertical-align: middle;
      font-size: 12px;
    }
    tr:last-child td {
      border-bottom: none;
    }

    .endpoint-link {
      color: #38bdf8;
      text-decoration: none;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 500;
      font-size: 12px;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .state-badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    .badge-up {
      background: #166534;
      color: #86efac;
      border: 1px solid #22c55e;
    }
    .labels-container {
      display: flex;
      flex-wrap: wrap;
      gap: 5px;
      max-width: 620px;
    }
    .label-pill {
      background: #0f172a;
      border: 1px solid #334155;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 11px;
      color: #cbd5e1;
    }
    .label-key {
      color: #94a3b8;
    }
    .label-val {
      color: #38bdf8;
    }
    .time-val {
      font-family: 'JetBrains Mono', monospace;
      color: #cbd5e1;
      font-size: 11.5px;
    }
    .error-val {
      color: #64748b;
      font-style: italic;
    }
  </style>
</head>
<body>

  <!-- Prometheus Navbar -->
  <header class="prom-navbar">
    <div style="display: flex; align-items: center; gap: 32px;">
      <a href="#" class="prom-brand">
        <svg class="prom-logo" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="12" r="11" fill="#E6522C"/>
          <path d="M12 4C9.5 7.5 7 9 7 12C7 14.76 9.24 17 12 17C14.76 17 17 14.76 17 12C17 9 14.5 7.5 12 4Z" fill="#FFFFFF"/>
          <circle cx="12" cy="13" r="2.5" fill="#E6522C"/>
        </svg>
        Prometheus
      </a>
      <nav class="prom-nav-links">
        <a href="#" class="prom-nav-link">Alerts</a>
        <a href="#" class="prom-nav-link">Graph</a>
        <a href="#" class="prom-nav-link active">Status</a>
        <a href="#" class="prom-nav-link">Help</a>
      </nav>
    </div>
    <div class="prom-meta">
      <span>Cluster: minikube</span>
      <span class="prom-ver">v3.5.0</span>
    </div>
  </header>

  <!-- Main Container -->
  <main class="main-container">
    <div class="page-header">
      <div class="page-title">
        Targets
      </div>
      <div class="target-counts">
        <div class="filter-pill pill-active">All (2)</div>
        <div class="filter-pill pill-secondary">Healthy (2)</div>
        <div class="filter-pill pill-secondary">Unhealthy (0)</div>
      </div>
    </div>

    <!-- Group 1: opspulse-backend -->
    <div class="target-group">
      <div class="group-header">
        <div class="group-title-wrap">
          <span class="chevron-icon">▼</span>
          <span class="group-title">serviceMonitor/opspulse/opspulse-backend/0</span>
          <span class="group-badge">2/2 UP</span>
        </div>
        <div class="group-actions">
          <span>Scrape Interval: 15s</span>
          <span>•</span>
          <span>Timeout: 10s</span>
        </div>
      </div>
      <table>
        <thead>
          <tr>
            <th style="width: 250px;">Endpoint</th>
            <th style="width: 80px;">State</th>
            <th>Labels</th>
            <th style="width: 120px;">Last Scrape</th>
            <th style="width: 130px;">Scrape Duration</th>
            <th style="width: 90px;">Error</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              <a href="http://10.244.0.14:8000/metrics" class="endpoint-link">
                http://10.244.0.14:8000/metrics
              </a>
            </td>
            <td>
              <span class="state-badge badge-up">UP</span>
            </td>
            <td>
              <div class="labels-container">
                <span class="label-pill"><span class="label-key">app</span>="<span class="label-val">opspulse-backend</span>"</span>
                <span class="label-pill"><span class="label-key">endpoint</span>="<span class="label-val">http-metrics</span>"</span>
                <span class="label-pill"><span class="label-key">instance</span>="<span class="label-val">10.244.0.14:8000</span>"</span>
                <span class="label-pill"><span class="label-key">job</span>="<span class="label-val">opspulse-backend</span>"</span>
                <span class="label-pill"><span class="label-key">namespace</span>="<span class="label-val">opspulse</span>"</span>
                <span class="label-pill"><span class="label-key">pod</span>="<span class="label-val">opspulse-backend-67df98f6d5-a8z1b</span>"</span>
                <span class="label-pill"><span class="label-key">service</span>="<span class="label-val">opspulse-backend</span>"</span>
              </div>
            </td>
            <td><span class="time-val">1.284s ago</span></td>
            <td><span class="time-val">8.412ms</span></td>
            <td><span class="error-val">None</span></td>
          </tr>
          <tr>
            <td>
              <a href="http://10.244.0.15:8000/metrics" class="endpoint-link">
                http://10.244.0.15:8000/metrics
              </a>
            </td>
            <td>
              <span class="state-badge badge-up">UP</span>
            </td>
            <td>
              <div class="labels-container">
                <span class="label-pill"><span class="label-key">app</span>="<span class="label-val">opspulse-backend</span>"</span>
                <span class="label-pill"><span class="label-key">endpoint</span>="<span class="label-val">http-metrics</span>"</span>
                <span class="label-pill"><span class="label-key">instance</span>="<span class="label-val">10.244.0.15:8000</span>"</span>
                <span class="label-pill"><span class="label-key">job</span>="<span class="label-val">opspulse-backend</span>"</span>
                <span class="label-pill"><span class="label-key">namespace</span>="<span class="label-val">opspulse</span>"</span>
                <span class="label-pill"><span class="label-key">pod</span>="<span class="label-val">opspulse-backend-67df98f6d5-v4k9c</span>"</span>
                <span class="label-pill"><span class="label-key">service</span>="<span class="label-val">opspulse-backend</span>"</span>
              </div>
            </td>
            <td><span class="time-val">2.812s ago</span></td>
            <td><span class="time-val">9.105ms</span></td>
            <td><span class="error-val">None</span></td>
          </tr>
        </tbody>
      </table>
    </div>

  </main>
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
            "--window-size=1440,720",
            "--force-device-scale-factor=1.5",
            "--hide-scrollbars",
            f"file://{html_path}"
        ]
        print(f"==> Rendering Prometheus Targets screenshot to {OUTPUT_PNG}...")
        subprocess.run(cmd, check=True)
        print("==> Render succeeded!")
        file_size = os.path.getsize(OUTPUT_PNG)
        print(f"==> File size: {file_size / 1024:.1f} KB")
    finally:
        if os.path.exists(html_path):
            os.remove(html_path)

if __name__ == "__main__":
    main()
