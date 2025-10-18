from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.mongo_database import get_mongo_db
from app.schemas.auth_schemas import *
from app.services.auth_mongo_simple import AuthService
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/register", response_model=dict)
async def register_user(user: UsuarioMongoCreate, db = Depends(get_mongo_db)):
    """Registrar un nuevo usuario en MongoDB"""
    # Verificar si el email ya existe
    existing_user = db.usuarios.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Crear el usuario
    hashed_password = AuthService.get_password_hash(user.password)
    user_doc = {
        "nombre": user.nombre,
        "email": user.email,
        "telefono": user.telefono,
        "password_hash": hashed_password,
        "es_admin": user.es_admin,
        "fecha_registro": datetime.utcnow(),
        "activo": True
    }
    
    result = db.usuarios.insert_one(user_doc)
    
    return {
        "message": "Usuario creado exitosamente",
        "user_id": str(result.inserted_id)
    }

@router.post("/login", response_model=Token)
async def login_user(user_credentials: UsuarioMongoLogin, db = Depends(get_mongo_db)):
    """Iniciar sesión de usuario"""
    # Verificar credenciales
    user = db.usuarios.find_one({"email": user_credentials.email})
    
    if not user or not AuthService.verify_password(user_credentials.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.get("activo", True):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Crear token
    access_token = AuthService.create_access_token(data={"sub": user["email"]})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/profile", response_model=UsuarioMongo)
async def get_user_profile(current_user: UsuarioMongo = Depends(AuthService.get_current_user)):
    """Obtener perfil del usuario actual"""
    return current_user

@router.get("/users", response_model=List[dict])
async def get_all_users(
    db = Depends(get_mongo_db),
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user)
):
    """Obtener todos los usuarios (solo admin)"""
    users = list(db.usuarios.find({}, {"password_hash": 0}))  # Excluir password_hash
    
    # Convertir ObjectId a string
    for user in users:
        user["id"] = str(user["_id"])
        del user["_id"]
    
    return users

@router.put("/users/{user_id}/toggle", response_model=dict)
async def toggle_user_status(
    user_id: str,
    db = Depends(get_mongo_db),
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user)
):
    """Activar/desactivar usuario (solo admin)"""
    try:
        user = db.usuarios.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        new_status = not user.get("activo", True)
        result = db.usuarios.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {"activo": new_status}}
        )
        
        action = "activado" if new_status else "desactivado"
        return {"message": f"Usuario {action} exitosamente"}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al cambiar estado del usuario: {str(e)}"
        )