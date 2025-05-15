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