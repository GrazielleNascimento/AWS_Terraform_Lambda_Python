output "dynamodb_table_name" {
  description = "Nome da tabela DynamoDB"
  value       = aws_dynamodb_table.market_list_table.name
}

output "hello_terraform_lambda_arn" {
  description = "ARN da função Lambda Hello Terraform"
  value       = module.hello_terraform.function_arn
}

output "add_item_lambda_arn" {
  description = "ARN da função Lambda Add Item"
  value       = module.add_item.function_arn
}

output "update_item_lambda_arn" {
  description = "ARN da função Lambda Update Item"
  value       = module.update_item.function_arn
}

output "delete_item_lambda_arn" {
  description = "ARN da função Lambda Delete Item"
  value       = module.delete_item.function_arn
}

output "api_gateway_endpoint" {
  description = "Endpoint do API Gateway para /hello"
  value       = module.api_gateway.api_endpoint
}
output "get_item_lambda_arn" {
  description = "ARN da função Lambda Add Item"
  value       = module.get_item.function_arn
}