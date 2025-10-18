#!/usr/bin/env python3
"""
Script para crear el usuario administrador 'dario' con contraseña 'restaurante' en MongoDB
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.mongo_database import get_mongodb
from app.services.auth_mongo_service import AuthService
from datetime import datetime

def crear_usuario_admin():
    """Crear el usuario administrador si no existe"""
    try:
        # Conectar a MongoDB
        db = get_mongodb()
        
        # Verificar si ya existe el usuario admin
        usuario_existente = db.usuarios.find_one({"email": "dario@restaurante.com"})
        
        if usuario_existente:
            print("✅ El usuario administrador ya existe")
            print(f"   Email: {usuario_existente['email']}")
            print(f"   Nombre: {usuario_existente['nombre']}")
            print(f"   Es admin: {usuario_existente.get('es_admin', False)}")
            return
        
        # Crear el usuario administrador
        admin_user = {
            "nombre": "Dario",
            "email": "dario@restaurante.com",
            "telefono": "2291096048",
            "password_hash": AuthService.get_password_hash("admin123"),  # Contraseña más corta
            "es_admin": True,
            "fecha_registro": datetime.utcnow(),
            "activo": True
        }
        
        result = db.usuarios.insert_one(admin_user)
        
        print("🎉 ¡Usuario administrador creado exitosamente!")
        print("📧 Email: dario@restaurante.com")
        print("🔑 Contraseña: admin123")
        print("👤 Nombre: Dario")
        print("⚡ Permisos: Administrador")
        print(f"🆔 ID: {result.inserted_id}")
        print()
        print("🔐 Puedes usar estas credenciales para acceder al panel de administración")
        
    except Exception as e:
        print(f"❌ Error al crear usuario administrador: {e}")

if __name__ == "__main__":
    print("🔧 Creando usuario administrador en MongoDB...")
    print("=" * 60)
    crear_usuario_admin()
    print("=" * 60)
    print("✅ Proceso completado")