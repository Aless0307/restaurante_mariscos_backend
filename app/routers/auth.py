from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.schemas import Usuario, UsuarioCreate, UsuarioLogin, Token, Message
from app.models.models import Usuario as UsuarioModel
from app.services.auth_service import AuthService

router = APIRouter()

@router.post("/register", response_model=Usuario)
async def register_user(user: UsuarioCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario"""
    # Verificar si el email ya existe
    db_user = db.query(UsuarioModel).filter(UsuarioModel.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear el usuario
    hashed_password = AuthService.get_password_hash(user.password)
    db_user = UsuarioModel(
        nombre=user.nombre,
        email=user.email,
        telefono=user.telefono,
        password_hash=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@router.post("/login", response_model=Token)
async def login_user(user_credentials: UsuarioLogin, db: Session = Depends(get_db)):
    """Iniciar sesión de usuario"""
    # Verificar credenciales
    user = db.query(UsuarioModel).filter(UsuarioModel.email == user_credentials.email).first()
    
    if not user or not AuthService.verify_password(user_credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token
    access_token = AuthService.create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=Usuario)
async def get_user_profile(current_user: Usuario = Depends(AuthService.get_current_user)):
    """Obtener perfil del usuario actual"""
    return current_user

@router.get("/users", response_model=List[Usuario])
async def get_all_users(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(AuthService.get_current_admin_user)
):
    """Obtener todos los usuarios (solo admin)"""
    users = db.query(UsuarioModel).all()
    return users