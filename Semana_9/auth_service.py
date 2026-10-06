from fastapi import (
    FastAPI,
    Header,
    HTTPException,
    Depends
)
from pydantic import BaseModel
import secrets

app = FastAPI()

USERS = {
        "ana" : {
            "user_id": "USR-001",
            "password" : "...",
            "roles" : ["user"]
        },
        "ernesto" : {
            "user_id": "USR-003",
            "password" : "...",
            "roles" : ["user", "admin"]
        },
        "matias" : {
            "user_id": "USR-004",
            "password" : "...",
            "roles" : ["user"]
        },
        "christian" : {
            "user_id": "USR-005",
            "password" : "...",
            "roles" : ["user"]
        }
}

SESSIONS = {}

class LoginRequest(BaseModel):
    username: str
    password: str   

class IntrospectionRequest(BaseModel):
    token: str

@app.post("/login")
def login(request: LoginRequest):
    user = USERS.get(request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(
            status_code=401,
            detail="No autorizado"
        )

    access_token = secrets.token_hex(16)

    SESSIONS[access_token] = {
        "user_id": user["user_id"],
        "username": request.username,
        "roles": user["roles"],
        "active": True  
    }

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 900
    }   

@app.post("/introspect")
def introspect(request: IntrospectionRequest):
    session = SESSIONS.get(request.token)
    if not session or not session.get("active"):
        return {"active": False}

    return {
        "active": True,
        "user_id": session["user_id"],
        "username": session["username"],
        "roles": session["roles"]
    }

@app.post("/logout")
def logout(request: IntrospectionRequest):
    if request.token in SESSIONS:
        SESSIONS.pop(request.token)
    return {"message": "Sesión cerrada exitosamente"}

@app.get("/health")
def health():
    return {"status": "OK, Todo bien!"}


