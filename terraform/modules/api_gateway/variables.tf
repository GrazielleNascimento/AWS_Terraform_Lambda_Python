variable "api_name" {
  description = "Nome do API Gateway"
  type        = string
}

variable "environment" {
  description = "Ambiente de deploy"
  type        = string
}

variable "cognito_user_pool_arn" {
  description = "ARN do Cognito User Pool"
  type        = string
}

variable "lambda_invoke_arn" {
  description = "ARN para invocação da função Lambda"
  type        = string
}

variable "lambda_function_name" {
  description = "Nome da função Lambda"
  type        = string
}

variable "lambda_add_item_arn" {
  type = string
}

variable "lambda_add_item_function_name" {
  type = string
}

variable "api_gateway_cloudwatch_role_arn" {
  description = "ARN do IAM Role para CloudWatch logs do API Gateway"
  type        = string
}
