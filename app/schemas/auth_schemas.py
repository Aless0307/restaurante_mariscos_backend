from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Esquemas para Usuario en MongoDB
class UsuarioMongoBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    es_admin: bool = False

class UsuarioMongoCreate(UsuarioMongoBase):
    password: str

class UsuarioMongoLogin(BaseModel):
    username: str  # Puede ser email o nombre de usuario
    password: str

class UsuarioMongo(UsuarioMongoBase):
    id: str
    fecha_registro: datetime
    activo: bool = True
    
    class Config:
        from_attributes = True

# Token schemas siguen igual
class Token(BaseModel):
    access_token: str
    token_type: str

class Message(BaseModel):
    message: str