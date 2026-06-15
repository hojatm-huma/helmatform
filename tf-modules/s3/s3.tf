resource "aws_s3_bucket" "s3" {
  bucket = var.bucket_name
}

resource "aws_iam_user" "s3_user" {
  name = var.iam_user_name
}

resource "aws_iam_user_policy" "s3_user_policy" {
  name = var.policy_name
  user = aws_iam_user.s3_user.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket"
        ]
        Resource = aws_s3_bucket.s3.arn
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.s3.arn}/*"
      }
    ]
  })
}

resource "aws_iam_access_key" "s3_user_key" {
  user = aws_iam_user.s3_user.name
}
