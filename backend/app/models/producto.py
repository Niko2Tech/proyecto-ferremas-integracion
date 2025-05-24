from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True, nullable=False)
    marca = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    categoria = Column(String, nullable=False)
    fecha_actualizacion = Column(DateTime, default=datetime.now())
    imagen_url = Column(String, nullable=True, default="/static/images/c63e12d6add6400f89f205d318a13716.jpg") 