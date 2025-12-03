#!/usr/bin/env python3
"""
Script para crear el usuario 'restaurantedario' usando bcrypt directamente
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.mongo_database import get_mongodb
import bcrypt
from datetime import datetime

def crear_usuario_restaurantedario():
    """Crear el usuario restaurantedario directamente"""
    try:
        # Conectar a MongoDB
        db = get_mongodb()
        
        # Verificar si ya existe el usuario
        usuario_existente = db.usuarios.find_one({"email": "restaurantedario@restaurante.com"})
        
        if usuario_existente:
            print("⚠️  El usuario 'restaurantedario' ya existe")
            print(f"   Email: {usuario_existente['email']}")
            print(f"   Nombre: {usuario_existente.get('nombre', 'N/A')}")
            print(f"   Es admin: {usuario_existente.get('es_admin', False)}")
            
            # Actualizar la contraseña
            print("\n🔄 Actualizando contraseña...")
            password = "Dario6219$"
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
            
            db.usuarios.update_one(
                {"email": "restaurantedario@restaurante.com"},
                {"$set": {
                    "password_hash": password_hash,
                    "es_admin": True,
                    "activo": True
                }}
            )
            print("✅ Contraseña y permisos actualizados exitosamente")
            print("=" * 60)
            print("📧 Email: restaurantedario@restaurante.com")
            print("👤 Usuario: restaurantedario")
            print("🔑 Contraseña: Dario6219$")
            print("⚡ Permisos: Administrador")
            print("=" * 60)
            return
        
        # Crear el nuevo usuario administrador
        print("🔐 Generando hash de contraseña con bcrypt...")
        password = "Dario6219$"
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        
        nuevo_usuario = {
            "nombre": "Restaurante Dario",
            "email": "restaurantedario@restaurante.com",
            "telefono": "2291096048",
            "password_hash": password_hash,
            "es_admin": True,
            "fecha_registro": datetime.utcnow(),
            "activo": True
        }
        
        result = db.usuarios.insert_one(nuevo_usuario)
        
        print("🎉 ¡Usuario administrador creado exitosamente!")
        print("=" * 60)
        print("📧 Email: restaurantedario@restaurante.com")
        print("👤 Usuario para login: restaurantedario")
        print("🔑 Contraseña: Dario6219$")
        print("👤 Nombre: Restaurante Dario")
        print("⚡ Permisos: Administrador")
        print(f"🆔 ID: {result.inserted_id}")
        print(f"🔐 Hash generado: {password_hash[:30]}...")
        print("=" * 60)
        print()
        print("📝 IMPORTANTE: Para hacer login usa:")
        print("   - Usuario/Email: restaurantedario")
        print("   - Contraseña: Dario6219$")
        print()
        print("🌐 URL de login: http://localhost:5173")
        
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
