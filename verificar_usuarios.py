#!/usr/bin/env python3
"""
Script para verificar usuarios en la base de datos y probar contraseñas
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.mongo_database import get_mongodb
import bcrypt

def verificar_usuarios():
    """Verificar usuarios existentes"""
    try:
        db = get_mongodb()
        
        print("="*60)
        print("👥 USUARIOS EN LA BASE DE DATOS")
        print("="*60)
        
        usuarios = list(db.usuarios.find({}))
        
        if not usuarios:
            print("❌ No hay usuarios en la base de datos")
            return
        
        for i, user in enumerate(usuarios, 1):
            print(f"\n{i}. Usuario:")
            print(f"   📧 Email: {user.get('email')}")
            print(f"   👤 Nombre: {user.get('nombre')}")
            print(f"   ⚡ Es Admin: {user.get('es_admin', False)}")
            print(f"   ✅ Activo: {user.get('activo', False)}")
            print(f"   🔐 Hash: {user.get('password_hash', 'N/A')[:50]}...")
            
            # Probar contraseña para restaurantedario
            if 'restaurantedario' in user.get('email', '').lower():
                print(f"\n   🧪 Probando contraseñas comunes:")
                passwords_to_test = [
                    "Dario6219$",
                    "admin123",
                    "restaurante",
                ]
                
                for pwd in passwords_to_test:
                    try:
                        password_hash = user.get('password_hash', '')
                        # Verificar si el hash es compatible con bcrypt
                        if password_hash.startswith('$2b$') or password_hash.startswith('$2a$'):
                            result = bcrypt.checkpw(pwd.encode('utf-8'), password_hash.encode('utf-8'))
                            status = "✅ CORRECTA" if result else "❌ Incorrecta"
                            print(f"      - '{pwd}': {status}")
                        else:
                            print(f"      - '{pwd}': ⚠️ Hash no compatible con bcrypt")
                    except Exception as e:
                        print(f"      - '{pwd}': ❌ Error: {str(e)}")
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    verificar_usuarios()
