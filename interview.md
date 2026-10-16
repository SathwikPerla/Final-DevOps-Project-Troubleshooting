# OpsPulse — DevOps & SRE Capstone Interview Preparation Guide

> **Project:** OpsPulse — Enterprise DevOps Incident & Service Reliability Management Platform  
> **Course:** DevOps Engineering Capstone (100/100 Rubric Verified)  
> **Core Tech:** FastAPI, React (Vite), PostgreSQL, Alembic, Docker, Kubernetes (Minikube / EKS), Helm 3, Terraform, Prometheus, Grafana, GitHub Actions, Trivy

---

## 1. 30-Second Elevator Pitch

> *"Most student projects are basic CRUD applications on localhost. For my capstone, I built **OpsPulse**—a production-grade, cloud-native DevOps incident and reliability management platform designed around the complete SRE lifecycle.*  
>  
> *It features an asynchronous FastAPI backend instrumented with Prometheus metrics and an Alembic-managed PostgreSQL database. I built a multi-stage, non-root Docker container architecture, secured it with automated Trivy DevSecOps vulnerability gating in a GitHub Actions CI/CD pipeline, and provisioned a multi-AZ AWS EKS cluster using modular Terraform IaC. Finally, I packaged the entire microservice stack into a Helm 3 chart with Ingress routing, Horizontal Pod Autoscaling (HPA), and real-time Grafana dashboard observability."*

---

## 2. The 10-Stage DevOps Lifecycle Architecture

```text
  [ Developer Push ]
          │
          ▼
┌──────────────────────────────────────┐
│  STAGE 1 & 2: QUALITY GATE           │
│  - FastAPI backend + React UI        │
│  - 12 Pytest test cases (SQLite DB)  │
└──────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────┐
│  STAGE 3, 4 & 5: DOCKER & CI/CD      │
│  - Multi-stage non-root containers   │
│  - GitHub Actions on `main` push     │
│  - Automated build & test execution  │
│  - Tagged GHCR image publishing      │
└──────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────┐
│  STAGE 6: DEVSECOPS SECURITY GATE    │
│  - Trivy vulnerability scanner       │
│  - Severity: HIGH, CRITICAL fail gate│
│  - Zero CVE deployment policy        │
└──────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────┐
│  STAGE 7: CLOUD INFRASTRUCTURE (IaC) │
│  - Modular Terraform HCL             │
│  - AWS VPC (2 public, 2 private)     │
│  - AWS EKS Managed Node Groups       │
└──────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────┐
│  STAGE 8 & 9: KUBERNETES & AUTOSCALE │
│  - Helm 3 chart with multi-replicas  │
│  - Ingress Controller routing        │
│  - HPA CPU/Memory autoscaling        │
└──────────────────────────────────────┘
          │
          ▼
┌──────────────────────────────────────┐
│  STAGE 10: OBSERVABILITY & METRICS   │
│  - Prometheus instrumentator (/metrics)
│  - Custom Grafana Dashboard (QPS,    │
│    latency, error rates, incidents)  │
└──────────────────────────────────────┘
```

---

## 3. Deep Dive Technical Questions & Verbatim Model Answers

### Q1: *"How did you secure your Docker containers for production?"*
> **Verbatim Answer:**  
> *"Container security was implemented at three levels:*  
> 1. *Non-Root Execution: Default containers run as root (UID 0), creating container breakout vulnerabilities. In our backend Dockerfile, we explicitly created a system user and group `appuser:10001` with `USER appuser`. In frontend Nginx, we used unprivileged Nginx (UID 101) listening on port 8080.*  
> 2. *Multi-Stage Builds: For the React frontend, Node.js and build tooling exist only in Stage 1 (`node:20-alpine as builder`). Only static compiled assets in `dist/` are copied to the runtime Nginx container, slashing image attack surface and size.*  
> 3. *DevSecOps Gate: Integrated Trivy scanning directly into GitHub Actions with `--exit-code 1 --severity HIGH,CRITICAL`, failing pipeline builds if unpatched CVEs are introduced."*

---

### Q2: *"Walk me through your Kubernetes deployment strategy, Ingress, and Autoscaling."*
> **Verbatim Answer:**  
> *"I packaged the platform into a production Helm 3 chart:*  
> *Each microservice (backend and frontend) runs with a minimum of 2 replicas managed via a `Deployment` with rolling update strategy (`maxSurge: 1, maxUnavailable: 0`) and `ClusterIP` services.*  
> *Traffic is routed into the cluster via an Nginx Ingress Controller using path-based routing: `/api` paths forward to the backend FastAPI service, while `/` routes to the React frontend.*  
> *To handle traffic spikes, I configured a Horizontal Pod Autoscaler (HPA) targeting 70% CPU and memory utilization, automatically scaling backend replicas from 2 up to 10 pods during simulated load tests."*

---

### Q3: *"How is observability set up, and how do you track service health?"*
> **Verbatim Answer:**  
> *"We implemented the golden signals of SRE:*  
> *In FastAPI, I integrated `prometheus-fastapi-instrumentator` to expose standard RED metrics (Rate, Errors, Duration) on `/metrics` alongside custom business metrics for incident status transitions.*  
> *Prometheus scrapes these endpoints via a `ServiceMonitor` every 15 seconds. In Grafana, I built a unified dashboard tracking QPS, P95 latency percentiles, 5xx error spikes, and active critical incidents, paired with Kubernetes health (`/health`) and readiness (`/ready`) probes to prevent traffic routing to unready pods."*

---

### Q4: *"Explain your Terraform modular architecture for AWS."*
> **Verbatim Answer:**  
> *"The infrastructure is provisioned through Terraform using declarative HCL separated into three reusable modules:*  
> 1. *`modules/vpc`: Creates an isolated Virtual Private Cloud across two Availability Zones with 2 public subnets (Internet Gateway) and 2 private subnets (NAT Gateway).*  
> 2. *`modules/eks`: Provisions the AWS EKS control plane and managed EC2 worker node groups (`t3.medium`) inside private subnets for defense-in-depth.*  
> 3. *Root Module: Ties the inputs, variables, and output endpoints together with remote state locking and validation via `terraform validate`."*

---

### Q5: *"Tell me about a real troubleshooting scenario you encountered and how you triaged it."*
> **Verbatim Answer:**  
> *"During capstone validation, we tested a failure recovery lab: simulating an image pull backoff by pushing an invalid container tag.*  
> *I used `kubectl describe pod` to inspect the event stream and diagnosed `ImagePullBackOff (ErrImagePull)`. Because our Helm release had rolling update safeguards, Kubernetes kept the healthy old replicas alive while halting the rollout of the failed revision. I executed `helm rollback opspulse <revision>` to instantly revert the deployment without dropping a single user request."*

---

## 4. Key Metrics to Quote in the Interview

* **Test Suite:** 12 automated Pytest test cases passing in <0.7s with isolated SQLite fixtures.
* **Security:** 0 High or Critical CVEs verified via automated Trivy scans.
* **Autoscaling:** HPA scaled backend pods 2 $\rightarrow$ 10 replicas under load.
* **Rubric Score:** 100 / 100 points across all 10 DevOps lifecycle modules.
