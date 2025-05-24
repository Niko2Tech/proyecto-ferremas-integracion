from pydantic import BaseModel
from typing import Optional


class DetalleVentaCreate(BaseModel):
    producto_id: int
    cantidad: int


class DetalleVentaResponse(DetalleVentaCreate):
    id: int
    precio_unitario: float

    class Config:
        from_attributes = True