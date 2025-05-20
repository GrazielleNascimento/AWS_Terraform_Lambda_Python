variable "user_pool_name" {
  description = "Nome do Cognito User Pool"
  type        = string
}

variable "client_name" {
  description = "Nome do App Client"
  type        = string
}

variable "domain_prefix" {
  description = "Prefixo do domínio do Cognito"
  type        = string
}