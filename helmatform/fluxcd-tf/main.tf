resource "flux_bootstrap_git" "this" {
  embedded_manifests = true
  path               = "helmatform/cluster"
  components_extra = [ "source-watcher" ]
  kustomization_override = file("${path.root}/kustomization.yaml")
}
