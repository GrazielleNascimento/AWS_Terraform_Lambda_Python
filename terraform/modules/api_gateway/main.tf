resource "aws_api_gateway_rest_api" "this" {
  name        = var.api_name
  description = "API Gateway para Hello Terraform com autenticação Cognito"
}

resource "aws_api_gateway_resource" "hello" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  parent_id   = aws_api_gateway_rest_api.this.root_resource_id
  path_part   = "hello"
}

# Método GET para /hello
resource "aws_api_gateway_method" "get_hello" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  resource_id   = aws_api_gateway_resource.hello.id
  http_method   = "GET"
  authorization = "COGNITO_USER_POOLS"
  authorizer_id = aws_api_gateway_authorizer.cognito.id
}


resource "aws_api_gateway_integration" "get_hello_integration" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  resource_id = aws_api_gateway_resource.hello.id
  http_method = aws_api_gateway_method.get_hello.http_method
  
  integration_http_method = "POST"  
  type                    = "AWS_PROXY"
  uri                     = var.lambda_invoke_arn
}

# Adiciona método response
resource "aws_api_gateway_method_response" "get_hello_response_200" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  resource_id = aws_api_gateway_resource.hello.id
  http_method = aws_api_gateway_method.get_hello.http_method
  status_code = "200"

  response_models = {
    "application/json" = "Empty"
  }

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = false
  }
}

#  Adiciona integration response
resource "aws_api_gateway_integration_response" "get_hello_integration_response" {
  rest_api_id = aws_api_gateway_rest_api.this.id
  resource_id = aws_api_gateway_resource.hello.id
  http_method = aws_api_gateway_method.get_hello.http_method
  status_code = aws_api_gateway_method_response.get_hello_response_200.status_code

  response_parameters = {
    "method.response.header.Access-Control-Allow-Origin" = "'*'"
  }

  depends_on = [aws_api_gateway_integration.get_hello_integration]
}

# Permissão Lambda específica
resource "aws_lambda_permission" "api_gateway_lambda" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "apigateway.amazonaws.com"
  
  # Mais específico para o método GET em /hello
  source_arn = "${aws_api_gateway_rest_api.this.execution_arn}/*/GET/hello"
}

# Authorizer Cognito
resource "aws_api_gateway_authorizer" "cognito" {
  name                   = "${var.api_name}-cognito-authorizer"
  rest_api_id           = aws_api_gateway_rest_api.this.id
  type                  = "COGNITO_USER_POOLS"
  provider_arns         = [var.cognito_user_pool_arn]
  identity_source       = "method.request.header.Authorization"
}

# Deploy do API Gateway
resource "aws_api_gateway_deployment" "this" {
  rest_api_id = aws_api_gateway_rest_api.this.id

  depends_on = [
    aws_api_gateway_method.get_hello,
    aws_api_gateway_integration.get_hello_integration,
    aws_api_gateway_method_response.get_hello_response_200,
    aws_api_gateway_integration_response.get_hello_integration_response
  ]

  lifecycle {
    create_before_destroy = true
  }
  
  
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.hello.id,
      aws_api_gateway_method.get_hello.id,
      aws_api_gateway_integration.get_hello_integration.id,
    ]))
  }
}

# Stage do API Gateway
resource "aws_api_gateway_stage" "this" {
  rest_api_id   = aws_api_gateway_rest_api.this.id
  deployment_id = aws_api_gateway_deployment.this.id
  stage_name    = var.environment
  
  # Habilita logs para debug
  xray_tracing_enabled = true
  
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip            = "$context.identity.sourceIp"
      caller        = "$context.identity.caller"
      user          = "$context.identity.user"
      requestTime   = "$context.requestTime"
      httpMethod    = "$context.httpMethod"
      resourcePath  = "$context.resourcePath"
      status        = "$context.status"
      protocol      = "$context.protocol"
      responseLength = "$context.responseLength"
      error         = "$context.error.message"
      integrationError = "$context.integrationErrorMessage"
    })
  }
}

# CloudWatch Log Group para API Gateway
resource "aws_cloudwatch_log_group" "api_gateway" {
  name              = "/aws/apigateway/${var.api_name}"
  retention_in_days = 7
}

#  Configurar API Gateway Account 
resource "aws_api_gateway_account" "this" {
  cloudwatch_role_arn = var.api_gateway_cloudwatch_role_arn
}