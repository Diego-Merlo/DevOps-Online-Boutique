output "namespace" {
  value       = kubernetes_namespace.boutique.metadata[0].name
  description = "Namespace creado en Kubernetes"
}

output "deployment" {
  value       = kubernetes_deployment.recommendation.metadata[0].name
  description = "Nombre del Deployment creado"
}

output "service" {
  value       = kubernetes_service.recommendation.metadata[0].name
  description = "Nombre del Service creado"
}

output "imagen_desplegada" {
  value       = "${var.docker_image}:${var.image_tag}"
  description = "Imagen corriendo en el clúster"
}