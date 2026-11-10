import hashlib
import hmac
import os
import secrets
import time

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Auth Service - Frío Natural")

AUTH_INTROSPECTION_SECRET = os.getenv("AUTH_INTROSPECTION_SECRET")
if not AUTH_INTROSPECTION_SECRET:
    raise RuntimeError("AUTH_INTROSPECTION_SECRET no esta configurado")

SESSION_SECONDS = 900

# Contraseñas guardadas como hash PBKDF2 (formato: algoritmo$iteraciones$sal$hash).
# Claves de laboratorio: ana/1234, ernesto/admin123, matias/1234, christian/1234
USERS = {
    "ana": {
        "user_id": "USR-001",
        "password_hash": "pbkdf2_sha256$200000$a1a1a1a1a1a1a1a1$26b82494a28398c2c652ffaba73c48ff218f6ce249189dda5aec2ff9c51161c5",
        "roles": ["user"],
    },
    "ernesto": {
        "user_id": "USR-003",
        "password_hash": "pbkdf2_sha256$200000$e3e3e3e3e3e3e3e3$c7f994ea36d7ec5fc1484dfbba4b2a86cc97d02dd577ef2c541c9cea120b5b2c",
        "roles": ["user", "admin"],
    },
    "matias": {
        "user_id": "USR-004",
        "password_hash": "pbkdf2_sha256$200000$m4m4m4m4m4m4m4m4$fda52129930020d3709fec3a01cf4f228f8192f845f65c5ca473551a490f35f3",
        "roles": ["user"],
    },
    "christian": {
        "user_id": "USR-005",
        "password_hash": "pbkdf2_sha256$200000$c5c5c5c5c5c5c5c5$b3ba707e7f8ab20b02d9f3c447310aeacb8876ceac02922c75e7eca2b72d9a4c",
        "roles": ["user"],
    },
}

SESSIONS: dict[str, dict] = {}


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenRequest(BaseModel):
    token: str


def verify_password(password: str, stored: str) -> bool:
    _, iterations, salt, expected = stored.split("$")
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), int(iterations)).hex()
    return hmac.compare_digest(digest, expected)


def verify_gateway_secret(received: str):
    if not secrets.compare_digest(received, AUTH_INTROSPECTION_SECRET):
        raise HTTPException(status_code=403, detail="Secreto de Gateway invalido")


@app.get("/health")
def health():
    return {"status": "OK", "service": "Auth Service"}


@app.post("/login")
def login(request: LoginRequest):
    user = USERS.get(request.username)
    # Se verifica siempre un hash para no revelar si el usuario existe por tiempo de respuesta
    stored = user["password_hash"] if user else USERS["ana"]["password_hash"]
    valid = verify_password(request.password, stored)
    if not user or not valid:
        raise HTTPException(status_code=401, detail="Credenciales invalidas")

    token = secrets.token_hex(32)
    SESSIONS[token] = {
        "user_id": user["user_id"],
        "username": request.username,
        "roles": user["roles"],
        "expires_at": time.time() + SESSION_SECONDS,
    }
    return {"access_token": token, "token_type": "bearer", "expires_in": SESSION_SECONDS}


@app.post("/introspect")
def introspect(request: TokenRequest, x_gateway_auth_secret: str = Header(default="")):
    verify_gateway_secret(x_gateway_auth_secret)
    session = SESSIONS.get(request.token)
    if session and session["expires_at"] < time.time():
        SESSIONS.pop(request.token, None)
        session = None
    if session is None:
        return {"active": False}
    return {
        "active": True,
        "user_id": session["user_id"],
        "username": session["username"],
        "roles": session["roles"],
    }


@app.post("/logout")
def logout(request: TokenRequest, x_gateway_auth_secret: str = Header(default="")):
    verify_gateway_secret(x_gateway_auth_secret)
    SESSIONS.pop(request.token, None)
    return {"message": "Sesion cerrada"}
