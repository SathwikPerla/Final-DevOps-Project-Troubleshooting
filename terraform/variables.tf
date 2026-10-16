variable "region" {
  description = "The target AWS region for SevZero cloud infrastructure"
  type        = string
  default     = "ap-south-1"
}

variable "cluster_name" {
  description = "The EKS cluster identifier"
  type        = string
  default     = "sevzero-cluster"
}

variable "vpc_cidr" {
  description = "The CIDR block for the dedicated SevZero VPC"
  type        = string
  default     = "10.20.0.0/16"
}
