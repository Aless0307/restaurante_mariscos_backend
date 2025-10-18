from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from app.database import get_db
from app.schemas.schemas import Reserva, ReservaCreate, ReservaUpdate, Message
from app.models.models import Reserva as ReservaModel
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/", response_model=Reserva)
async def create_reserva(reserva: ReservaCreate, db: Session = Depends(get_db)):
    """Crear una nueva reserva"""
    # Validar que la fecha de reserva sea en el futuro
    if reserva.fecha_reserva <= datetime.now():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de reserva debe ser en el futuro"
        )
    
    # Validar número de personas
    if reserva.numero_personas <= 0 or reserva.numero_personas > 20:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El número de personas debe ser entre 1 y 20"
        )
    
    db_reserva = ReservaModel(**reserva.dict())
    db.add(db_reserva)
    db.commit()
    db.refresh(db_reserva)
    
    return db_reserva

@router.get("/", response_model=List[Reserva])
async def get_reservas(
    fecha_desde: Optional[datetime] = None,
    fecha_hasta: Optional[datetime] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_admin_user)
):
    """Obtener reservas con filtros (solo admin)"""
    query = db.query(ReservaModel)
    
    if fecha_desde:
        query = query.filter(ReservaModel.fecha_reserva >= fecha_desde)
    
    if fecha_hasta:
        query = query.filter(ReservaModel.fecha_reserva <= fecha_hasta)
    
    if estado:
        query = query.filter(ReservaModel.estado == estado)
    
    reservas = query.order_by(ReservaModel.fecha_reserva).all()
    return reservas

@router.get("/hoy", response_model=List[Reserva])
async def get_reservas_hoy(
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_admin_user)
):
    """Obtener reservas de hoy (solo admin)"""
    hoy = datetime.now().date()
    manana = hoy + timedelta(days=1)
    
    reservas = db.query(ReservaModel).filter(
        ReservaModel.fecha_reserva >= hoy,
        ReservaModel.fecha_reserva < manana
    ).order_by(ReservaModel.fecha_reserva).all()
    
    return reservas

@router.get("/{reserva_id}", response_model=Reserva)
async def get_reserva(reserva_id: int, db: Session = Depends(get_db)):
    """Obtener una reserva específica"""
    reserva = db.query(ReservaModel).filter(ReservaModel.id == reserva_id).first()
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@router.put("/{reserva_id}", response_model=Reserva)
async def update_reserva_status(
    reserva_id: int,
    reserva_update: ReservaUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_admin_user)
):
    """Actualizar estado de una reserva (solo admin)"""
    db_reserva = db.query(ReservaModel).filter(ReservaModel.id == reserva_id).first()
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    # Validar estado
    estados_validos = ["pendiente", "confirmada", "cancelada"]
    if reserva_update.estado not in estados_validos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Estado inválido. Estados válidos: " + ", ".join(estados_validos)
        )
    
    db_reserva.estado = reserva_update.estado
    db.commit()
    db.refresh(db_reserva)
    
    return db_reserva

@router.delete("/{reserva_id}", response_model=Message)
async def delete_reserva(
    reserva_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_admin_user)
):
    """Eliminar una reserva (solo admin)"""
    db_reserva = db.query(ReservaModel).filter(ReservaModel.id == reserva_id).first()
    if not db_reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    
    db.delete(db_reserva)
    db.commit()
    
    return {"message": "Reserva eliminada correctamente"}