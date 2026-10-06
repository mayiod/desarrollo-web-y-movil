import pytest
from fastapi.testclient import TestClient
# Asegúrate de importar tu app desde el archivo real del Auth Service
from auth_service import app 

client = TestClient(app)

# Secreto configurado en Vault para que el Gateway hable con Auth Service
AUTH_SECRET = "gateway-auth-secret-789"

def test_login_valido():
    # Ana existe en la base de datos simulada con clave 1234
    response = client.post("/login", json={"username": "ana", "password": "1234"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalido():
    # Intentar entrar con una clave errónea debe dar 401
    response = client.post("/login", json={"username": "ana", "password": "incorrecta"})
    assert response.status_code == 401

def test_introspection_token_valido():
    # Primero hacemos login para obtener un token real de la sesión
    login_res = client.post("/login", json={"username": "ana", "password": "1234"})
    token = login_res.json()["access_token"]

    # Luego validamos el token en /introspect usando el secreto del Gateway
    headers = {"X-Gateway-Auth-Secret": AUTH_SECRET}
    response = client.post(
        "/introspect", 
        json={"token": token},
        headers=headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["active"] is True
    assert data["username"] == "ana"

def test_introspection_sin_secreto():
    # Si la petición no manda el secreto interno, el Auth Service debe rechazarla
    response = client.post("/introspect", json={"token": "cualquier_token_falso"})
    assert response.status_code == 403