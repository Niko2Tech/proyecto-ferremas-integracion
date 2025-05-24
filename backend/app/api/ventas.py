from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from datetime import datetime
from app.db.database import get_db
from app.models.venta import Venta
from app.models.detalle_venta import DetalleVenta
from app.models.producto import Producto
from app.schemas.venta import VentaCreate, VentaResponse

router = APIRouter(prefix="/ventas", tags=["Ventas"])

@router.post("/crear", response_model=VentaResponse)
def crear_venta(venta_data: VentaCreate, db: Session = Depends(get_db)):
    total = 0
    detalles_para_guardar = []

    for item in venta_data.productos:
        producto = db.query(Producto).filter_by(id=item.producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto ID {item.producto_id} no encontrado")

        if producto.stock < item.cantidad:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para {producto.nombre}")

        subtotal = producto.precio * item.cantidad
        total += subtotal

        detalles_para_guardar.append({
            "producto_id": producto.id,
            "cantidad": item.cantidad,
            "precio_unitario": producto.precio
        })

    orden_compra = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid4().hex[:6].upper()}"

    venta = Venta(
        cliente_id=venta_data.cliente_id,
        total=total,
        orden_compra=orden_compra,
        estado="pendiente",
        direccion_envio=venta_data.direccion_envio,
        correo_contacto=venta_data.correo_contacto,
    )
    db.add(venta)
    db.flush()  # para obtener venta.id antes de insertar detalles

    for detalle in detalles_para_guardar:
        db.add(DetalleVenta(
            venta_id=venta.id,
            producto_id=detalle["producto_id"],
            cantidad=detalle["cantidad"],
            precio_unitario=detalle["precio_unitario"]
        ))

    db.commit()
    db.refresh(venta)

    return venta

@router.get("/{id}", response_model=VentaResponse)
def obtener_venta(id: int, db: Session = Depends(get_db)):
    venta = db.query(Venta).filter(Venta.id == id).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta


@router.get("/orden/{orden_compra}", response_model=VentaResponse)
def obtener_venta_por_orden(orden_compra: str, db: Session = Depends(get_db)):
    venta = db.query(Venta).filter(Venta.orden_compra == orden_compra).first()
    print(venta)    
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta
