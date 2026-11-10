"""Flujo completo Gateway -> Auth Service -> Backend, en memoria (sin Vault ni red)."""
import httpx
import pytest
from fastapi.testclient import TestClient

import Semana_14_Entrega_2.backend.auth_service as auth_service
import backend_api
import gateway

VAULT = {"backend_shared_secret": "test-backend-secret", "auth_introspection_secret": "test-auth-secret"}


@pytest.fixture
def gw(monkeypatch):
    destinos = {
        "http://auth.test": TestClient(auth_service.app),
        "http://backend.test": TestClient(backend_api.app),
    }

    class FakeAsyncClient:
        def __init__(self, *a, **k):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def post(self, url, json=None, headers=None):
            return await self.request("POST", url, json=json, headers=headers)

        async def request(self, method, url, params=None, content=None, headers=None, json=None):
            for base, cliente in destinos.items():
                if url.startswith(base):
                    return cliente.request(method, url[len(base):], params=params, content=content, json=json, headers=headers)
            raise httpx.ConnectError("destino desconocido")

    async def fake_vault():
        return VAULT

    monkeypatch.setattr(gateway.httpx, "AsyncClient", FakeAsyncClient)
    monkeypatch.setattr(gateway, "get_vault_secrets", fake_vault)
    with TestClient(gateway.app) as c:
        yield c


def entrar(gw, user, pwd):
    r = gw.post("/auth/login", json={"username": user, "password": pwd})
    assert r.status_code == 200
    return r


def test_sin_cookie_es_401(gw):
    assert gw.get("/api/products").status_code == 401
    assert gw.get("/auth/me").status_code == 401


def test_login_incorrecto_es_401(gw):
    assert gw.post("/auth/login", json={"username": "ana", "password": "mala"}).status_code == 401


def test_login_pone_cookie_httponly_y_no_expone_el_token(gw):
    r = entrar(gw, "ana", "1234")
    cookie = r.headers["set-cookie"].lower()
    assert "session_token=" in cookie and "httponly" in cookie and "samesite=lax" in cookie
    assert "access_token" not in r.json()


def test_usuario_consulta_catalogo_y_pedidos_propios(gw):
    entrar(gw, "ana", "1234")
    assert gw.get("/auth/me").json()["username"] == "ana"
    assert len(gw.get("/api/products").json()["products"]) == 11
    pedidos = gw.get("/api/orders").json()["orders"]
    assert len(pedidos) == 1 and pedidos[0]["user_id"] == "USR-001"


def test_usuario_no_puede_eliminar(gw):
    entrar(gw, "ana", "1234")
    assert gw.delete("/api/products/11").status_code == 403


def test_admin_elimina_y_ve_todos_los_pedidos(gw):
    entrar(gw, "ernesto", "admin123")
    assert gw.delete("/api/products/11").status_code == 200
    assert len(gw.get("/api/orders").json()["orders"]) == 3


def test_cliente_no_puede_falsificar_identidad(gw):
    entrar(gw, "ana", "1234")
    falsos = {"X-Authenticated-Roles": "admin", "X-Authenticated-User": "USR-003"}
    assert gw.delete("/api/products/11", headers=falsos).status_code == 403
    assert all(o["user_id"] == "USR-001" for o in gw.get("/api/orders", headers=falsos).json()["orders"])


def test_logout_revoca_la_sesion(gw):
    entrar(gw, "ana", "1234")
    token = gw.cookies.get("session_token")
    assert gw.post("/auth/logout").status_code == 200
    assert gw.get("/auth/me").status_code == 401
    # aunque alguien conserve el token, el servidor ya lo invalidó
    gw.cookies.set("session_token", token)
    assert gw.get("/api/products").status_code == 401
