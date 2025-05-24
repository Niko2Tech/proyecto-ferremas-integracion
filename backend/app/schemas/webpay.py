from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict


class WebpayInitRequest(BaseModel):
    venta_id: int
    isDolar: bool


class WebpayInitResponse(BaseModel):
    token: str
    url: str


class WebpayConfirmResponse(BaseModel):
    vci: Optional[str]
    amount: float
    status: str
    buy_order: str
    session_id: str
    card_detail: Optional[Dict[str, str]]
    accounting_date: Optional[str]
    transaction_date: datetime
    authorization_code: Optional[str]
    payment_type_code: Optional[str]
    response_code: int
    installments_number: int


class TransaccionWebpayBase(BaseModel):
    venta_id: int
    token: str
    url_redireccion: Optional[str]
    estado: Optional[str]
    response_data: Optional[dict]


class TransaccionWebpayCreate(TransaccionWebpayBase):
    pass


class TransaccionWebpayResponse(TransaccionWebpayBase):
    id: int
    fecha_transaccion: datetime

    class Config:
        from_attributes = True
