from pymongo import MongoClient
import json
from datetime import datetime

# Configuración
MONGO_URI = "mongodb+srv://alessandroah77:alessandro2003@clustermarisco.uuco735.mongodb.net/?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE"
DATABASE_NAME = "restaurante_dario"

def test_conexion_mongodb():
    """Prueba de conexión a MongoDB y carga de datos básicos"""
    
    client = None
    try:
        print("🚀 Probando conexión a MongoDB...")
        
        # Conectar con configuración específica para SSL
        client = MongoClient(
            MONGO_URI,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000,
            socketTimeoutMS=5000
        )
        
        # Probar la conexión
        client.admin.command('ping')
        print("✅ Conexión exitosa a MongoDB Atlas!")
        
        db = client[DATABASE_NAME]
        
        # Limpiar y crear datos de prueba
        print("🧹 Limpiando colecciones...")
        db.restaurante_info.delete_many({})
        db.categorias_menu.delete_many({})
        
        # Insertar información básica del restaurante
        print("📝 Insertando información del restaurante...")
        restaurante_info = {
            "nombre": "Dario Restaurante",
            "descripcion_corta": "Los mariscos más frescos del mar, preparados con pasión y tradición desde 1969",
            "telefono": "+52 229 109 6048",
            "whatsapp": "522291096048",
            "email": "restaurantedario1@outlook.com",
            "direccion": "Carr. Veracruz - Medellin km 2.5, 91966 Veracruz, Ver.",
            "horarios": "9:00 AM - 6:00 PM",
            "fecha_creacion": datetime.now()
        }
        db.restaurante_info.insert_one(restaurante_info)
        
        # Insertar algunas categorías de prueba
        print("🍽️ Insertando categorías de menú...")
        categorias_prueba = [
            {
                "nombre": "CARNES",
                "color": "bg-red-600",
                "icono": "🥩",
                "orden": 1,
                "activo": True,
                "fecha_creacion": datetime.now()
            },
            {
                "nombre": "MARISCOS",
                "color": "bg-blue-600",
                "icono": "🦐",
                "orden": 2,
                "activo": True,
                "fecha_creacion": datetime.now()
            },
            {
                "nombre": "BEBIDAS",
                "color": "bg-green-600",
                "icono": "🥤",
                "orden": 3,
                "activo": True,
                "fecha_creacion": datetime.now()
            }
        ]
        
        result = db.categorias_menu.insert_many(categorias_prueba)
        print(f"✅ {len(result.inserted_ids)} categorías insertadas")
        
        # Insertar algunos items de menú
        print("📋 Insertando items de menú...")
        items_prueba = [
            {
                "categoria_id": result.inserted_ids[0],
                "categoria_nombre": "CARNES",
                "nombre": "Barbacoa de Res",
                "precio": 110,
                "descripcion": "Deliciosa barbacoa preparada tradicionalmente",
                "disponible": True,
                "orden": 1,
                "fecha_creacion": datetime.now()
            },
            {
                "categoria_id": result.inserted_ids[1],
                "categoria_nombre": "MARISCOS",
                "nombre": "Camarón Empanizado",
                "precio": 200,
                "descripcion": "Camarones frescos empanizados",
                "disponible": True,
                "orden": 1,
                "fecha_creacion": datetime.now()
            },
            {
                "categoria_id": result.inserted_ids[2],
                "categoria_nombre": "BEBIDAS",
                "nombre": "Agua de Jamaica",
                "precio": 45,
                "descripcion": "Agua fresca natural",
                "disponible": True,
                "orden": 1,
                "fecha_creacion": datetime.now()
            }
        ]
        
        result_items = db.items_menu.insert_many(items_prueba)
        print(f"✅ {len(result_items.inserted_ids)} items insertados")
        
        # Verificar datos insertados
        print("\n📊 Verificando datos...")
        total_categorias = db.categorias_menu.count_documents({})
        total_items = db.items_menu.count_documents({})
        
        print(f"   • Categorías en BD: {total_categorias}")
        print(f"   • Items en BD: {total_items}")
        
        print("\n🎉 ¡Datos de prueba cargados exitosamente!")
        print(f"📍 Base de datos: {DATABASE_NAME}")
        
    except Exception as e:
        print(f"🚨 Error: {e}")
        
    finally:
        if client:
            client.close()
            print("🔌 Conexión cerrada")

if __name__ == "__main__":
    test_conexion_mongodb()