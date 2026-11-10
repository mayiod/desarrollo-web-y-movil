"""Base de datos SQLite de Frío Natural.

Modelo basado en el diagrama entidad-relación de la Semana 4:
FLAVORS (productos) -> DETALLE_PEDIDO <- PEDIDOS.
La tabla USUARIOS vive en el Auth Service, no aquí.
"""
import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = os.getenv("DB_PATH", str(BASE_DIR / "data" / "frio_natural.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS flavors (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL UNIQUE,
    category        TEXT NOT NULL CHECK (category IN ('helado', 'paleta')),
    price           INTEGER NOT NULL CHECK (price >= 0),
    tag             TEXT NOT NULL DEFAULT '',
    stock_kg        REAL NOT NULL DEFAULT 0,
    image           TEXT NOT NULL DEFAULT '',
    alt             TEXT NOT NULL DEFAULT '',
    visible_inicial INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS pedidos (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    total   INTEGER NOT NULL,
    fecha   TEXT NOT NULL,
    estado  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS detalle_pedido (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id       INTEGER NOT NULL REFERENCES pedidos(id) ON DELETE CASCADE,
    flavor_id       INTEGER NOT NULL REFERENCES flavors(id),
    cantidad        INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario INTEGER NOT NULL
);
"""

# Pedidos simulados de ejemplo: (user_id, fecha, estado, [(flavor_id, cantidad), ...])
SEED_PEDIDOS = [
    ("USR-001", "2026-10-01T14:30:00", "pagado", [(1, 2), (7, 3)]),
    ("USR-004", "2026-10-02T19:10:00", "pendiente", [(3, 1), (8, 2)]),
    ("USR-005", "2026-10-03T13:45:00", "pagado", [(6, 1)]),
]


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def load_json(nombre: str):
    with open(BASE_DIR / "data" / nombre, encoding="utf-8") as f:
        return json.load(f)


def init_db():
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    with get_conn() as conn:
        conn.executescript(SCHEMA)
        if conn.execute("SELECT COUNT(*) FROM flavors").fetchone()[0] > 0:
            return
        for p in load_json("productos.json"):
            conn.execute(
                "INSERT INTO flavors (name, category, price, tag, stock_kg, image, alt, visible_inicial) "
                "VALUES (:name, :category, :price, :tag, :stock_kg, :image, :alt, :visible_inicial)",
                p,
            )
        for user_id, fecha, estado, items in SEED_PEDIDOS:
            total = 0
            lineas = []
            for flavor_id, cantidad in items:
                precio = conn.execute("SELECT price FROM flavors WHERE id = ?", (flavor_id,)).fetchone()[0]
                total += precio * cantidad
                lineas.append((flavor_id, cantidad, precio))
            cur = conn.execute(
                "INSERT INTO pedidos (user_id, total, fecha, estado) VALUES (?, ?, ?, ?)",
                (user_id, total, fecha, estado),
            )
            for flavor_id, cantidad, precio in lineas:
                conn.execute(
                    "INSERT INTO detalle_pedido (pedido_id, flavor_id, cantidad, precio_unitario) VALUES (?, ?, ?, ?)",
                    (cur.lastrowid, flavor_id, cantidad, precio),
                )


def reset_db():
    """Borra el archivo y vuelve a sembrar los datos (útil en pruebas)."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()
