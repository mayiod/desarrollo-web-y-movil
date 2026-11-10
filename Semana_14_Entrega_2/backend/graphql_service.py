import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi import FastAPI, Request, HTTPException
import httpx
from typing import List, Optional
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-api:9000/api")

@strawberry.type
class Product:
    id: int
    name: str
    price: int
    category: str

@strawberry.type
class OrderDetail:
    id: int
    flavor_id: int
    cantidad: int
    precio_unitario: int
    product: Optional[Product]

@strawberry.type
class OrderSummary:
    id: int
    user_id: int
    total: int
    estado: str
    detalles: List[OrderDetail]

@strawberry.type
class Query:
    @strawberry.field
    async def order_summary(self, id: int, info: strawberry.Info) -> OrderSummary:
        request: Request = info.context["request"]
        
        x_user = request.headers.get("X-Authenticated-User")
        x_secret = request.headers.get("X-Gateway-Secret")
        
        if not x_secret:
            raise HTTPException(status_code=403, detail="Acceso denegado. Se requiere pasar por el API Gateway.")

        headers = {
            "X-Authenticated-User": str(x_user) if x_user else "",
            "X-Gateway-Secret": x_secret
        }

        async with httpx.AsyncClient() as client:
            # 1. Consultar el pedido
            order_res = await client.get(f"{BACKEND_URL}/orders/{id}", headers=headers)
            if order_res.status_code != 200:
                raise HTTPException(status_code=order_res.status_code, detail="Pedido no encontrado o sin permisos")
            order_data = order_res.json()

            detalles_agregados = []
            
            # 2. Consultar el producto por cada detalle del pedido
            for item in order_data.get("items", []):
                flavor_id = item.get("product_id")
                prod_res = await client.get(f"{BACKEND_URL}/products/{flavor_id}", headers=headers)
                
                product_obj = None
                if prod_res.status_code == 200:
                    prod_data = prod_res.json()
                    product_obj = Product(
                        id=prod_data["id"],
                        name=prod_data["name"],
                        price=prod_data["price"],
                        category=prod_data["category"]
                    )

                detalles_agregados.append(OrderDetail(
                    id=item.get("id", 0),
                    flavor_id=flavor_id,
                    cantidad=item.get("quantity", 0),
                    precio_unitario=item.get("unit_price", 0),
                    product=product_obj
                ))

            return OrderSummary(
                id=order_data["id"],
                user_id=order_data["user_id"],
                total=order_data["total"],
                estado=order_data["estado"],
                detalles=detalles_agregados
            )

schema = strawberry.Schema(query=Query)

async def get_context(request: Request):
    return {"request": request}

graphql_app = GraphQLRouter(schema, context_getter=get_context)
app = FastAPI(title="GraphQL Gateway")
app.include_router(graphql_app, prefix="/graphql")