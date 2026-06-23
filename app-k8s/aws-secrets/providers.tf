# export KUBE_CONFIG_PATH=.kubeconfig

terraform {
  required_version = "~> 1.5"
  required_providers {
    kubernetes = {
      source  = "kubernetes"
      version = "~> 3.2.0"
    }
  }
}
