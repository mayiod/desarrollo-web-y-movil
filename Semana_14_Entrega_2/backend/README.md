# Backend Frío Natural (Entrega 2)

Backend con los datos de la página simulada (Semana 7 Entrega 1): 11 productos (6 helados, 5 paletas), datos de la empresa y pedidos. **No está integrado al frontend todavía.**

## Arquitectura

```
Cliente --cookie--> API Gateway :8000 --> Auth Service :8100  (login, introspect, logout)
                         |--> Vault :8200                       (secretos)
                         '--> Backend API :9000 --> SQLite      (productos, pedidos)
```

| Archivo | Rol |
|---|---|
| `auth_service.py` | Usuarios (hash PBKDF2), sesiones de 15 min, introspección, logout |
| `gateway.py` | Valida cookie `HttpOnly`, autoriza por rol, propaga identidad al backend |
| `backend_api.py` | Lógica de negocio y datos |
| `database.py` | SQLite según el diagrama ER de la Semana 4 (`flavors`, `pedidos`, `detalle_pedido`) |
| `data/productos.json` | Productos tal como aparecen en la página |
| `data/empresa.json` | Contacto, despacho y reembolsos (páginas legales) |

## Ejecutar

```
docker compose up --build
```

Vault y sus secretos se cargan solos (`vault-init`). Los valores de laboratorio están en `.env.example`.

## Usuarios de prueba

| Usuario | Clave | Roles |
|---|---|---|
| ana | 1234 | user |
| matias | 1234 | user |
| christian | 1234 | user |
| ernesto | admin123 | user, admin |

## Endpoints (todos bajo `/api`, requieren sesión)

| Método | Ruta | Quién |
|---|---|---|
| GET | `/api/products?category=helado&q=mora` | autenticado |
| GET | `/api/products/{id}` | autenticado |
| POST / PUT / DELETE | `/api/products[/{id}]` | solo admin |
| GET | `/api/orders` | user: los suyos · admin: todos |
| GET | `/api/orders/{id}` | dueño o admin |
| POST | `/api/orders` | autenticado (`{"items":[{"product_id":1,"quantity":2}]}`) |
| GET | `/api/store-info` | autenticado |

Auth: `POST /auth/login`, `GET /auth/me`, `POST /auth/logout`.

## Prueba manual

```
curl -i http://localhost:9000/products                                  # 403 (bypass bloqueado)
curl -i -c c.txt -X POST localhost:8000/auth/login -H "Content-Type: application/json" -d '{"username":"ana","password":"1234"}'
curl -b c.txt localhost:8000/api/products                               # 200
curl -i -b c.txt -X DELETE localhost:8000/api/products/11               # 403 (ana no es admin)
curl -i -c e.txt -X POST localhost:8000/auth/login -H "Content-Type: application/json" -d '{"username":"ernesto","password":"admin123"}'
curl -i -b e.txt -X DELETE localhost:8000/api/products/11               # 200
curl -b e.txt -X POST localhost:8000/auth/logout
curl -i -b e.txt localhost:8000/auth/me                                 # 401
```

En PowerShell usa `curl.exe`. También sirve la documentación automática en `http://localhost:9000/docs` (backend) y `:8100/docs` (auth).

## Pruebas automatizadas

```
pip install -r requirements-dev.txt
pytest -q
```

36 pruebas: backend (secreto, catálogo, roles, pedidos), auth (login, expiración, revocación) y flujo completo Gateway → Auth → Backend.

## Notas

- `stock_kg` y los pedidos de ejemplo son datos simulados (el diagrama ER pide stock; la página no lo muestra).
- Un producto con pedidos asociados no se puede eliminar (409).
- Pendiente para producción: HTTPS (`COOKIE_SECURE=true`), CSRF, CORS, rate limiting, usuarios en BD real.
