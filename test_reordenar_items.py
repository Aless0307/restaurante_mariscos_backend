#!/usr/bin/env python3
"""
Script de prueba para el endpoint de reordenar items
"""

import requests
import json

# Configuración
BASE_URL = "http://localhost:8000/api"
# Necesitas obtener un token válido primero haciendo login

def test_reordenar_items(token, categoria_id):
    """
    Prueba el endpoint de reordenar items
    """
    url = f"{BASE_URL}/admin/categorias/{categoria_id}/reordenar-items"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Ejemplo de nuevo orden de items
    data = {
        "items": [
            "Camarones al Coco",
            "Camarones a la Diabla", 
            "Camarones Empanizados",
            "Camarones al Ajillo"
        ]
    }
    
    print(f"🔄 Probando reordenamiento de items...")
    print(f"📍 URL: {url}")
    print(f"📝 Nuevo orden: {data['items']}")
    
    response = requests.put(url, json=data, headers=headers)
    
    print(f"\n📊 Respuesta:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    return response.json()

def login(username, password):
    """Login para obtener token"""
    url = f"{BASE_URL}/auth-mongo/login"
    data = {"username": username, "password": password}
    
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        print(f"❌ Error en login: {response.text}")
        return None

if __name__ == "__main__":
    print("="*60)
    print("🧪 TEST: Endpoint de Reordenar Items")
    print("="*60)
    
    # Instrucciones
    print("\n📋 Instrucciones:")
    print("1. Asegúrate de que el servidor esté corriendo")
    print("2. Modifica este script con tus credenciales")
    print("3. Modifica el categoria_id y el array de items")
    print("\n" + "="*60)
    
    # Ejemplo de uso (comentado para seguridad)
    """
    # Descomentar y configurar con tus datos:
    
    USERNAME = "admin"
    PASSWORD = "tu_password"
    CATEGORIA_ID = "68e1a2eebeba702d9b740f4b"  # ID de la categoría CARNES o similar
    
    # Login
    token = login(USERNAME, PASSWORD)
    if token:
        print(f"✅ Login exitoso")
        
        # Probar reordenamiento
        result = test_reordenar_items(token, CATEGORIA_ID)
        
        if result.get("status") == "success":
            print(f"\n✅ ¡Reordenamiento exitoso!")
        else:
            print(f"\n❌ Error en reordenamiento")
    else:
        print(f"❌ No se pudo obtener token")
    """
    
    print("\n💡 Descomenta la sección de ejemplo y configura tus datos para probar")
