import argparse
import json
import time
import xml.etree.ElementTree as ET
import stomp

DESTINO = "cola.pedidos"


def interpretar_fijo(cuerpo):
    if len(cuerpo) != 36:
        raise ValueError("El contrato fijo debe tener 36 caracteres")

    identificador = cuerpo[0:6]
    cliente = cuerpo[6:26].strip()
    monto_txt = cuerpo[26:36]

    if not identificador.isdigit():
        raise ValueError("El id del contrato fijo no es numérico")
    if not cliente:
        raise ValueError("El cliente del contrato fijo viene vacío")
    if not (monto_txt[:7].isdigit() and monto_txt[7] == "." and monto_txt[8:].isdigit()):
        raise ValueError("El monto del contrato fijo no tiene un formato válido")

    return {
        "id": int(identificador),
        "cliente": cliente,
        "monto": monto_txt,
    }


def interpretar_xml(cuerpo):
    raiz = ET.fromstring(cuerpo)
    if raiz.tag != "pedido":
        raise ValueError("El nodo raíz debe ser <pedido>")
    return {hijo.tag: hijo.text for hijo in raiz}


def interpretar(cuerpo, headers):
    formato = (headers.get("x-formato") or "").lower()
    tipo_mime = (headers.get("content-type") or "").lower()

    if not formato:
        if "application/json" in tipo_mime:
            formato = "json"
        elif "application/xml" in tipo_mime or "text/xml" in tipo_mime:
            formato = "xml"
        else:
            formato = "texto"

    if formato == "texto":
        return formato, cuerpo
    if formato == "fijo":
        return formato, interpretar_fijo(cuerpo)
    if formato == "json":
        return formato, json.loads(cuerpo)
    if formato == "xml":
        return formato, interpretar_xml(cuerpo)

    raise ValueError(f"Formato no soportado: {formato}")


class Escuchador(stomp.ConnectionListener):
    def __init__(self, conexion):
        self.conexion = conexion

    def on_error(self, frame):
        print(f"Error del broker: {frame.body}")

    def on_disconnected(self):
        print("Conexión STOMP cerrada")

    def on_message(self, frame):
        ack_id = frame.headers.get("ack")
        try:
            formato, contenido = interpretar(frame.body, frame.headers)
            print(f"Recibido formato {formato}")
            if isinstance(contenido, str):
                print(contenido)
            else:
                print(json.dumps(contenido, ensure_ascii=False, indent=2))
            self.conexion.ack(ack_id)
        except Exception as error:
            print(f"Mensaje inválido: {error}")
            self.conexion.nack(ack_id)


def main():
    parser = argparse.ArgumentParser(description="Consumidor STOMP")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=61613)
    parser.add_argument("--usuario", default="demo")
    parser.add_argument("--clave", default="demo123")
    args = parser.parse_args()

    conexion = stomp.Connection12([(args.host, args.port)])
    conexion.set_listener("escuchador", Escuchador(conexion))
    try:
        conexion.connect(args.usuario, args.clave, wait=True)
        conexion.subscribe(
            destination=DESTINO,
            id="lector-pedidos",
            ack="client-individual",
            headers={"prefetch-count": 1},
        )
        print(f"Escuchando {DESTINO} (Ctrl+C para salir)")
        while conexion.is_connected():
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Deteniendo consumidor")
    finally:
        if conexion.is_connected():
            conexion.disconnect()


if __name__ == "__main__":
    main()
