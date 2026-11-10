import os

import httpx
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse

app = FastAPI(title="API Gateway - Frío Natural")

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:9000")
AUTH_URL = os.getenv("AUTH_URL", "http://127.0.0.1:8100")
GRAPHQL_URL = os.getenv("GRAPHQL_URL", "http://graphql-service:8050/graphql")
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"  # true cuando haya HTTPS

if not VAULT_TOKEN:
    raise RuntimeError("VAULT_TOKEN no configurado")

COOKIE_NAME = "session_token"


# ---------- Vault ----------
async def get_vault_secrets() -> dict:
    url = f"{VAULT_ADDR}/v1/secret/data/gateway"
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url, headers={"X-Vault-Token": VAULT_TOKEN})
    except httpx.RequestError:
        raise HTTPException(status_code=500, detail="No fue posible acceder a Vault")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="No fue posible acceder a Vault")
    return response.json()["data"]["data"]


# ---------- Auth Service ----------
async def call_auth(path: str, payload: dict, secret: str | None = None) -> httpx.Response:
    headers = {"X-Gateway-Auth-Secret": secret} if secret else {}
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            return await client.post(f"{AUTH_URL}/{path}", json=payload, headers=headers)
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="Auth Service no disponible")


async def get_session(request: Request) -> dict:
    """Valida la cookie contra el Auth Service. Devuelve identidad + secretos."""
    token = request.cookies.get(COOKIE_NAME)
    if not token:
        raise HTTPException(status_code=401, detail="Sesion requerida")

    vault = await get_vault_secrets()
    response = await call_auth("introspect", {"token": token}, vault["auth_introspection_secret"])
    if response.status_code != 200:
        raise HTTPException(status_code=503, detail="Auth Service respondio con error")
    data = response.json()
    if not data.get("active"):
        raise HTTPException(status_code=401, detail="Sesion invalida o expirada")

    return {
        "token": token,
        "user_id": data["user_id"],
        "username": data["username"],
        "roles": data["roles"],
        "backend_secret": vault["backend_shared_secret"],
        "auth_secret": vault["auth_introspection_secret"],
    }


# ---------- Autorización ----------
def authorize(method: str, path: str, roles: list[str]):
    """Escribir/modificar/eliminar productos es solo para administradores."""
    recurso = path.strip("/").split("/")[0]
    if recurso == "products" and method != "GET" and "admin" not in roles:
        raise HTTPException(status_code=403, detail="Se requiere rol administrador")


# ---------- Endpoints propios ----------
@app.get("/health")
def health():
    return {"status": "OK", "service": "API Gateway"}


@app.post("/auth/login")
async def login(request: Request):
    body = await request.json()
    response = await call_auth("login", body)
    if response.status_code != 200:
        return JSONResponse(status_code=response.status_code, content=response.json())

    data = response.json()
    # El token NO se devuelve en el cuerpo: viaja solo en la cookie HttpOnly
    result = JSONResponse({"message": "Login exitoso", "expires_in": data["expires_in"]})
    result.set_cookie(
        COOKIE_NAME,
        data["access_token"],
        max_age=data["expires_in"],
        httponly=True,
        samesite="lax",
        secure=COOKIE_SECURE,
    )
    return result


@app.get("/auth/me")
async def me(request: Request):
    session = await get_session(request)
    return {"user_id": session["user_id"], "username": session["username"], "roles": session["roles"]}


@app.post("/auth/logout")
async def logout(request: Request):
    token = request.cookies.get(COOKIE_NAME)
    if token:
        vault = await get_vault_secrets()
        await call_auth("logout", {"token": token}, vault["auth_introspection_secret"])
    result = JSONResponse({"message": "Sesion cerrada"})
    result.delete_cookie(COOKIE_NAME)
    return result

# ---------- Proxy hacia GraphQL ----------
@app.api_route("/graphql", methods=["GET", "POST"])
async def graphql_proxy(request: Request):
    # Validar sesión
    session = await get_session(request)

    headers = {
        "X-Gateway-Secret": session["backend_secret"],
        "X-Authenticated-User": session["user_id"],
        "X-Authenticated-Username": session["username"],
        "X-Authenticated-Roles": ",".join(session["roles"]),
    }
    if "content-type" in request.headers:
        headers["content-type"] = request.headers["content-type"]

    # Redirigir al servicio GraphQL privado
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            upstream = await client.request(
                method=request.method,
                url=GRAPHQL_URL,
                params=request.query_params,
                content=await request.body(),
                headers=headers,
            )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Servicio GraphQL no disponible")

    media = upstream.headers.get("content-type")
    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers={"content-type": media} if media else {},
    )

# ---------- Proxy hacia el backend ----------
@app.api_route("/api/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy(path: str, request: Request):
    session = await get_session(request)
    authorize(request.method, path, session["roles"])

    # Se construyen headers nuevos: los X-Authenticated-* que envíe el cliente nunca pasan
    headers = {
        "X-Gateway-Secret": session["backend_secret"],
        "X-Authenticated-User": session["user_id"],
        "X-Authenticated-Username": session["username"],
        "X-Authenticated-Roles": ",".join(session["roles"]),
    }
    if "content-type" in request.headers:
        headers["content-type"] = request.headers["content-type"]

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            upstream = await client.request(
                method=request.method,
                url=f"{BACKEND_URL}/{path}",
                params=request.query_params,
                content=await request.body(),
                headers=headers,
            )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Backend no disponible")

    media = upstream.headers.get("content-type")
    return Response(
        content=upstream.content,
        status_code=upstream.status_code,
        headers={"content-type": media} if media else {},
    )
