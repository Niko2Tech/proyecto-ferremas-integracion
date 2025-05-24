from pydantic import BaseModel
from datetime import datetime

class DolarBase(BaseModel):
    code: str
    codein: str
    name: str
    high: float
    low: float
    varBid: float
    pctChange: float
    bid: float
    ask: float
    timestamp: str
    create_date: datetime

class DolarCreate(DolarBase):
    pass

class DolarInDB(DolarBase):
    id: int
    class Config:
        from_attributes = True
