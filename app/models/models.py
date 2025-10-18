from sqlalchemy import Column, Integer, String, Float, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    telefono = Column(String(15), nullable=True)
    password_hash = Column(String(100), nullable=False)
    es_admin = Column(Boolean, default=False)  # Campo para administradores
    fecha_registro = Column(DateTime, default=datetime.utcnow)
    activo = Column(Boolean, default=True)
    
    # Relación con reservas
    reservas = relationship("Reserva", back_populates="usuario")

class CategoriaMenu(Base):
    __tablename__ = "categorias_menu"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)

class ItemMenu(Base):
    __tablename__ = "items_menu"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(Text)
    precio = Column(Float, nullable=False)
    categoria_id = Column(Integer, nullable=False)  # Foreign key a CategoriaMenu
    imagen_url = Column(String(500))
    disponible = Column(Boolean, default=True)
    tiempo_preparacion = Column(Integer)  # En minutos
    ingredientes = Column(Text)  # JSON string con lista de ingredientes
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Reserva(Base):
    __tablename__ = "reservas"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)  # Foreign key a Usuario
    nombre_cliente = Column(String(100), nullable=False)
    email_cliente = Column(String(255), nullable=False)
    telefono_cliente = Column(String(20), nullable=False)
    fecha_reserva = Column(DateTime, nullable=False)
    numero_personas = Column(Integer, nullable=False)
    mesa_preferida = Column(String(50))
    comentarios = Column(Text)
    estado = Column(String(20), default="pendiente")  # pendiente, confirmada, cancelada
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con usuario
    usuario = relationship("Usuario", back_populates="reservas")