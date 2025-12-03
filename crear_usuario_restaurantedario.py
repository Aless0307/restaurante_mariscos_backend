#!/usr/bin/env python3
"""
Script para crear el usuario 'restaurantedario' con contraseña 'Dario6219$' en MongoDB
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.mongo_database import get_mongodb
from app.services.auth_mongo_service import AuthService
from datetime import datetime

def crear_usuario_restaurantedario():
    """Crear el usuario restaurantedario si no existe"""
    try:
        # Conectar a MongoDB
        db = get_mongodb()
        
        # Verificar si ya existe el usuario
        usuario_existente = db.usuarios.find_one({"email": "restaurantedario@restaurante.com"})
        
        if usuario_existente:
            print("⚠️  El usuario 'restaurantedario' ya existe")
            print(f"   Email: {usuario_existente['email']}")
            print(f"   Nombre: {usuario_existente['nombre']}")
            print(f"   Es admin: {usuario_existente.get('es_admin', False)}")
            
            # Preguntar si desea actualizar la contraseña
            respuesta = input("\n¿Deseas actualizar la contraseña? (s/n): ")
            if respuesta.lower() == 's':
                nueva_password_hash = AuthService.get_password_hash("Dario6219$")
                db.usuarios.update_one(
                    {"email": "restaurantedario@restaurante.com"},
                    {"$set": {"password_hash": nueva_password_hash}}
                )
                print("✅ Contraseña actualizada exitosamente")
            return
        
        # Crear el nuevo usuario administrador
        nuevo_usuario = {
            "nombre": "Restaurante Dario Admin",
            "email": "restaurantedario@restaurante.com",
            "telefono": "2291096048",
            "password_hash": AuthService.get_password_hash("Dario6219$"),
            "es_admin": True,
            "fecha_registro": datetime.utcnow(),
            "activo": True
        }
        
        result = db.usuarios.insert_one(nuevo_usuario)
        
        print("🎉 ¡Usuario administrador creado exitosamente!")
        print("=" * 60)
        print("📧 Email: restaurantedario@restaurante.com")
        print("👤 Usuario: restaurantedario")
        print("🔑 Contraseña: Dario6219$")
        print("👤 Nombre: Restaurante Dario Admin")
        print("⚡ Permisos: Administrador")
        print(f"🆔 ID: {result.inserted_id}")
        print("=" * 60)
        print()
        print("🔐 Puedes usar estas credenciales para acceder al panel de administración")
        print("🌐 URL de login: http://localhost:5173 (o tu dominio)")
        
    except Exception as e:
        print(f"❌ Error al crear usuario administrador: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 Creando usuario 'restaurantedario' en MongoDB...")
    print("=" * 60)
    print()
    crear_usuario_restaurantedario()
    print()
    print("✅ Proceso completado")
    print("=" * 60)
