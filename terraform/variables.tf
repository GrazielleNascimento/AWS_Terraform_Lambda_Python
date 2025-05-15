variable "region" {
  description = "Região AWS"
  type        = string
  default     = "us-east-1"
}

variable "profile" {
  description = "Perfil AWS CLI"
  type        = string
  default     = "default"
}

variable "lambda_runtime" {
  description = "Runtime para funções Lambda"
  type        = string
  default     = "python3.9"
}

variable "dynamodb_table_name" {
  description = "Nome da tabela DynamoDB"
  type        = string
  default     = "MarketList"
}

variable "environment" {
  description = "Ambiente de deploy (dev, prod)"
  type        = string
  default     = "dev"
}