variable "region" {
  description = "Região AWS"
  type        = string
  default     = "sa-east-1"
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