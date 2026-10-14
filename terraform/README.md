# OpsPulse AWS Infrastructure as Code (Terraform)

This directory defines the automated cloud infrastructure provisioning for the OpsPulse Incident & Reliability Management platform on Amazon Web Services (AWS).

---

## Infrastructure Architecture

- **AWS VPC**: Custom CIDR block `10.20.0.0/16` deployed across two Availability Zones (`ap-south-1a`, `ap-south-1b`).
- **Subnets**:
  - Two Public Subnets (`10.20.101.0/24`, `10.20.102.0/24`) with Internet Gateway and AWS Load Balancer tags.
  - Two Private Subnets (`10.20.1.0/24`, `10.20.2.0/24`) with single NAT Gateway for secure egress.
- **Amazon EKS**: Kubernetes version 1.31 with managed node groups (`t3.medium`, 2-4 nodes).
- **IAM**: Automated role creation and cluster creator admin permissions.

---

## Execution Workflow

### 1. Initialize Working Directory
Downloads AWS provider plugins and verified modules:
```bash
terraform init
```

### 2. Format & Validate HCL
```bash
terraform fmt -check
terraform validate
```

### 3. Generate Execution Plan
```bash
terraform plan -out=tfplan
```

### 4. Apply Cloud Provisioning
```bash
terraform apply tfplan
```

### 5. Configure Local Kubectl
After cluster creation, link local `kubectl` to the new EKS cluster:
```bash
aws eks --region ap-south-1 update-kubeconfig --name opspulse-cluster
```

### 6. Clean Teardown (Avoid Runaway AWS Costs)
```bash
terraform destroy -auto-approve
```

> [!IMPORTANT]
> Never commit AWS access keys, secret keys, or `.tfstate` files to GitHub. All state files and credentials are strictly ignored via `.gitignore`.
