import pytest
from fastapi.testclient import TestClient

from backend_api import app

GW = {"X-Gateway-Secret": "test-backend-secret"}
USER = {**GW, "X-Authenticated-User": "USR-001", "X-Authenticated-Username": "ana", "X-Authenticated-Roles": "user"}
ADMIN = {**GW, "X-Authenticated-User": "USR-003", "X-Authenticated-Username": "ernesto", "X-Authenticated-Roles": "user,admin"}


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_acceso_directo_sin_secreto_es_403(client):
    assert client.get("/products").status_code == 403
    assert client.get("/orders").status_code == 403


def test_secreto_incorrecto_es_403(client):
    assert client.get("/products", headers={"X-Gateway-Secret": "malo"}).status_code == 403


def test_health_es_publico(client):
    assert client.get("/health").status_code == 200


def test_catalogo_tiene_los_11_productos_de_la_pagina(client):
    products = client.get("/products", headers=USER).json()["products"]
    assert len(products) == 11
    cookies = next(p for p in products if p["name"] == "Cookies & Cream")
    assert cookies["price"] == 4500 and cookies["tag"] == "Más Vendido" and cookies["category"] == "helado"


def test_filtro_por_categoria(client):
    helados = client.get("/products?category=helado", headers=USER).json()["products"]
    paletas = client.get("/products?category=paleta", headers=USER).json()["products"]
    assert len(helados) == 6 and len(paletas) == 5


def test_busqueda_por_nombre(client):
    r = client.get("/products?q=mora", headers=USER).json()["products"]
    assert {p["name"] for p in r} == {"Vaso de Helado de Mora", "Paleta de Mora"}


def test_producto_por_id(client):
    assert client.get("/products/1", headers=USER).status_code == 200
    assert client.get("/products/999", headers=USER).status_code == 404


def test_store_info(client):
    info = client.get("/store-info", headers=USER).json()
    assert info["despacho"]["radio_km"] == 15


def test_usuario_no_puede_eliminar(client):
    assert client.delete("/products/11", headers=USER).status_code == 403


def test_admin_elimina_producto_sin_pedidos(client):
    assert client.delete("/products/11", headers=ADMIN).status_code == 200
    assert client.get("/products/11", headers=ADMIN).status_code == 404


def test_no_se_elimina_producto_con_pedidos(client):
    assert client.delete("/products/1", headers=ADMIN).status_code == 409


def test_admin_crea_y_actualiza(client):
    nuevo = {"name": "Vainilla", "category": "helado", "price": 4200}
    r = client.post("/products", json=nuevo, headers=ADMIN)
    assert r.status_code == 201
    pid = r.json()["id"]
    assert client.post("/products", json=nuevo, headers=ADMIN).status_code == 409
    r = client.put(f"/products/{pid}", json={**nuevo, "price": 4300}, headers=ADMIN)
    assert r.json()["price"] == 4300
    assert client.post("/products", json=nuevo, headers=USER).status_code == 403


def test_validacion_de_producto(client):
    malo = {"name": "X", "category": "torta", "price": -5}
    assert client.post("/products", json=malo, headers=ADMIN).status_code == 422


def test_usuario_ve_solo_sus_pedidos(client):
    orders = client.get("/orders", headers=USER).json()["orders"]
    assert len(orders) == 1 and orders[0]["user_id"] == "USR-001"
    assert orders[0]["total"] == 2 * 4500 + 3 * 2500


def test_admin_ve_todos_los_pedidos(client):
    assert len(client.get("/orders", headers=ADMIN).json()["orders"]) == 3


def test_usuario_no_lee_pedido_ajeno(client):
    assert client.get("/orders/2", headers=USER).status_code == 404
    assert client.get("/orders/2", headers=ADMIN).status_code == 200


def test_crear_pedido_calcula_total_en_servidor(client):
    body = {"items": [{"product_id": 8, "quantity": 2}, {"product_id": 3, "quantity": 1}]}
    r = client.post("/orders", json=body, headers=USER)
    assert r.status_code == 201
    assert r.json()["total"] == 2 * 2800 + 4500
    assert r.json()["user_id"] == "USR-001"


def test_pedido_con_producto_inexistente(client):
    body = {"items": [{"product_id": 999, "quantity": 1}]}
    assert client.post("/orders", json=body, headers=USER).status_code == 404
