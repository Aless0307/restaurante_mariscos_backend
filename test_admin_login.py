#!/usr/bin/env python3
"""
Script para probar el login del administrador
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_admin_login():
    """Probar login del administrador"""
    print("🔐 Probando login del administrador...")
    
    # Datos de login
    login_data = {
        "email": "admin@restaurante.com",
        "password": "admin123"
    }
    
    try:
        # Intentar login
        response = requests.post(
            f"{BASE_URL}/api/auth-mongo/login",
            json=login_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print("✅ Login exitoso!")
            print(f"🔑 Token: {token[:50]}...")
            
            # Probar acceso al perfil
            headers = {"Authorization": f"Bearer {token}"}
            profile_response = requests.get(
                f"{BASE_URL}/api/auth-mongo/profile",
                headers=headers
            )
            
            if profile_response.status_code == 200:
                profile = profile_response.json()
                print("👤 Perfil obtenido:")
                print(f"   Nombre: {profile.get('nombre')}")
                print(f"   Email: {profile.get('email')}")
                print(f"   Es Admin: {profile.get('es_admin')}")
                
                # Probar acceso a endpoint de admin
                admin_response = requests.get(
                    f"{BASE_URL}/api/admin/categorias",
                    headers=headers
                )
                
                if admin_response.status_code == 200:
                    categorias = admin_response.json()
                    print(f"🍽️ Acceso a admin exitoso! Categorías: {len(categorias)}")
                else:
                    print(f"❌ Error en endpoint admin: {admin_response.status_code}")
                    print(admin_response.text)
            else:
                print(f"❌ Error obteniendo perfil: {profile_response.status_code}")
                print(profile_response.text)
        else:
            print(f"❌ Login fallido: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    print("🧪 Probando sistema de autenticación de administrador...")
    print("=" * 60)
    test_admin_login()
    print("=" * 60)
    print("✅ Prueba completada")