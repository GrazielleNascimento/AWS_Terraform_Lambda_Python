resource "aws_cognito_user_pool" "this" {
  name = var.user_pool_name
}

resource "aws_cognito_user_pool_client" "this" {
  name         = var.client_name
  user_pool_id = aws_cognito_user_pool.this.id
  generate_secret = false

  explicit_auth_flows = [
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_SRP_AUTH"
  ]
}

resource "aws_cognito_user_pool_domain" "this" {
  domain       = var.domain_prefix
  user_pool_id = aws_cognito_user_pool.this.id
}
