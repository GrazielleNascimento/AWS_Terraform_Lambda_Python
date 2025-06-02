# Bucket para armazenar o tfstate

terraform {
  backend "s3" {
    bucket         = "my-terraform-state-bucket-dev-v7"
    key            = "global/s3/terraform.tfstate"
    region         = "sa-east-1"
    dynamodb_table = "terraform-locks-dev"
    encrypt        = true
  }

}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "my-terraform-state-bucket-dev-v7"

  tags = {
    Name        = "Terraform State Bucket"
    Environment = "dev"
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.bucket

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Tabela DynamoDB para controle de locking
resource "aws_dynamodb_table" "terraform_locks" {
  name         = "terraform-locks-dev"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name        = "Terraform Locks Table"
    Environment = "dev"
  }
}


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

module "get_item" {
  source = "./modules/lambda"

  function_name = "get_item"
  role_arn      = aws_iam_role.lambda_role.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = var.lambda_runtime

  filename         = "../dist/get_item_lambda.zip"
  source_code_hash = filebase64sha256("../dist/get_item_lambda.zip")

  memory_size = 256
  timeout     = 15

  environment_variables = {
    DYNAMODB_TABLE_NAME = aws_dynamodb_table.market_list_table.name
  }

  tags = {
    Environment = var.environment
    Function    = "get_item"
  }
}


module "cognito" {
  source         = "./modules/cognito"
  user_pool_name = "user-pool-hello-api-prod"
  client_name    = "hello-api-client"
  domain_prefix  = "hello-terraform-api-auth-v2"
}

module "api_gateway" {
  source = "./modules/api_gateway"

  api_name                        = "hello-terraform-api"
  environment                     = var.environment
  cognito_user_pool_arn           = module.cognito.user_pool_arn
  lambda_invoke_arn               = module.hello_terraform.invoke_arn
  lambda_function_name            = module.hello_terraform.function_name
  api_gateway_cloudwatch_role_arn = aws_iam_role.api_gateway_role.arn
}

module "api_gateway_list" {
  source = "./modules/api_gateway_list"

  api_name                 = "market-list-api"
  region                   = var.region
  function_name            = var.function_name
  http_method              = var.http_method
  environment              = var.environment
  cognito_user_pool_arn    = module.cognito.user_pool_arn
  lambda_invoke_arn_get    = module.get_item.invoke_arn
  lambda_function_arn      = module.get_item.function_arn
  lambda_function_name_get = module.get_item.function_name
}

