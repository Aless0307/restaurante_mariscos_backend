import asyncio
import requests
import json

async def test_public_menu():
    try:
        print("🔄 Probando endpoint público del menú...")
        
        # Hacer request al endpoint público
        response = requests.get("http://localhost:8000/api/restaurante/menu-publico")
        
        print(f"📡 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Respuesta exitosa")
            print(f"📊 Total categorías: {data.get('total_categorias', 0)}")
            print(f"📊 Total items: {data.get('total_items', 0)}")
            
            categorias = data.get('categorias', [])
            print(f"\n📋 Categorías con items:")
            
            for i, cat in enumerate(categorias[:5]):  # Solo primeras 5
                items_count = len(cat.get('items', []))
                print(f"   {i+1}. {cat.get('nombre', 'Sin nombre')} - {items_count} items")
                
                # Mostrar algunos items
                items = cat.get('items', [])
                if items:
                    for j, item in enumerate(items[:2]):  # Solo primeros 2
                        print(f"      - {item.get('nombre', 'Sin nombre')}: ${item.get('precio', 0)}")
            
            if len(categorias) > 5:
                print(f"   ... y {len(categorias) - 5} categorías más")
            
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_public_menu())