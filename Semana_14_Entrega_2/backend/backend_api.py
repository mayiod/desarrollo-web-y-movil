import os
import secrets
import sqlite3
from contextlib import asynccontextmanager
import grpc
import analytics_pb2
import analytics_pb2_grpc
from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

import database

INTERNAL_GATEWAY_SECRET = os.getenv("INTERNAL_GATEWAY_SECRET")
if not INTERNAL_GATEWAY_SECRET:
    raise RuntimeError("INTERNAL_GATEWAY_SECRET no esta configurado")


@asynccontextmanager
async def lifespan(_: FastAPI):
    database.init_db()
    yield


app = FastAPI(title="Backend API - Frío Natural", lifespan=lifespan)


# ---------- Seguridad ----------
def verify_gateway(x_gateway_secret: str = Header(default="")):
    if not secrets.compare_digest(x_gateway_secret, INTERNAL_GATEWAY_SECRET):
        raise HTTPException(status_code=403, detail="Solicitud no autorizada desde Gateway")


class Identity(BaseModel):
    user_id: str = ""
    username: str = ""
    roles: list[str] = []

    @property
    def is_admin(self) -> bool:
        return "admin" in self.roles


def get_identity(
    x_authenticated_user: str = Header(default=""),
    x_authenticated_username: str = Header(default=""),
    x_authenticated_roles: str = Header(default=""),
) -> Identity:
    roles = [r for r in x_authenticated_roles.split(",") if r]
    return Identity(user_id=x_authenticated_user, username=x_authenticated_username, roles=roles)


def require_admin(identity: Identity = Depends(get_identity)) -> Identity:
    if not identity.is_admin:
        raise HTTPException(status_code=403, detail="Se requiere rol administrador")
    return identity


# ---------- Modelos ----------
class ProductIn(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    category: str = Field(pattern="^(helado|paleta)$")
    price: int = Field(ge=0)
    tag: str = ""
    stock_kg: float = Field(default=0, ge=0)
    image: str = ""
    alt: str = ""
    visible_inicial: bool = True


class OrderItemIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, le=100)


class OrderIn(BaseModel):
    items: list[OrderItemIn] = Field(min_length=1)


def product_row(row: sqlite3.Row) -> dict:
    d = dict(row)
    d["visible_inicial"] = bool(d["visible_inicial"])
    return d


def get_order(conn: sqlite3.Connection, order_id: int) -> dict | None:
    pedido = conn.execute("SELECT * FROM pedidos WHERE id = ?", (order_id,)).fetchone()
    if pedido is None:
        return None
    lineas = conn.execute(
        "SELECT d.flavor_id AS product_id, f.name, d.cantidad AS quantity, d.precio_unitario AS unit_price "
        "FROM detalle_pedido d JOIN flavors f ON f.id = d.flavor_id WHERE d.pedido_id = ?",
        (order_id,),
    ).fetchall()
    return {**dict(pedido), "items": [dict(l) for l in lineas]}


# ---------- Endpoints ----------
@app.get("/health")
def health():
    return {"status": "OK", "service": "Backend API"}


@app.get("/store-info", dependencies=[Depends(verify_gateway)])
def store_info():
    return database.load_json("empresa.json")


@app.get("/products", dependencies=[Depends(verify_gateway)])
def list_products(category: str | None = None, q: str | None = None):
    sql, params = "SELECT * FROM flavors WHERE 1=1", []
    if category:
        sql += " AND category = ?"
        params.append(category)
    if q:
        sql += " AND LOWER(name) LIKE ?"
        params.append(f"%{q.lower()}%")
    with database.get_conn() as conn:
        rows = conn.execute(sql + " ORDER BY id", params).fetchall()
    return {"products": [product_row(r) for r in rows]}


