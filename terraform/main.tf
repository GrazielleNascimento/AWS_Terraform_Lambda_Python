# Lambda Functions

module "hello_terraform" {
  source = "./modules/lambda"

  function_name = "hello-terraform-python"
  role_arn      = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = var.lambda_runtime
  
  filename         = "../dist/hello_terraform_lambda.zip"
  source_code_hash = filebase64sha256("../dist/hello_terraform_lambda.zip")
  
  memory_size = 128
  timeout     = 10
  
  environment_variables = {
    ENVIRONMENT = var.environment
  }
  
  tags = {
    Environment = var.environment
    Function    = "hello-terraform"
  }
}

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

module "update_item" {
  source = "./modules/lambda"

  function_name = "update-item-python"
  role_arn      = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = var.lambda_runtime
  
  filename         = "../dist/update_item_lambda.zip"
  source_code_hash = filebase64sha256("../dist/update_item_lambda.zip")
  
  memory_size = 256
  timeout     = 15
  
  environment_variables = {
    DYNAMODB_TABLE_NAME = aws_dynamodb_table.market_list_table.name
  }
  
  tags = {
    Environment = var.environment
    Function    = "update-item"
  }
}

module "delete_item" {
  source = "./modules/lambda"

  function_name = "delete-item-python"
  role_arn      = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = var.lambda_runtime
  
  filename         = "../dist/delete_item_lambda.zip"
  source_code_hash = filebase64sha256("../dist/delete_item_lambda.zip")
  
  memory_size = 256
  timeout     = 15
  
  environment_variables = {
    DYNAMODB_TABLE_NAME = aws_dynamodb_table.market_list_table.name
  }
  
  tags = {
    Environment = var.environment
    Function    = "delete-item"
  }
}