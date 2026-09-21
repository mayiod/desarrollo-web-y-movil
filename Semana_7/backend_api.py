from fastapi import FastAPI

app = FastAPI(
    title="Backend API - Frío Natural",
    description="API de negocio de la heladería ubicada en el puerto 9000"
)

@app.get("/health")
def health():
    return {
        "status": "OK",
        "service": "Backend API - Frío Natural"
    }

@app.get("/products")
def products():
    return {
        "products": [
            {"id": 1, "name": "Helado de Lúcuma", "category": "Cremoso", "price": 3500, "stockKg": 45.0},
            {"id": 2, "name": "Helado de Frambuesa", "category": "Frutal", "price": 3000, "stockKg": 30.0},
            {"id": 3, "name": "Helado de Chocolate Belga", "category": "Chocolate", "price": 4000, "stockKg": 25.0}
        ]
    }

@app.get("/orders")
def orders():
    return {
        "orders": [
            {"id": 1001, "flavor": "Helado de Lúcuma", "status": "paid"},
            {"id": 1002, "flavor": "Helado de Frambuesa", "status": "pending"}
        ]
    }
