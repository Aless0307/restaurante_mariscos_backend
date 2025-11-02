#!/usr/bin/env python3
"""Script para diagnosticar dónde está el item 'Barbacoa de Res'"""

from app.mongo_database import get_mongo_db
from bson import ObjectId

db = get_mongo_db()

# Buscar el item "Barbacoa de Res"
categoria_id = "68e1a2efbeba702d9b740f53"
item_nombre = "Barbacoa de Res"

print(f"\n{'='*60}")
print(f"DIAGNÓSTICO: Buscando '{item_nombre}'")
print(f"{'='*60}\n")

# 1. Buscar en colección items_menu SIN filtro de categoría
print("1️⃣ BUSCANDO EN items_menu (SIN filtro de categoría):")
item_sin_filtro = db.items_menu.find_one({"nombre": item_nombre})
if item_sin_filtro:
    print(f"   ✅ ENCONTRADO:")
    print(f"      - _id: {item_sin_filtro['_id']}")
    print(f"      - categoria_id: {item_sin_filtro.get('categoria_id')} (tipo: {type(item_sin_filtro.get('categoria_id'))})")
    print(f"      - categoria_nombre: {item_sin_filtro.get('categoria_nombre')}")
    print(f"      - disponible: {item_sin_filtro.get('disponible')}")
else:
    print(f"   ❌ NO encontrado")

# 2. Buscar en colección items_menu CON filtro de categoría
print(f"\n2️⃣ BUSCANDO EN items_menu CON categoria_id={categoria_id}:")
item_con_filtro = db.items_menu.find_one({
    "categoria_id": ObjectId(categoria_id),
    "nombre": item_nombre
})
if item_con_filtro:
    print(f"   ✅ ENCONTRADO")
else:
    print(f"   ❌ NO encontrado con ese filtro")

# 3. Ver qué categoría es la solicitada
print(f"\n3️⃣ CATEGORÍA SOLICITADA (ID: {categoria_id}):")
cat_solicitada = db.categorias_menu.find_one({"_id": ObjectId(categoria_id)})
if cat_solicitada:
    print(f"   Nombre: {cat_solicitada['nombre']}")
    print(f"   Items en array embebido: {len(cat_solicitada.get('items', []))}")
    
    # Buscar el item en el array
    items_array = cat_solicitada.get('items', [])
    item_en_array = None
    for i, item in enumerate(items_array):
        if item.get('nombre') == item_nombre:
            item_en_array = (i, item)
            break
    
    if item_en_array:
        idx, item = item_en_array
        print(f"   ✅ Item '{item_nombre}' ENCONTRADO en array (índice {idx})")
        print(f"      - disponible: {item.get('disponible')}")
        print(f"      - precio: {item.get('precio')}")
    else:
        print(f"   ❌ Item '{item_nombre}' NO encontrado en array embebido")
        print(f"   📝 Items en el array:")
        for item in items_array[:5]:  # Mostrar primeros 5
            print(f"      - {item.get('nombre')}")
else:
    print(f"   ❌ Categoría no encontrada")

# 4. Buscar en TODAS las categorías
print(f"\n4️⃣ BUSCANDO EN TODAS LAS CATEGORÍAS:")
todas_categorias = list(db.categorias_menu.find({}))
encontrado_en = []

for cat in todas_categorias:
    items = cat.get("items", [])
    for item in items:
        if item.get("nombre") == item_nombre:
            encontrado_en.append({
                'categoria_id': str(cat['_id']),
                'categoria_nombre': cat['nombre'],
                'item': item
            })

if encontrado_en:
    print(f"   ✅ Encontrado en {len(encontrado_en)} categoría(s):")
    for resultado in encontrado_en:
        print(f"\n   📁 Categoría: {resultado['categoria_nombre']}")
        print(f"      ID: {resultado['categoria_id']}")
        print(f"      Item: nombre={resultado['item'].get('nombre')}, precio={resultado['item'].get('precio')}")
else:
    print(f"   ❌ NO encontrado en ninguna categoría")

# 5. Comparar IDs
if item_sin_filtro:
    print(f"\n5️⃣ COMPARACIÓN DE IDs:")
    item_cat_id = item_sin_filtro.get('categoria_id')
    url_cat_id = ObjectId(categoria_id)
    
    print(f"   Item categoria_id: {item_cat_id} (tipo: {type(item_cat_id)})")
    print(f"   URL categoria_id:  {url_cat_id} (tipo: {type(url_cat_id)})")
    print(f"   ¿Son iguales? {item_cat_id == url_cat_id}")
    
    if item_cat_id != url_cat_id:
        print(f"\n   ⚠️ PROBLEMA ENCONTRADO:")
        print(f"   El item está en categoria_id={item_cat_id}")
        print(f"   Pero el frontend está usando categoria_id={categoria_id}")
        print(f"   El frontend debe usar la categoría correcta!")

print(f"\n{'='*60}\n")
