output "iam_access_key_user_key_id" {
  value     = aws_iam_access_key.s3_user_key.id
  sensitive = true
}

output "iam_access_key_user_key_secret" {
  value     = aws_iam_access_key.s3_user_key.secret
  sensitive = true
}

output "bucket_name" {
  value = var.bucket_name
}
