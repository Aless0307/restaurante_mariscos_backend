#!/usr/bin/env python3
"""
Script para listar todas las rutas registradas en FastAPI
"""

from main import app

print("="*80)
print("📋 RUTAS REGISTRADAS EN FASTAPI")
print("="*80)

rutas_admin = []
todas_rutas = []

for route in app.routes:
    if hasattr(route, 'methods') and hasattr(route, 'path'):
        path = route.path
        methods = ', '.join(route.methods)
        todas_rutas.append((methods, path))
        
        if '/admin/' in path:
            rutas_admin.append((methods, path))

print(f"\n🔍 Total de rutas: {len(todas_rutas)}")
print(f"🔧 Rutas de admin: {len(rutas_admin)}")

print("\n" + "="*80)
print("🔧 RUTAS DE ADMINISTRACIÓN")
print("="*80)

for methods, path in sorted(rutas_admin):
    print(f"{methods:30} {path}")

print("\n" + "="*80)
print("🔍 BUSCANDO RUTA DE REORDENAR")
print("="*80)

encontrada = False
for methods, path in todas_rutas:
    if 'reordenar' in path.lower():
        print(f"✅ ENCONTRADA: {methods:20} {path}")
        encontrada = True

if not encontrada:
    print("❌ NO SE ENCONTRÓ la ruta de reordenar-items")
    print("\n💡 Esto significa que:")
    print("   1. El servidor necesita reiniciarse")
    print("   2. O hay un error de sintaxis que impide el registro")
    
print("\n" + "="*80)
