#!/usr/bin/env python3
"""
Script para crear el usuario administrador 'dario' con contraseña 'restaurante'
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal, engine
from app.models.models import Usuario
from app.services.auth_service import AuthService
from sqlalchemy.orm import Session

def crear_usuario_admin():
    """Crear el usuario administrador si no existe"""
    db = SessionLocal()
    try:
        # Verificar si ya existe el usuario admin
        usuario_existente = db.query(Usuario).filter(Usuario.email == "dario@restaurante.com").first()
        
        if usuario_existente:
            print("✅ El usuario administrador ya existe")
            print(f"   Email: {usuario_existente.email}")
            print(f"   Nombre: {usuario_existente.nombre}")
            print(f"   Es admin: {usuario_existente.es_admin}")
            return
        
        # Crear el usuario administrador
        admin_user = Usuario(
            nombre="Dario",
            email="dario@restaurante.com",
            telefono="2291096048",
            password_hash=AuthService.get_password_hash("restaurante"),
            es_admin=True,
            activo=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("🎉 ¡Usuario administrador creado exitosamente!")
        print("📧 Email: dario@restaurante.com")
        print("🔑 Contraseña: restaurante")
        print("👤 Nombre: Dario")
        print("⚡ Permisos: Administrador")
        print()
        print("🔐 Puedes usar estas credenciales para acceder al panel de administración")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error al crear usuario administrador: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🔧 Creando usuario administrador...")
    print("=" * 50)
    crear_usuario_admin()
    print("=" * 50)
    print("✅ Proceso completado")