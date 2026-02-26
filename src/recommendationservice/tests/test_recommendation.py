# test_recommendation.py — Pruebas Unitarias con PyTest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from recommendation_service import (
    get_recommendations,
    filter_by_category,
    format_recommendation_response
)

SAMPLE_PRODUCTS = [
    {"id": "AAA", "name": "Prod A", "price": 10.0, "category": "clothing"},
    {"id": "BBB", "name": "Prod B", "price": 20.0, "category": "electronics"},
    {"id": "CCC", "name": "Prod C", "price": 30.0, "category": "clothing"},
    {"id": "DDD", "name": "Prod D", "price": 40.0, "category": "accessories"},
]

# --- FUNCIÓN 1: get_recommendations ---

def test_recommendations_devuelve_lista():
    result = get_recommendations("OLJCESPC7Z")
    assert isinstance(result, list)

def test_recommendations_excluye_producto_actual():
    result = get_recommendations("OLJCESPC7Z")
    ids = [p["id"] for p in result]
    assert "OLJCESPC7Z" not in ids

def test_recommendations_respeta_limite():
    result = get_recommendations("AAA", max_results=3)
    assert len(result) <= 3

# --- FUNCIÓN 2: filter_by_category ---

def test_filter_retorna_categoria_correcta():
    result = filter_by_category(SAMPLE_PRODUCTS, "clothing")
    for p in result:
        assert p["category"] == "clothing"

def test_filter_categoria_inexistente_retorna_todos():
    result = filter_by_category(SAMPLE_PRODUCTS, "no_existe")
    assert result == SAMPLE_PRODUCTS

# --- FUNCIÓN 3: format_recommendation_response ---

def test_formato_tiene_campo_total():
    response = format_recommendation_response(SAMPLE_PRODUCTS)
    assert "total" in response

def test_formato_total_es_correcto():
    response = format_recommendation_response(SAMPLE_PRODUCTS)
    assert response["total"] == len(SAMPLE_PRODUCTS)

def test_formato_tiene_campo_recommendations():
    response = format_recommendation_response(SAMPLE_PRODUCTS)
    assert "recommendations" in response