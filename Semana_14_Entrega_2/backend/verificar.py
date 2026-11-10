import httpx

GATEWAY_URL = "http://localhost:8000"

def probar_flujo():
    with httpx.Client() as client:
        # 1. Iniciar sesión para obtener la cookie (ajusta la clave si es distinta en tu README)
        print("1. Iniciando sesión...")
        res_login = client.post(f"{GATEWAY_URL}/auth/login", json={"username": "ana", "password": "1234"})
        if res_login.status_code != 200:
            print(f"Error en login: {res_login.json()}")
            return
        print("Login exitoso. Cookie obtenida.")

        # 2. Crear un pedido
        print("\n2. Creando pedido...")
        res_order = client.post(f"{GATEWAY_URL}/api/orders", json={
            "items": [{"product_id": 1, "quantity": 2}]
        })
        if res_order.status_code != 201:
            print(f"Error creando pedido: {res_order.text}")
            return
        order_id = res_order.json()["id"]
        print(f"Pedido #{order_id} creado con estado: {res_order.json()['estado']}")

        # 3. Pagar el pedido (El nuevo endpoint)
        print("\n3. Procesando pago...")
        res_pay = client.post(f"{GATEWAY_URL}/api/payments/{order_id}")
        print(f"Resultado del pago: {res_pay.json()}")

        # 4. Consultar el GraphQL Gateway
        print("\n4. Consultando GraphQL...")
        query = """
        query ($id: Int!) {
          orderSummary(id: $id) {
            id
            estado
            total
            detalles {
              cantidad
              product {
                name
                price
              }
            }
          }
        }
        """
        res_graphql = client.post(f"{GATEWAY_URL}/graphql", json={
            "query": query,
            "variables": {"id": order_id}
        })
        print("Respuesta GraphQL:")
        import json
        print(json.dumps(res_graphql.json(), indent=2))

if __name__ == "__main__":
    probar_flujo()