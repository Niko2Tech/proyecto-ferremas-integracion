from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class TransaccionWebpay(Base):
    __tablename__ = "webpay_transacciones"

    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    token = Column(String, unique=True, nullable=False)
    url_redireccion = Column(String)
    estado = Column(String)  # AUTHORIZED, FAILED, etc.
    response_data = Column(JSON)  # para guardar todo lo que devuelve webpay
    fecha_transaccion = Column(DateTime, default=datetime.now())

    venta = relationship("Venta", back_populates="transaccion")
