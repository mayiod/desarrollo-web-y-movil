import os
import secrets
import httpx
from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(
    title="Secure Local API Gateway - Roles",
    description="API Gateway con Vault, Bearer Token y Roles"
)
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

security = HTTPBearer(auto_error=False)

VAULT_ADDR = os.getenv("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:9000")

if not VAULT_TOKEN:
    raise RuntimeError("VAULT_TOKEN no configurado")

AUTH_URL = os.getenv("AUTH_URL", "http://auth-service:8100")

async def get_gateway_secrets():
    url = f"{VAULT_ADDR}/v1/secret/data/gateway"
    headers = {"X-Vault-Token": VAULT_TOKEN}
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(url, headers=headers)
        
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="No fue posible acceder a Vault")
        
    vault_response = response.json()
    return vault_response["data"]["data"]

async def authenticate_client(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        raise HTTPException(status_code=401, detail="Bearer token requerido")
        
    received_token = credentials.credentials

    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            auth_response = await client.post(
                f"{AUTH_URL}/introspect",
                json={"token": received_token}
            )
            auth_data = auth_response.json()
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Auth Service no disponible")

    if not auth_data.get("active"):
        raise HTTPException(status_code=401, detail="Token invalido o expirado")
        
    vault_secrets = await get_gateway_secrets()
    
    roles_usuario = auth_data.get("roles", [])
    role = "administrador" if "admin" in roles_usuario else "usuario"
        
    return {
        "client_id": auth_data.get("username", "cliente-desconocido"),
        "role": role,
        "backend_secret": vault_secrets["backend_shared_secret"]
    }


@app.get("/health")
def health():
    return {"status": "OK", "service": "API Gateway"}

@app.api_route("/auth/{path:path}", methods=["POST", "GET"])
async def auth_proxy(path: str, request: Request):
    target_url = f"{AUTH_URL}/{path}"
    body = await request.body()
    
    headers = {}
    if "content-type" in request.headers:
        headers["content-type"] = request.headers["content-type"]
        
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            upstream = await client.request(
                method=request.method,
                url=target_url,
                content=body,
                headers=headers
            )
    except httpx.RequestError:
        raise HTTPException(status_code=502, detail="Auth Service no disponible")
        
    return Response(
        content=upstream.content,
        status_code=upstream.status_code
    )