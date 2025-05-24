from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base
from sqlalchemy.orm import relationship


class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    total = Column(Float, nullable=False)
    total_dolar = Column(Float, nullable=False, default=0)
    fecha = Column(DateTime, default=datetime.now())
    estado = Column(String, default="pendiente")  # pendiente, pagado, rechazado
    orden_compra = Column(String, unique=True, nullable=False)
    direccion_envio = Column(String, nullable=True)
    correo_contacto = Column(String, nullable=True)

    cliente = relationship("Cliente")
    transaccion = relationship("TransaccionWebpay", back_populates="venta", uselist=False)
    detalles = relationship("DetalleVenta", back_populates="venta")
