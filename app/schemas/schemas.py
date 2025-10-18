from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Esquemas para Usuario
class UsuarioBase(BaseModel):
    nombre: str
    email: str
    telefono: Optional[str] = None
    es_admin: bool = False

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str

class Usuario(UsuarioBase):
    id: int
    fecha_registro: datetime
    activo: bool = True
    
    class Config:
        from_attributes = True

# Esquemas para Categoría de Menú
class CategoriaMenuBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class CategoriaMenuCreate(CategoriaMenuBase):
    pass

class CategoriaMenu(CategoriaMenuBase):
    id: int
    activo: bool
    
    class Config:
        from_attributes = True

# Esquemas para Item de Menú
class ItemMenuBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    categoria_id: int
    imagen_url: Optional[str] = None
    tiempo_preparacion: Optional[int] = None
    ingredientes: Optional[str] = None

class ItemMenuCreate(ItemMenuBase):
    pass

class ItemMenuUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    categoria_id: Optional[int] = None
    imagen_url: Optional[str] = None
    disponible: Optional[bool] = None
    tiempo_preparacion: Optional[int] = None
    ingredientes: Optional[str] = None

class ItemMenu(ItemMenuBase):
    id: int
    disponible: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Esquemas para Reserva
class ReservaBase(BaseModel):
    nombre_cliente: str
    email_cliente: EmailStr
    telefono_cliente: str
    fecha_reserva: datetime
    numero_personas: int
    mesa_preferida: Optional[str] = None
    comentarios: Optional[str] = None

class ReservaCreate(ReservaBase):
    pass

class ReservaUpdate(BaseModel):
    estado: str  # pendiente, confirmada, cancelada

class Reserva(ReservaBase):
    id: int
    estado: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Esquemas para respuestas
class Token(BaseModel):
    access_token: str
    token_type: str

class Message(BaseModel):
    message: str