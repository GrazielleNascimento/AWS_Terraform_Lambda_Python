output "api_invoke_url" {
  value = "https://${aws_api_gateway_rest_api.api_gateway_list.id}.execute-api.${var.region}.amazonaws.com/${aws_api_gateway_stage.dev.stage_name}"
}


output "lambda_invoke_arn" {
  value = var.lambda_invoke_arn_get
}

