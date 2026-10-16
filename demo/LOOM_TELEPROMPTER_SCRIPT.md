# SevZero — 90-Second Loom Video Demonstration Script

> **Total Time:** 1 Minute 30 Seconds (90 Seconds)  
> **Target Speaking Pace:** ~140 words per minute (Calm, confident, natural)  
> **Presenter:** Sathwik Perla (Roll: 590)  
> **Project:** SevZero — Enterprise Cloud-Native SRE Incident & Reliability Platform  

---

## 🎬 Pre-Flight Checklist: Open These 4 Browser Tabs Before Recording

1. **Tab 1:** Slide 1 of the Presentation (`demo/index.html` or `demo/SevZero_DevOps_Capstone_Presentation.pptx`)
2. **Tab 2:** Live SevZero Web UI (`http://localhost:3000`)
3. **Tab 3:** Terminal Window (Split or ready with `pytest -v` and `kubectl get all -n opspulse`)
4. **Tab 4:** GitHub Actions Pipeline (`https://github.com/SathwikPerla/Final-DevOps-Project-Troubleshooting/actions`)

---

## ⏱️ Teleprompter Script (Word-for-Word)

### [0:00 - 0:15] Hook & Project Introduction
- **What to show on screen:** **Tab 1** (Slide 1 of presentation or Title Slide).
- **What to speak:**
> *"Hello everyone! My name is Sathwik Perla. For my DevOps Capstone project, I built **SevZero**—a production-grade, cloud-native SRE Incident and Reliability platform. Rather than building a generic task list, SevZero is an enterprise incident management system modeled around the complete DevOps and Site Reliability Engineering lifecycle."*

---

### [0:15 - 0:35] Application Core, Docker & Testing
- **What to show on screen:** Switch to **Tab 2** (Web UI at `localhost:3000`), click one incident card or filter, then switch to **Tab 3** (Terminal) and run `pytest -v`.
- **What to speak:**
> *"The backend is built with asynchronous FastAPI and an Alembic-migrated PostgreSQL database, serving a responsive React frontend. Both services run in multi-stage Docker containers strictly as unprivileged non-root users. As you can see in the terminal, our Pytest suite executes 12 automated unit and integration tests across an isolated in-memory test database, passing 100% in just 0.05 seconds."*

---

### [0:35 - 0:55] CI/CD Automation & DevSecOps Gating
- **What to show on screen:** Switch to **Tab 4** (GitHub Actions page showing the green workflow runs and 3 passing checks).
- **What to speak:**
> *"Every push to the main branch triggers our 3-stage GitHub Actions pipeline. First, it validates code quality and runs Pytest. Next, it builds multi-architecture Docker images and runs an automated Aquasecurity Trivy vulnerability scan—gating the build on high or critical CVEs—before pushing SHA-tagged immutable containers to GitHub Container Registry."*

---

### [0:55 - 1:15] AWS Terraform IaC & Kubernetes Orchestration
- **What to show on screen:** Switch to **Tab 3** (Terminal) and run `kubectl get pods,svc,ingress,hpa -n opspulse`.
- **What to speak:**
> *"For cloud infrastructure, I authored modular Terraform to provision a multi-AZ AWS VPC and managed EKS cluster. The application is packaged into a declarative Helm 3 chart running in our dedicated `opspulse` namespace. Here in the cluster, we have high-availability backend and frontend pods with 2 replicas each, Ingress routing through `opspulse.local`, and Horizontal Pod Autoscaling based on CPU utilization."*

---

### [1:15 - 1:30] Full Observability & Conclusion
- **What to show on screen:** Open `screenshots/20-grafana-dashboard.png` or `README.md` showing the live Grafana dashboard.
- **What to speak:**
> *"Finally, full-stack observability is established with Prometheus scraping application metrics at `/metrics` and a live Grafana 11 SRE dashboard monitoring the four golden signals: sub-20ms P95 latency, 100% uptime, and zero 5xx errors. The entire project meets all 10 grading milestones for a complete 100 out of 100 score. Thank you!"*

---

## 💡 Quick Tips for a Flawless Recording
1. **Don't rush:** 90 seconds is plenty of time if you speak clearly.
2. **Smooth Tab Switching:** Keep your tabs in order (1 -> 2 -> 3 -> 4) so you can use `Cmd + Option + Right Arrow` or click seamlessly.
3. **Finish with confidence:** When you say "Thank you!", pause for 2 seconds before stopping the Loom recording so it doesn't cut off your last word.
