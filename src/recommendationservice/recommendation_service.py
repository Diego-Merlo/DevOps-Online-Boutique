# recommendation_service.py
# Servicio de Recomendaciones — Online Boutique
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Catálogo de productos
PRODUCT_CATALOG = [
    {"id": "OLJCESPC7Z", "name": "Sunglasses",      "price": 19.99, "category": "accessories"},
    {"id": "66VCHSJNUP", "name": "Tank Top",         "price": 18.99, "category": "clothing"},
    {"id": "1YMWWN1N4O", "name": "Watch",            "price": 109.99,"category": "accessories"},
    {"id": "2ZYFJ3GM2N", "name": "Loafers",          "price": 89.99, "category": "footwear"},
    {"id": "0PUK6V6EV0", "name": "Hairdryer",        "price": 24.99, "category": "electronics"},
    {"id": "LS4PSXUNUM", "name": "Metal Mug",        "price": 18.99, "category": "kitchen"},
    {"id": "9SIQT8TOJO", "name": "Bamboo Speakers",  "price": 36.99, "category": "electronics"},
    {"id": "6E92ZMYYFZ", "name": "Backpack",         "price": 56.99, "category": "accessories"},
    {"id": "L9ECAV4NIU", "name": "Ceramic Plate",    "price": 3.99,  "category": "kitchen"},
    {"id": "VJJKEF63SK", "name": "Vintage Shirt",    "price": 12.99, "category": "clothing"},
]

# -------------------------------------------------------
# FUNCIÓN 1: get_recommendations()
# Devuelve productos recomendados excluyendo el actual
# -------------------------------------------------------
def get_recommendations(current_product_id: str, max_results: int = 4) -> list:
    filtered = [p for p in PRODUCT_CATALOG if p["id"] != current_product_id]
    return filtered[:max_results]

# -------------------------------------------------------
# FUNCIÓN 2: filter_by_category()
# Filtra productos por categoría
# -------------------------------------------------------
def filter_by_category(products: list, category: str) -> list:
    result = [p for p in products if p["category"] == category]
    return result if result else products

# -------------------------------------------------------
# FUNCIÓN 3: format_recommendation_response()
# Empaqueta la respuesta en formato estándar
# -------------------------------------------------------
def format_recommendation_response(products: list) -> dict:
    return {
        "total": len(products),
        "recommendations": products
    }

# ========================
# RUTAS
# ========================

@app.route("/")
def index():
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Online Boutique</title>
        <style>
            *{box-sizing:border-box;margin:0;padding:0}
            body{font-family:'Segoe UI',sans-serif;background:#f5f5f5}
            header{background:#1a1a2e;color:white;padding:20px 40px}
            header h1{font-size:24px;letter-spacing:2px}
            header p{color:#aaa;font-size:13px;margin-top:4px}
            .container{max-width:1100px;margin:30px auto;padding:0 20px}
            h2{margin-bottom:20px;color:#333}
            .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:20px}
            .card{background:white;border-radius:10px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,.08);cursor:pointer;transition:transform .2s}
            .card:hover{transform:translateY(-4px)}
            .card h3{font-size:15px;color:#222;margin-bottom:8px}
            .price{color:#e91e63;font-weight:bold}
            .cat{display:inline-block;margin-top:8px;background:#e8f0fe;color:#1a73e8;padding:2px 10px;border-radius:12px;font-size:11px}
            footer{text-align:center;padding:30px;color:#aaa;font-size:12px;margin-top:40px}
        </style>
    </head>
    <body>
        <header>
            <h1>🛍️ ONLINE BOUTIQUE</h1>
            <p>Recommendation Service — Running on Minikube + Terraform</p>
        </header>
        <div class="container">
            <h2>📦 Catálogo de productos</h2>
            <div class="grid">
                {% for p in products %}
                <div class="card" onclick="window.location='/recommend/{{ p.id }}'">
                    <h3>{{ p.name }}</h3>
                    <div class="price">${{ p.price }}</div>
                    <span class="cat">{{ p.category }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
        <footer>Online Boutique · DevOps Project · Flask + Docker + Minikube</footer>
    </body>
    </html>
    """
    return render_template_string(html, products=PRODUCT_CATALOG)

@app.route("/recommend/<product_id>")
def recommend(product_id):
    recs = get_recommendations(product_id)
    current = next((p for p in PRODUCT_CATALOG if p["id"] == product_id), None)
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Recomendaciones - Online Boutique</title>
        <style>
            *{box-sizing:border-box;margin:0;padding:0}
            body{font-family:'Segoe UI',sans-serif;background:#f5f5f5}
            header{background:#1a1a2e;color:white;padding:20px 40px}
            header h1{font-size:24px;letter-spacing:2px}
            .container{max-width:1100px;margin:30px auto;padding:0 20px}
            .current{background:white;border-radius:10px;padding:20px;margin-bottom:30px;border-left:4px solid #e91e63}
            .current small{color:#e91e63;font-size:12px;text-transform:uppercase;letter-spacing:1px}
            .current h3{font-size:22px;margin:8px 0}
            .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:20px}
            .card{background:white;border-radius:10px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,.08)}
            .card h3{font-size:15px;color:#222;margin-bottom:8px}
            .price{color:#e91e63;font-weight:bold}
            .cat{display:inline-block;margin-top:8px;background:#e8f0fe;color:#1a73e8;padding:2px 10px;border-radius:12px;font-size:11px}
            a{color:#1a73e8;text-decoration:none;font-size:14px;display:inline-block;margin-bottom:20px}
            h2{margin-bottom:16px;color:#555}
        </style>
    </head>
    <body>
        <header><h1>🛍️ ONLINE BOUTIQUE</h1></header>
        <div class="container">
            <a href="/">← Volver al catálogo</a>
            {% if current %}
            <div class="current">
                <small>Producto seleccionado</small>
                <h3>{{ current.name }}</h3>
                <p>${{ current.price }} · {{ current.category }}</p>
            </div>
            {% endif %}
            <h2>✨ También te puede interesar ({{ recs|length }} recomendaciones)</h2>
            <div class="grid">
                {% for p in recs %}
                <div class="card">
                    <h3>{{ p.name }}</h3>
                    <div class="price">${{ p.price }}</div>
                    <span class="cat">{{ p.category }}</span>
                </div>
                {% endfor %}
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html, recs=recs, current=current)

@app.route("/api/recommend/<product_id>")
def api_recommend(product_id):
    recs = get_recommendations(product_id)
    return jsonify(format_recommendation_response(recs))

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "recommendationservice"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)