import asyncio
import pymongo
from app.mongo_database import get_mongodb

async def test_menu_data():
    try:
        db = get_mongodb()
        
        print("🔍 Verificando datos en MongoDB...")
        
        # Contar documentos en categorias_menu
        count_categorias = db.categorias_menu.count_documents({})
        print(f"📊 Total de categorías en categorias_menu: {count_categorias}")
        
        # Contar documentos en items_menu
        count_items = db.items_menu.count_documents({})
        print(f"📊 Total de items en items_menu: {count_items}")
        
        # Listar todas las categorías
        categorias = list(db.categorias_menu.find())
        print(f"\n📋 Categorías encontradas:")
        
        total_items_combined = 0
        
        for i, cat in enumerate(categorias):
            print(f"   {i+1}. {cat.get('nombre', 'Sin nombre')}")
            print(f"      ID: {cat.get('_id')}")
            print(f"      Activo: {cat.get('activo', 'No definido')}")
            print(f"      Orden: {cat.get('orden', 'No definido')}")
            
            # Items en el documento de la categoría
            items_en_categoria = cat.get('items', [])
            print(f"      Items en documento: {len(items_en_categoria)}")
            
            # Items en la colección separada
            from bson import ObjectId
            items_en_coleccion = list(db.items_menu.find({"categoria_id": ObjectId(cat["_id"])}))
            print(f"      Items en colección separada: {len(items_en_coleccion)}")
            
            # Total combinado
            total_categoria = len(items_en_categoria) + len(items_en_coleccion)
            total_items_combined += total_categoria
            print(f"      📊 TOTAL COMBINADO: {total_categoria}")
            
            # Mostrar algunos items si existen
            if items_en_coleccion:
                print(f"      📋 Items de colección separada:")
                for j, item in enumerate(items_en_coleccion[:3]):  # Solo mostrar primeros 3
                    print(f"        - {item.get('nombre', 'Sin nombre')}: ${item.get('precio', 0)}")
                if len(items_en_coleccion) > 3:
                    print(f"        ... y {len(items_en_coleccion) - 3} más")
            
            if items_en_categoria:
                print(f"      📋 Items en documento:")
                for j, item in enumerate(items_en_categoria[:3]):  # Solo mostrar primeros 3
                    print(f"        - {item.get('nombre', 'Sin nombre')}: ${item.get('precio', 0)}")
                if len(items_en_categoria) > 3:
                    print(f"        ... y {len(items_en_categoria) - 3} más")
            
            print()
        
        print(f"🎯 RESUMEN:")
        print(f"   - Total categorías: {count_categorias}")
        print(f"   - Total items en colección separada: {count_items}")
        print(f"   - Total items combinados: {total_items_combined}")
        
        return categorias
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

if __name__ == "__main__":
    asyncio.run(test_menu_data())