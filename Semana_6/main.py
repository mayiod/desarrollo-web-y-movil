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


# Endpoints: Flavors

@app.get("/flavors", response_model=List[FlavorOut])
async def get_flavors(q: Optional[str] = None):
    query = {"name": {"$regex": q, "$options": "i"}} if q else {}
    cursor = col_flavors.find(query)
    results = []
    async for doc in cursor:
        results.append(FlavorOut(
            id=str(doc["_id"]),
            name=doc["name"],
            category=doc["category"],
            price=doc["price"],
            tag=doc.get("tag", ""),
            stockKg=doc["stockKg"]
        ))
    return results

@app.post("/flavors", status_code=201, response_model=FlavorOut)
async def create_flavor(flavor: FlavorIn):
    res = await col_flavors.insert_one(flavor.model_dump())
    doc = await col_flavors.find_one({"_id": res.inserted_id})
    return FlavorOut(
            id=str(doc["_id"]),
            name=doc["name"],
            category=doc["category"],
            price=doc["price"],
            tag=doc.get("tag", ""),
            stockKg=doc["stockKg"]
    )

@app.delete("/delete/{id}", status_code=204)
async def delete_flavor(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID invalido")
    res = await col_flavors.delete_one({"_id": ObjectId(id)})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Sabor no encontrado")
    return None

# Endpoints: Usuarios

@app.get("/usuarios", response_model=List[UsuarioOut])
async def get_usuarios():
    cursor = col_usuarios.find()
    results = []
    async for doc in cursor:
        results.append(UsuarioOut(
            id=str(doc["_id"]),
            nombre=doc["nombre"]
        ))
    return results

@app.post("/usuarios", status_code=201, response_model=UsuarioOut)
async def create_usuario(usuario: UsuarioIn):
    res = await col_usuarios.insert_one(usuario.model_dump(by_alias=True))
    doc = await col_usuarios.find_one({"_id": res.inserted_id})
    return UsuarioOut(
        id=str(doc["_id"]),
        nombre=doc["nombre"]
    )
