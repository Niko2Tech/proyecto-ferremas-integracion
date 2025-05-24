from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.cliente import Cliente as ClienteModel
from app.schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate, ClienteObtenerPorCorreo

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=ClienteRead)
def crear_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    db_cliente = ClienteModel(**cliente.model_dump())
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

@router.get("/", response_model=list[ClienteRead])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(ClienteModel).all()

@router.get("/{id}", response_model=ClienteRead)
def obtener_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.put("/{id}", response_model=ClienteRead)
def actualizar_cliente(id: int, datos: ClienteUpdate, db: Session = Depends(get_db)):
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    for key, value in datos.model_dump(exclude_unset=True).items():
        setattr(cliente, key, value)

    db.commit()
    db.refresh(cliente)
    return cliente

@router.delete("/{id}")
def eliminar_cliente(id: int, db: Session = Depends(get_db)):
    cliente = db.query(ClienteModel).filter(ClienteModel.id == id).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    db.delete(cliente)
    db.commit()
    return {"detail": f"Cliente con ID {id} eliminado correctamente"}

@router.post("/obtener_por_correo", response_model=ClienteRead)
def obtener_cliente_por_correo(correo: ClienteObtenerPorCorreo, db: Session = Depends(get_db)):
    cliente = db.query(ClienteModel).filter(ClienteModel.correo == correo.correo).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente