resource "kubernetes_secret" "secrets" {
  for_each = toset(local.namespaces)

  metadata {
    name      = "aws-creds"
    namespace = each.key
  }

  data = {
    AWS_ACCESS_KEY_ID = var.aws_access_key_id
    AWS_SECRET_ACCESS_KEY = var.aws_secret_access_key
  }

  type = "Opaque"
}
