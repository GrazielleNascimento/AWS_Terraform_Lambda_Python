variable "function_name" {
  description = "Nome da função Lambda"
  type        = string
}

variable "role_arn" {
  description = "ARN do IAM Role para a função Lambda"
  type        = string
}

variable "handler" {
  description = "Handler da função Lambda"
  type        = string
}

variable "runtime" {
  description = "Runtime da função Lambda"
  type        = string
}

variable "filename" {
  description = "Path para o arquivo ZIP da Lambda"
  type        = string
}

variable "memory_size" {
  description = "Memória alocada para a função Lambda (MB)"
  type        = number
  default     = 128
}

variable "timeout" {
  description = "Timeout da função Lambda (segundos)"
  type        = number
  default     = 10
}

variable "source_code_hash" {
  description = "Hash do código fonte para detectar mudanças"
  type        = string
}

variable "environment_variables" {
  description = "Variáveis de ambiente para a função Lambda"
  type        = map(string)
  default     = {}
}

variable "tags" {
  description = "Tags para a função Lambda"
  type        = map(string)
  default     = {}
}