output "api_endpoint" {
  description = "URL do endpoint do API Gateway"
  value       = "${aws_api_gateway_stage.this.invoke_url}/${aws_api_gateway_resource.hello.path_part}"
}

output "api_id" {
  description = "ID do API Gateway"
  value       = aws_api_gateway_rest_api.this.id
}