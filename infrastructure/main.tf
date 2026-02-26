terraform {
  required_providers {
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}

provider "kubernetes" {
  config_path    = "~/.kube/config"
  config_context = "minikube"
}

# RECURSO 1: Namespace
resource "kubernetes_namespace" "boutique" {
  metadata {
    name = var.namespace
    labels = {
      app        = "online-boutique"
      managed-by = "terraform"
    }
  }
}

# RECURSO 2: Deployment
resource "kubernetes_deployment" "recommendation" {
  metadata {
    name      = "recommendationservice"
    namespace = kubernetes_namespace.boutique.metadata[0].name
    labels = {
      app = "recommendationservice"
    }
  }
  spec {
    replicas = var.replicas
    selector {
      match_labels = { app = "recommendationservice" }
    }
    template {
      metadata {
        labels = { app = "recommendationservice" }
      }
      spec {
        container {
          name              = "server"
          image             = "${var.docker_image}:${var.image_tag}"
          image_pull_policy = "Always"
          port { container_port = 8080 }
          env {
            name  = "PORT"
            value = "8080"
          }
          resources {
            requests = { cpu = "100m", memory = "64Mi" }
            limits   = { cpu = "200m", memory = "128Mi" }
          }
          liveness_probe {
            http_get {
              path = "/health"
              port = 8080
            }
            initial_delay_seconds = 10
            period_seconds        = 30
          }
        }
      }
    }
  }
}

# RECURSO 3: Service LoadBalancer
resource "kubernetes_service" "recommendation" {
  metadata {
    name      = "recommendationservice"
    namespace = kubernetes_namespace.boutique.metadata[0].name
  }
  spec {
    selector = { app = "recommendationservice" }
    port {
      port        = 80
      target_port = 8080
    }
    type = "LoadBalancer"
  }
}