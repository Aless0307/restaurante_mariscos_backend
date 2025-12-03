#!/usr/bin/env python3
"""
Script para probar el login con username en lugar de email
"""
import requests
import json

BASE_URL = "http://localhost:8000/api/auth-mongo"

def test_login(username, password):
    """Probar login con username"""
    print(f"🔐 Probando login con username: '{username}'")
    
    url = f"{BASE_URL}/login"
    data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            token = result.get("access_token", "")
            print(f"✅ Login exitoso!")
            print(f"   Token: {token[:50]}...")
            return token
        else:
            print(f"❌ Login fallido")
            print(f"   Status: {response.status_code}")
            print(f"   Error: {response.json()}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("="*60)
    print("🧪 TEST: Login con Username")
    print("="*60)
    print()
    
    # Test 1: Con username
    print("TEST 1: Login con username 'restaurantedario'")
    print("-"*60)
    token1 = test_login("restaurantedario", "Dario6219$")
    print()
    
    # Test 2: Con email completo
    print("TEST 2: Login con email completo")
    print("-"*60)
    token2 = test_login("restaurantedario@restaurante.com", "Dario6219$")
    print()
    
    # Test 3: Con credenciales incorrectas
    print("TEST 3: Login con contraseña incorrecta")
    print("-"*60)
    token3 = test_login("restaurantedario", "wrong_password")
    print()
    
    print("="*60)
    print("✅ Tests completados")
    print("="*60)
