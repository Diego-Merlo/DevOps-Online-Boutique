variable "namespace" {
  description = "Namespace de Kubernetes"
  type        = string
  default     = "online-boutique"
}

variable "replicas" {
  description = "Número de réplicas"
  type        = number
  default     = 1
}

variable "docker_image" {
  description = "Imagen Docker del servicio"
  type        = string
}

variable "image_tag" {
  description = "Tag de la imagen"
  type        = string
  default     = "recommendation-latest"
}