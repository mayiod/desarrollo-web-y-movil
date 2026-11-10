import time

import pytest
from fastapi.testclient import TestClient

import Semana_14_Entrega_2.backend.auth_service as auth_service
from Semana_14_Entrega_2.backend.auth_service import app

SECRET = {"X-Gateway-Auth-Secret": "test-auth-secret"}
client = TestClient(app)


def login(username="ana", password="1234"):
    return client.post("/login", json={"username": username, "password": password})


def test_login_valido():
    r = login()
    assert r.status_code == 200
    assert r.json()["token_type"] == "bearer" and r.json()["access_token"]


@pytest.mark.parametrize("user,pwd", [("ana", "incorrecta"), ("noexiste", "1234")])
def test_login_invalido(user, pwd):
    assert login(user, pwd).status_code == 401


def test_introspection_token_valido():
    token = login().json()["access_token"]
    data = client.post("/introspect", json={"token": token}, headers=SECRET).json()
    assert data == {"active": True, "user_id": "USR-001", "username": "ana", "roles": ["user"]}


def test_introspection_admin_tiene_rol_admin():
    token = login("ernesto", "admin123").json()["access_token"]
    assert "admin" in client.post("/introspect", json={"token": token}, headers=SECRET).json()["roles"]


def test_introspection_sin_secreto_es_403():
    assert client.post("/introspect", json={"token": "x"}).status_code == 403


def test_token_inexistente_inactivo():
    assert client.post("/introspect", json={"token": "falso"}, headers=SECRET).json() == {"active": False}


def test_logout_revoca_la_sesion():
    token = login().json()["access_token"]
    assert client.post("/logout", json={"token": token}, headers=SECRET).status_code == 200
    assert client.post("/introspect", json={"token": token}, headers=SECRET).json()["active"] is False


def test_logout_sin_secreto_es_403():
    assert client.post("/logout", json={"token": "x"}).status_code == 403


def test_token_expirado_queda_inactivo():
    token = login().json()["access_token"]
    auth_service.SESSIONS[token]["expires_at"] = time.time() - 1
    assert client.post("/introspect", json={"token": token}, headers=SECRET).json()["active"] is False
