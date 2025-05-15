module "add_item" {
  source = "./modules/lambda"

  function_name = "add-item-python"
  role_arn      = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = var.lambda_runtime
  
  filename         = "../dist/add_item_lambda.zip"
  source_code_hash = filebase64sha256("../dist/add_item_lambda.zip")
  
  memory_size = 256
  timeout     = 15
  
  environment_variables = {
    DYNAMODB_TABLE_NAME = aws_dynamodb_table.market_list_table.name
  }
  
  tags = {
    Environment = var.environment
    Function    = "add-item"
  }
}