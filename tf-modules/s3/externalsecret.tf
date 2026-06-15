resource "aws_secretsmanager_secret" "s3" {
  name = var.secret_name
}

resource "aws_secretsmanager_secret_version" "s3_keys" {
  secret_id = aws_secretsmanager_secret.s3.id
  secret_string = jsonencode({
    access_key_id     = aws_iam_access_key.s3_user_key.id
    secret_access_key = aws_iam_access_key.s3_user_key.secret
  })
}
