#!/usr/bin/env python3
"""
Script simplificado para crear el usuario administrador en MongoDB
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.mongo_database import get_mongodb
import hashlib
from datetime import datetime

def hash_password_simple(password):
    """Hash simple con SHA256 + salt"""
    salt = "restaurante_dario_salt_2025"
    return hashlib.sha256((password + salt).encode()).hexdigest()

def crear_usuario_admin():
    """Crear el usuario administrador si no existe"""
    try:
        # Conectar a MongoDB
        db = get_mongodb()
        
        # Verificar si ya existe el usuario admin
        usuario_existente = db.usuarios.find_one({"email": "admin@restaurante.com"})
        
        if usuario_existente:
            print("✅ El usuario administrador ya existe")
            print(f"   Email: {usuario_existente['email']}")
            print(f"   Nombre: {usuario_existente['nombre']}")
            print(f"   Es admin: {usuario_existente.get('es_admin', False)}")
            return
        
        # Crear el usuario administrador con hash simple
        admin_user = {
            "nombre": "Dario Administrador",
            "email": "admin@restaurante.com",
            "telefono": "2291096048",
            "password_hash": hash_password_simple("admin123"),
            "es_admin": True,
            "fecha_registro": datetime.utcnow(),
            "activo": True
        }
        
        result = db.usuarios.insert_one(admin_user)
        
        print("🎉 ¡Usuario administrador creado exitosamente!")
        print("📧 Email: admin@restaurante.com")
        print("🔑 Contraseña: admin123")
        print("👤 Nombre: Dario Administrador")
        print("⚡ Permisos: Administrador")
        print(f"🆔 ID: {result.inserted_id}")
        print()
        print("🔐 Usa estas credenciales para acceder al panel de administración")
        print("⚠️  NOTA: Este es un hash simple para desarrollo, en producción usa bcrypt")
        
    except Exception as e:
        print(f"❌ Error al crear usuario administrador: {e}")

if __name__ == "__main__":
    print("🔧 Creando usuario administrador en MongoDB (versión simple)...")
    print("=" * 70)
    crear_usuario_admin()
    print("=" * 70)
    print("✅ Proceso completado")