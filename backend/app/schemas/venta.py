from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from app.schemas.detalle_venta import DetalleVentaCreate, DetalleVentaResponse



class VentaCreate(BaseModel):
    cliente_id: int
    productos: List[DetalleVentaCreate]  # Carrito con producto_id y cantidad
    direccion_envio: Optional[str] = Field(None, max_length=255)
    correo_contacto: Optional[str] = Field(None, max_length=255)


class VentaResponse(BaseModel):
    id: int
    cliente_id: int
    total: float
    total_dolar: float
    estado: str
    orden_compra: str
    fecha: datetime
    direccion_envio: Optional[str] = Field(None, max_length=255)
    correo_contacto: Optional[str] = Field(None, max_length=255)
    detalles: List[DetalleVentaResponse]

    class Config:
        from_attributes = True
