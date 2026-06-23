output "kube_config" {
  value     = kind_cluster.this.kubeconfig
  sensitive = true
}
