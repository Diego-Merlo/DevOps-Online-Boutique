FROM python:3.11-slim

LABEL maintainer="equipo-devops"
LABEL version="1.0.0"
LABEL description="Online Boutique - Recommendation Service"

WORKDIR /app

# Copiar requirements primero para aprovechar caché de capas de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1

CMD ["python", "recommendation_service.py"]