resource "aws_lambda_function" "this" {
  function_name = var.function_name
  role          = var.role_arn
  handler       = var.handler
  runtime       = var.runtime
  
  filename      = var.filename
  
  memory_size   = var.memory_size
  timeout       = var.timeout
  
  source_code_hash = var.source_code_hash
  
  dynamic "environment" {
    for_each = length(keys(var.environment_variables)) > 0 ? [1] : []
    content {
      variables = var.environment_variables
    }
  }
  
  tags = var.tags
}