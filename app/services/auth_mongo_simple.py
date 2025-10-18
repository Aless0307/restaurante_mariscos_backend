from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.mongo_database import get_mongo_db
from app.schemas.auth_schemas import UsuarioMongo
from bson import ObjectId
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración de seguridad
SECRET_KEY = os.getenv("SECRET_KEY", "tu-clave-secreta-super-segura-aqui")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuración de autenticación Bearer
security = HTTPBearer()

def hash_password_simple(password):
    """Hash simple con SHA256 + salt (temporal para desarrollo)"""
    salt = "restaurante_dario_salt_2025"
    return hashlib.sha256((password + salt).encode()).hexdigest()

def verify_password_simple(plain_password, hashed_password):
    """Verificar contraseña con hash simple"""
    return hash_password_simple(plain_password) == hashed_password

class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña (versión simple)"""
        return verify_password_simple(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generar hash de contraseña (versión simple)"""
        return hash_password_simple(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        """Crear token de acceso JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str):
        """Verificar y decodificar token JWT"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("sub")
            if email is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return email
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @staticmethod
    def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db = Depends(get_mongo_db)
    ) -> UsuarioMongo:
        """Obtener usuario actual desde el token"""
        email = AuthService.verify_token(credentials.credentials)
        
        # Buscar usuario en MongoDB
        user_data = db.usuarios.find_one({"email": email})
        if user_data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        # Convertir ObjectId a string
        user_data["id"] = str(user_data["_id"])
        del user_data["_id"]
        
        return UsuarioMongo(**user_data)

    @staticmethod
    def get_current_admin_user(current_user: UsuarioMongo = Depends(get_current_user)):
        """Obtener usuario administrador actual"""
        if not current_user.es_admin:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos de administrador"
            )
        return current_user