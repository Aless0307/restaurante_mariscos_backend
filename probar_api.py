import requests
import json

# URL base de la API
BASE_URL = "http://localhost:8000"

def probar_rutas_api():
    """Probar todas las rutas de la API que consumen MongoDB"""
    
    print("🚀 Probando rutas de la API con datos de MongoDB")
    print("=" * 60)
    
    # 1. Probar información del restaurante
    print("\n📝 1. Información del restaurante:")
    try:
        response = requests.get(f"{BASE_URL}/api/restaurante/info")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Nombre: {data.get('nombre', 'N/A')}")
            print(f"✅ Teléfono: {data.get('telefono', 'N/A')}")
            print(f"✅ Email: {data.get('email', 'N/A')}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 2. Probar categorías del menú
    print("\n🍽️ 2. Categorías del menú:")
    try:
        response = requests.get(f"{BASE_URL}/api/mongo/menu/categorias")
        if response.status_code == 200:
            categorias = response.json()
            print(f"✅ Total categorías: {len(categorias)}")
            for cat in categorias:
                print(f"   • {cat.get('nombre', 'N/A')} ({cat.get('icono', '?')})")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 3. Probar menú completo
    print("\n📋 3. Menú completo:")
    try:
        response = requests.get(f"{BASE_URL}/api/mongo/menu/menu-completo")
        if response.status_code == 200:
            menu = response.json()
            print(f"✅ Total categorías: {menu.get('total_categorias', 0)}")
            print(f"✅ Total items: {menu.get('total_items', 0)}")
            
            # Mostrar algunos items de cada categoría
            for categoria in menu.get('categorias', [])[:2]:  # Solo las primeras 2
                print(f"\n   📂 {categoria.get('nombre', 'N/A')}:")
                for item in categoria.get('items', [])[:3]:  # Solo los primeros 3
                    precio = item.get('precio', 0)
                    print(f"      • {item.get('nombre', 'N/A')} - ${precio}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 4. Probar items por categoría
    print("\n🍤 4. Items de CAMARONES:")
    try:
        # Primero obtener el ID de la categoría CAMARONES
        response = requests.get(f"{BASE_URL}/api/mongo/menu/categorias")
        if response.status_code == 200:
            categorias = response.json()
            categoria_camarones = None
            for cat in categorias:
                if cat.get('nombre') == 'CAMARONES':
                    categoria_camarones = cat
                    break
            
            if categoria_camarones:
                categoria_id = categoria_camarones.get('id')
                response = requests.get(f"{BASE_URL}/api/mongo/menu/items?categoria_id={categoria_id}")
                if response.status_code == 200:
                    items = response.json()
                    print(f"✅ Items de camarones: {len(items)}")
                    for item in items:
                        precio = item.get('precio', 0)
                        print(f"   • {item.get('nombre', 'N/A')} - ${precio}")
                else:
                    print(f"❌ Error obteniendo items: {response.status_code}")
            else:
                print("❌ Categoría CAMARONES no encontrada")
        else:
            print(f"❌ Error obteniendo categorías: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 5. Probar búsqueda de items
    print("\n🔍 5. Búsqueda de items (buscar 'camaron'):")
    try:
        response = requests.get(f"{BASE_URL}/api/mongo/menu/items?buscar=camaron")
        if response.status_code == 200:
            items = response.json()
            print(f"✅ Resultados encontrados: {len(items)}")
            for item in items:
                precio = item.get('precio', 0)
                print(f"   • {item.get('nombre', 'N/A')} - ${precio}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # 6. Probar rutas originales (SQLite)
    print("\n💾 6. Comparación con rutas SQLite originales:")
    try:
        response = requests.get(f"{BASE_URL}/api/menu/categorias")
        if response.status_code == 200:
            categorias_sqlite = response.json()
            print(f"✅ Categorías en SQLite: {len(categorias_sqlite)}")
        else:
            print(f"❌ Error SQLite: {response.status_code}")
    except Exception as e:
        print(f"❌ Error SQLite: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 ¡Pruebas completadas!")
    print("\n📍 Endpoints disponibles:")
    print("   • MongoDB Menu: /api/mongo/menu/menu-completo")
    print("   • Información: /api/restaurante/info")
    print("   • Documentación: /docs")

if __name__ == "__main__":
    probar_rutas_api()