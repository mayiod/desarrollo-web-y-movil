from fastapi import FastAPI
import httpx

app = FastAPI(title="Local API Gateway")
BACKEND_URL = "http://192.168.1.20:9000"

@app.get("/api/products")
async def products():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BACKEND_URL}/products")
    return r.json()

@app.get("/api/orders")
async def orders():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{BACKEND_URL}/orders")
    return r.json()