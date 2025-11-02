#!/usr/bin/env python3
"""
Script para crear índices en MongoDB para mejorar el rendimiento
"""
from app.mongo_database import get_mongodb
from pymongo import ASCENDING, DESCENDING

def crear_indices():
    """Crear índices en las colecciones de MongoDB"""
    db = get_mongodb()
    
    print("🔧 Creando índices en MongoDB...")
    
    # Índices para categorias_menu
    print("\n📁 Creando índices en categorias_menu...")
    db.categorias_menu.create_index([("activo", ASCENDING)])
    db.categorias_menu.create_index([("orden", ASCENDING)])
    db.categorias_menu.create_index([("activo", ASCENDING), ("orden", ASCENDING)])
    print("✅ Índices creados en categorias_menu")
    
    # Índices para items_menu
    print("\n📁 Creando índices en items_menu...")
    db.items_menu.create_index([("categoria_id", ASCENDING)])
    db.items_menu.create_index([("disponible", ASCENDING)])
    db.items_menu.create_index([("orden", ASCENDING)])
    db.items_menu.create_index([("categoria_id", ASCENDING), ("orden", ASCENDING)])
    db.items_menu.create_index([("categoria_id", ASCENDING), ("disponible", ASCENDING)])
    print("✅ Índices creados en items_menu")
    
    # Índices para nombre (búsqueda de texto)
    print("\n📁 Creando índice de texto en items_menu...")
    try:
        db.items_menu.create_index([("nombre", "text"), ("descripcion", "text")])
        print("✅ Índice de texto creado en items_menu")
    except Exception as e:
        print(f"⚠️  Índice de texto ya existe o error: {e}")
    
    # Listar todos los índices creados
    print("\n📊 Índices en categorias_menu:")
    for index in db.categorias_menu.list_indexes():
        print(f"  - {index['name']}: {index['key']}")
    
    print("\n📊 Índices en items_menu:")
    for index in db.items_menu.list_indexes():
        print(f"  - {index['name']}: {index['key']}")
    
    print("\n✨ ¡Índices creados exitosamente!")
    print("🚀 El rendimiento de las consultas debería mejorar significativamente.")

if __name__ == "__main__":
    crear_indices()
