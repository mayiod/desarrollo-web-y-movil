import argparse
import json
import xml.etree.ElementTree as ET
from decimal import Decimal, InvalidOperation

import stomp

DESTINO = "cola.pedidos"


def construir_fijo(pedido):
    identificador = str(pedido["id"]).zfill(6)
    cliente = str(pedido["cliente"])
    monto = pedido["monto"]

    if len(identificador) > 6:
        raise ValueError("El id no puede superar los 6 caracteres")
    if len(cliente) > 20:
        raise ValueError("El cliente no puede superar los 20 caracteres")
    if not cliente.replace(" ", "").isalnum():
        raise ValueError("El cliente debe ser alfanumérico")
    if monto < 0:
        raise ValueError("El monto debe ser positivo")

    monto_txt = f"{monto:010.2f}"
    if len(monto_txt) > 10:
        raise ValueError("El monto no puede superar los 10 caracteres")

    return f"{identificador}{cliente:<20}{monto_txt}"


def construir_xml(pedido):
    raiz = ET.Element("pedido")
    ET.SubElement(raiz, "id").text = str(pedido["id"])
    ET.SubElement(raiz, "cliente").text = str(pedido["cliente"])
    ET.SubElement(raiz, "monto").text = f"{pedido['monto']:.2f}"
    return ET.tostring(raiz, encoding="unicode")


def construir_mensaje(formato, pedido, texto):
    if formato == "texto":
        return texto, "text/plain;charset=utf-8"
    if formato == "fijo":
        return construir_fijo(pedido), "text/plain;charset=utf-8"
    if formato == "json":
        cuerpo = {**pedido, "monto": float(pedido["monto"])}
        return json.dumps(cuerpo), "application/json"
    if formato == "xml":
        return construir_xml(pedido), "application/xml"
    raise ValueError(f"Formato no soportado: {formato}")


def main():
    parser = argparse.ArgumentParser(description="Productor STOMP")
    parser.add_argument("--formato", choices=["texto", "fijo", "xml", "json"], required=True)
    parser.add_argument("--mensaje", default="Hola, desde el productor STOMP")
    parser.add_argument("--id", type=int, default=123)
    parser.add_argument("--cliente", default="Ernesto Ivanco")
    parser.add_argument("--monto", default="123.45")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=61613)
    parser.add_argument("--usuario", default="demo")
    parser.add_argument("--clave", default="demo123")
    args = parser.parse_args()

    try:
        monto = Decimal(args.monto)
        if not monto.is_finite():
            raise ValueError("El monto debe ser un número finito")
    except (InvalidOperation, ValueError):
        parser.error(f"Monto no válido: {args.monto}")

    pedido = {"id": args.id, "cliente": args.cliente, "monto": monto}

    try:
        cuerpo, mime = construir_mensaje(args.formato, pedido, args.mensaje)
    except ValueError as error:
        parser.error(str(error))

    conexion = stomp.Connection12([(args.host, args.port)])
    try:
        conexion.connect(args.usuario, args.clave, wait=True)
        conexion.send(
            destination=DESTINO,
            body=cuerpo,
            headers={
                "content-type": mime,
                "x-formato": args.formato,
                "persistent": "true",
            },
        )
        print(f"Mensaje enviado a {DESTINO} con formato {args.formato}: {cuerpo}")
    finally:
        if conexion.is_connected():
            conexion.disconnect()


if __name__ == "__main__":
    main()