variable "aws_region" {
  type    = string
  default = "eu-west-2"
}

variable "bucket_name" {
  type    = string
  default = "helmatform-s3-bucket"
}

variable "iam_user_name" {
  type    = string
  default = "s3-access-user"
}

variable "secret_name" {
  type    = string
  default = "s3-access-keys"
}

variable "policy_name" {
  type    = string
  default = "s3-access-policy"
}
