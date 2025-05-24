from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db.database import Base
from datetime import datetime

class Dolar(Base):
    __tablename__ = "dolar"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    codein = Column(String, nullable=False)
    name = Column(String, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    varBid = Column(Float, nullable=False)
    pctChange = Column(Float, nullable=False)
    bid = Column(Float, nullable=False)
    ask = Column(Float, nullable=False)
    timestamp = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.now())
