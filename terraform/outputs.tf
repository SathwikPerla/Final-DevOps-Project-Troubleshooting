output "cluster_name" {
  description = "The name of the provisioned EKS cluster"
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "The endpoint URL for the EKS control plane"
  value       = module.eks.cluster_endpoint
}

output "vpc_id" {
  description = "The ID of the provisioned VPC"
  value       = module.vpc.vpc_id
}

output "public_subnets" {
  description = "List of public subnet IDs in the VPC"
  value       = module.vpc.public_subnets
}

output "private_subnets" {
  description = "List of private subnet IDs in the VPC"
  value       = module.vpc.private_subnets
}

output "configure_kubectl" {
  description = "Command to configure kubectl credentials for the cluster"
  value       = "aws eks --region ${var.region} update-kubeconfig --name ${module.eks.cluster_name}"
}