@app.get("/products/{product_id}", dependencies=[Depends(verify_gateway)])
def get_product(product_id: int):
    with database.get_conn() as conn:
        row = conn.execute("SELECT * FROM flavors WHERE id = ?", (product_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product_row(row)


@app.post("/products", status_code=201, dependencies=[Depends(verify_gateway), Depends(require_admin)])
def create_product(product: ProductIn):
    try:
        with database.get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO flavors (name, category, price, tag, stock_kg, image, alt, visible_inicial) "
                "VALUES (:name, :category, :price, :tag, :stock_kg, :image, :alt, :visible_inicial)",
                product.model_dump(),
            )
            row = conn.execute("SELECT * FROM flavors WHERE id = ?", (cur.lastrowid,)).fetchone()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Ya existe un producto con ese nombre")
    return product_row(row)


@app.put("/products/{product_id}", dependencies=[Depends(verify_gateway), Depends(require_admin)])
def update_product(product_id: int, product: ProductIn):
    try:
        with database.get_conn() as conn:
            cur = conn.execute(
                "UPDATE flavors SET name=:name, category=:category, price=:price, tag=:tag, "
                "stock_kg=:stock_kg, image=:image, alt=:alt, visible_inicial=:visible_inicial WHERE id=:id",
                {**product.model_dump(), "id": product_id},
            )
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            row = conn.execute("SELECT * FROM flavors WHERE id = ?", (product_id,)).fetchone()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Ya existe un producto con ese nombre")
    return product_row(row)


@app.delete("/products/{product_id}", dependencies=[Depends(verify_gateway), Depends(require_admin)])
def delete_product(product_id: int):
    try:
        with database.get_conn() as conn:
            cur = conn.execute("DELETE FROM flavors WHERE id = ?", (product_id,))
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="El producto tiene pedidos asociados y no puede eliminarse")
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": f"Producto {product_id} eliminado"}


@app.get("/orders", dependencies=[Depends(verify_gateway)])
def list_orders(identity: Identity = Depends(get_identity)):
    with database.get_conn() as conn:
        if identity.is_admin:
            ids = conn.execute("SELECT id FROM pedidos ORDER BY id").fetchall()
        else:
            ids = conn.execute("SELECT id FROM pedidos WHERE user_id = ? ORDER BY id", (identity.user_id,)).fetchall()
        orders = [get_order(conn, r["id"]) for r in ids]
    return {"orders": orders}


@app.get("/orders/{order_id}", dependencies=[Depends(verify_gateway)])
def read_order(order_id: int, identity: Identity = Depends(get_identity)):
    with database.get_conn() as conn:
        order = get_order(conn, order_id)
    # Un usuario normal no puede distinguir "no existe" de "no es mío"
    if order is None or (not identity.is_admin and order["user_id"] != identity.user_id):
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return order


@app.post("/orders", status_code=201, dependencies=[Depends(verify_gateway)])
def create_order(order: OrderIn, identity: Identity = Depends(get_identity)):
    """Convierte el carrito en un pedido. El precio sale de la base, nunca del cliente."""
    if not identity.user_id:
        raise HTTPException(status_code=401, detail="Identidad no propagada")
    with database.get_conn() as conn:
        lineas, total = [], 0
        for item in order.items:
            row = conn.execute("SELECT id, price FROM flavors WHERE id = ?", (item.product_id,)).fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail=f"Producto {item.product_id} no existe")
            lineas.append((row["id"], item.quantity, row["price"]))
            total += row["price"] * item.quantity
        cur = conn.execute(
            "INSERT INTO pedidos (user_id, total, fecha, estado) VALUES (?, ?, datetime('now'), 'pendiente')",
            (identity.user_id, total),
        )
        for flavor_id, qty, price in lineas:
            conn.execute(
                "INSERT INTO detalle_pedido (pedido_id, flavor_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                (cur.lastrowid, flavor_id, qty, price),
            )
        return get_order(conn, cur.lastrowid)

@app.post("/payments/{order_id}", dependencies=[Depends(verify_gateway)])

def process_payment(order_id: int, identity: Identity = Depends(get_identity)):
    """Simula el sistema payments autorizando el cambio de estado del pedido."""
    if not identity.user_id:
        raise HTTPException(status_code=401, detail="Identidad no propagada")

    with database.get_conn() as conn:
        order = get_order(conn, order_id)

        if order is None or (not identity.is_admin and order["user_id"] != identity.user_id):
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
        if order["estado"] == "pagado":
            raise HTTPException(status_code=409, detail="El pedido ya se encuentra pagado")

        conn.execute("UPDATE pedidos SET estado = 'pagado' WHERE id = ?", (order_id,))
        updated_order = get_order(conn, order_id)

        # Notificar asíncronamente al servicio de analítica
        try:
            grpc_host = os.getenv("GRPC_ANALYTICS_HOST", "localhost:50051")
            with grpc.insecure_channel(grpc_host) as channel:
                stub = analytics_pb2_grpc.AnalyticsServiceStub(channel)
                stub.LogSale(
                    analytics_pb2.SaleRequest(order_id=updated_order["id"], total=updated_order["total"]), 
                    timeout=2
                )
        except Exception as e:
            print(f"Aviso: No se pudo contactar al servicio de analítica gRPC: {e}")    
        
    return {"message": "Pago procesado exitosamente", "order": updated_order}