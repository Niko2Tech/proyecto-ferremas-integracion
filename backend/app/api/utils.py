from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
from app.db.database import get_db
from app.models.dolar import Dolar
from app.schemas.dolar import DolarInDB
from datetime import datetime

router = APIRouter(prefix="/utils", tags=["Utils"])

@router.get("/dolar", response_model=DolarInDB)
async def obtener_y_guardar_dolar(db: Session = Depends(get_db)):
    url = "https://economia.awesomeapi.com.br/json/last/USD-CLP"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        usdclp = data["USDCLP"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error consultando API externa: {e}")

    dolar = Dolar(
        code=usdclp["code"],
        codein=usdclp["codein"],
        name=usdclp["name"],
        high=float(usdclp["high"]),
        low=float(usdclp["low"]),
        varBid=float(usdclp["varBid"]),
        pctChange=float(usdclp["pctChange"]),
        bid=float(usdclp["bid"]),
        ask=float(usdclp["ask"]),
        timestamp=usdclp["timestamp"],
        create_date=datetime.strptime(usdclp["create_date"], "%Y-%m-%d %H:%M:%S")
    )
    db.add(dolar)
    db.commit()
    db.refresh(dolar)
    return dolar
