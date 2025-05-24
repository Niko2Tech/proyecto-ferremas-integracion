from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class ProductoBase(BaseModel):
    codigo: str = Field(..., min_length=5, max_length=30)
    marca: str = Field(..., max_length=50)
    nombre: str = Field(..., max_length=100)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    categoria: str = Field(..., max_length=50)
    imagen_url: Optional[str] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    codigo: Optional[str] = Field(None, min_length=5, max_length=30)
    marca: Optional[str] = Field(None, max_length=50)
    nombre: Optional[str] = Field(None, max_length=100)
    precio: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    categoria: Optional[str] = Field(None, max_length=50)
    imagen_url: Optional[str] = None

class ProductoRead(ProductoBase):
    id: int
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True