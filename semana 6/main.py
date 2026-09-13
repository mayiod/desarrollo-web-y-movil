from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from contextlib import asynccontextmanager
from typing import List, Optional

# Conexión a MongoDB 
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "frio_natural"

client = None
db = None
col_flavors = None
col_usuarios = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global client, db, col_flavors, col_usuarios
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    col_flavors = db["flavors"]
    col_usuarios = db["usuarios"]
    yield
    client.close()

app = FastAPI(
    title="Frío Natural - API REST FastAPI",
    version="1.0.0",
    lifespan=lifespan
)

# ==================== MODELOS (Pydantic) ====================

class FlavorIn(BaseModel):
    name: str = Field(..., min_length=1)
    category: str
    price: float = Field(..., gt=0)
    tag: Optional[str] = ""
    stockKg: float = Field(..., ge=0)

class FlavorOut(FlavorIn):
    id: str

class UsuarioIn(BaseModel):
    nombre: str = Field(..., min_length=1)
    pass_: str = Field(..., alias="pass")

class UsuarioOut(BaseModel):
    id: str
    nombre: str

