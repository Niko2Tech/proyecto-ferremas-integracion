# app/api/webpay.py
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.schemas.webpay import WebpayInitRequest, WebpayInitResponse
from app.models.webpay import TransaccionWebpay
from app.models.venta import Venta
from app.models.producto import Producto
from app.db.database import get_db
from datetime import datetime
import requests
import os
from uuid import uuid4
from fastapi.responses import JSONResponse
from app.models.dolar import Dolar

router = APIRouter(prefix="/webpay", tags=["Webpay"])

WEBPAY_URL = "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions"
COMMERCE_CODE = os.getenv("WEBPAY_COMMERCE_CODE", "597055555532")
API_KEY = os.getenv("WEBPAY_API_KEY", "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C")

@router.post("/iniciar", response_model=WebpayInitResponse)
def iniciar_transaccion(request: WebpayInitRequest, db: Session = Depends(get_db)):
    venta = db.query(Venta).filter_by(id=request.venta_id).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")

    # Convertir a CLP si se indicó que el monto está en dólares
    monto = venta.total
    if request.isDolar:
        dolar = (
            db.query(Dolar)
            .order_by(Dolar.create_date.desc())
            .first()
        )
        if not dolar:
            raise HTTPException(status_code=500, detail="Valor del dólar no disponible")
        monto_dolar = venta.total / dolar.bid
        venta.total_dolar = monto_dolar

    buy_order = venta.orden_compra
    session_id = f"SES-{venta.id}"
    return_url = "http://localhost:5173/confirmar"

    headers = {
        "Tbk-Api-Key-Id": COMMERCE_CODE,
        "Tbk-Api-Key-Secret": API_KEY,
        "Content-Type": "application/json"
    }

    data_init = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": monto,
        "return_url": return_url
    }

    try:
        response = requests.post(WEBPAY_URL, json=data_init, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Error conectando con Webpay")

    data = response.json()

    transaccion = TransaccionWebpay(
        venta_id=venta.id,
        token=data["token"],
        url_redireccion=data["url"],
        estado="pendiente"
    )
    db.add(transaccion)
    db.commit()

    return WebpayInitResponse(**data)



@router.get("/confirmar")
def confirmar_pago(token_ws: str, db: Session = Depends(get_db)):
    if not token_ws:
        raise HTTPException(status_code=400, detail="Token WS es requerido")

    confirm_url = f"{WEBPAY_URL}/{token_ws}"
    headers = {
        "Tbk-Api-Key-Id": COMMERCE_CODE,
        "Tbk-Api-Key-Secret": API_KEY,
        "Content-Type": "application/json"
    }

    try:
        response = requests.put(confirm_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException:
        raise HTTPException(status_code=502, detail="Error confirmando con Webpay")

    data = response.json()
    print(data)

    # Buscar la transacción
    transaccion = db.query(TransaccionWebpay).filter_by(token=token_ws).first()
    if not transaccion:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")

    # Actualizar transacción
    transaccion.estado = data.get("status", "desconocido")
    transaccion.response_data = data
    transaccion.fecha_transaccion = datetime.now()

    venta = transaccion.venta
    if not venta:
        raise HTTPException(status_code=404, detail="Venta asociada no encontrada")

    # Actualizar venta
    venta.estado = data.get("status", "desconocido")

    # Si la transacción fue exitosa, descontar stock
    if venta.estado == "AUTHORIZED":
        detalles = venta.detalles
        for detalle in detalles:
            producto = db.query(Producto).filter_by(id=detalle.producto_id).first()
            if producto:
                if producto.stock < detalle.cantidad:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Stock insuficiente para el producto ID {producto.id}"
                    )
                producto.stock -= detalle.cantidad

    db.commit()

    return JSONResponse(content={
        "mensaje": "Pago confirmado",
        "estado": venta.estado,
        "monto": data.get("amount"),
        "orden": data.get("buy_order"),
        "total_dolar": venta.total_dolar
    })