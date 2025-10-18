from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId

# Esquemas para información del restaurante
class RestauranteInfo(BaseModel):
    nombre: str
    descripcion_corta: str
    descripcion_larga: str
    año_fundacion: int
    años_experiencia: int
    clientes_satisfechos: int
    platos_unicos: int
    capacidad_personas: int
    slogan: str
    logo_url: Optional[str] = None
    fecha_actualizacion: Optional[datetime] = None
    version: Optional[str] = None

class RestauranteInfoMongo(BaseModel):
    id: str = Field(alias="_id")
    nombre: str
    descripcion_corta: str
    descripcion_larga: Optional[str] = ""
    telefono: str
    whatsapp: str
    email: str
    direccion: str
    horarios: str
    facebook: Optional[str] = ""
    instagram: Optional[str] = ""
    website: Optional[str] = ""
    logo_url: Optional[str] = ""
    imagen_banner_url: Optional[str] = ""
    imagen_sobre_nosotros_url: Optional[str] = ""
    anos_experiencia: Optional[int] = 20
    clientes_satisfechos: Optional[int] = 10000
    platos_unicos: Optional[int] = 50
    
    @validator('id', pre=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return str(v)
    
    class Config:
        populate_by_name = True

class RestauranteInfoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion_corta: Optional[str] = None
    descripcion_larga: Optional[str] = None
    telefono: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None
    direccion: Optional[str] = None
    horarios: Optional[str] = None
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    website: Optional[str] = None
    logo_url: Optional[str] = None
    imagen_banner_url: Optional[str] = None
    imagen_sobre_nosotros_url: Optional[str] = None
    anos_experiencia: Optional[int] = None
    clientes_satisfechos: Optional[int] = None
    platos_unicos: Optional[int] = None

# Esquemas para contacto
class DireccionInfo(BaseModel):
    calle: str
    codigo_postal: str
    ciudad: str
    estado: str
    pais: str

class HorariosInfo(BaseModel):
    todos_los_dias: str

class ContactoInfo(BaseModel):
    telefono: str
    whatsapp: str
    email: str
    direccion: DireccionInfo
    horarios: HorariosInfo
    maps_embed: str
    fecha_actualizacion: Optional[datetime] = None

# Esquemas para menú
class ItemMenuMongo(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    categoria_id: str
    categoria_nombre: str
    nombre: str
    precio: float
    descripcion: Optional[str] = ""
    disponible: bool = True
    orden: int
    imagen_url: Optional[str] = None
    imagen_id: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    
    @validator('id', pre=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
    class Config:
        populate_by_name = True

class CategoriaMenuMongo(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    nombre: str
    color: str
    icono: str
    orden: int
    activo: bool = True
    imagen_url_original: Optional[str] = None
    imagen_id: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    items: Optional[List[ItemMenuMongo]] = []
    
    @validator('id', pre=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
    class Config:
        populate_by_name = True

# Esquemas para características
class CaracteristicaRestaurante(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    titulo: str
    descripcion: str
    icono: str
    fecha_creacion: Optional[datetime] = None
    
    class Config:
        populate_by_name = True

# Esquemas para servicios
class ServicioRestaurante(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    nombre: str
    descripcion: str
    icono: str
    fecha_creacion: Optional[datetime] = None
    
    class Config:
        populate_by_name = True

# Esquemas para respuestas completas
class MenuCompleto(BaseModel):
    categorias: List[CategoriaMenuMongo]
    total_categorias: int
    total_items: int

class DatosRestauranteCompleto(BaseModel):
    restaurante: RestauranteInfo
    contacto: ContactoInfo
    caracteristicas: List[CaracteristicaRestaurante]
    servicios: List[ServicioRestaurante]

# Esquemas para administración
class ItemMenuMongoCreate(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = ""

class ItemMenuMongoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    descripcion: Optional[str] = None
    disponible: Optional[bool] = None

class CategoriaMenuMongoCreate(BaseModel):
    nombre: str
    color: str
    icono: str
    imagen_url_original: Optional[str] = None

class CategoriaMenuMongoUpdate(BaseModel):
    nombre: Optional[str] = None
    color: Optional[str] = None
    icono: Optional[str] = None
    imagen_url_original: Optional[str] = None
    activo: Optional[bool] = None

class RestauranteInfoMongo(RestauranteInfo):
    id: Optional[str] = Field(None, alias="_id")
    
    class Config:
        populate_by_name = True

class RestauranteInfoMongoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion_corta: Optional[str] = None
    descripcion_larga: Optional[str] = None
    telefono: Optional[str] = None
    whatsapp: Optional[str] = None
    email: Optional[str] = None

class ActualizarItemMenu(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    descripcion: Optional[str] = None
    disponible: Optional[bool] = None
    imagen_url: Optional[str] = None
    imagen_id: Optional[str] = None

class CrearItemMenu(BaseModel):
    nombre: str
    precio: float
    descripcion: Optional[str] = ""
    disponible: bool = True
    imagen_url: Optional[str] = None
    imagen_id: Optional[str] = None

class ActualizarCategoriaMenu(BaseModel):
    nombre: Optional[str] = None
    color: Optional[str] = None
    icono: Optional[str] = None
    activo: Optional[bool] = None
    imagen_url_original: Optional[str] = None
    imagen_id: Optional[str] = None

class CrearCategoriaMenu(BaseModel):
    nombre: str
    color: str = "#16a34a"
    icono: str = "🍽️"
    activo: bool = True
    imagen_url_original: Optional[str] = None
    imagen_id: Optional[str] = None

# Esquemas para gestión de imágenes por sección
class SeccionImagen(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    seccion: str  # "hero", "menu", "galeria", "about", "logo", "banner"
    titulo: str
    descripcion: str
    imagen_id: Optional[str] = None
    imagen_url: Optional[str] = None
    orden: int = 0
    activo: bool = True
    fecha_actualizacion: Optional[datetime] = None
    
    @validator('id', pre=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v
    
    class Config:
        populate_by_name = True

class ActualizarSeccionImagen(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    imagen_id: Optional[str] = None
    imagen_url: Optional[str] = None
    activo: Optional[bool] = None

class CrearItemMenu(BaseModel):
    categoria_id: str
    nombre: str
    precio: float
    descripcion: Optional[str] = ""
    disponible: bool = True

class CrearCategoriaMenu(BaseModel):
    nombre: str
    color: str
    icono: str
    orden: int
    imagen_url_original: Optional[str] = None