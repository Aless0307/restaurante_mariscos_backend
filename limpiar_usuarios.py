#!/usr/bin/env python3
"""
Script para eliminar todos los usuarios excepto restaurantedario@restaurante.com
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.mongo_database import get_mongodb

def limpiar_usuarios():
    """Eliminar todos los usuarios excepto restaurantedario"""
    try:
        db = get_mongodb()
        
        print("="*60)
        print("🗑️  LIMPIEZA DE USUARIOS")
        print("="*60)
        print()
        
        # Listar usuarios actuales
        usuarios = list(db.usuarios.find({}))
        print(f"📊 Total de usuarios actuales: {len(usuarios)}")
        print()
        
        for user in usuarios:
            email = user.get('email', 'N/A')
            nombre = user.get('nombre', 'N/A')
            es_admin = user.get('es_admin', False)
            print(f"   - {email} ({nombre}) - Admin: {es_admin}")
        
        print()
        print("="*60)
        
        # Confirmar
        print("⚠️  ATENCIÓN: Se eliminarán TODOS los usuarios EXCEPTO:")
        print("   📧 restaurantedario@restaurante.com")
        print()
        respuesta = input("¿Estás seguro? Escribe 'SI' para continuar: ")
        
        if respuesta != "SI":
            print("\n❌ Operación cancelada")
            return
        
        # Eliminar todos excepto restaurantedario
        resultado = db.usuarios.delete_many({
            "email": {"$ne": "restaurantedario@restaurante.com"}
        })
        
        print()
        print("="*60)
        print(f"✅ {resultado.deleted_count} usuario(s) eliminado(s)")
        print("="*60)
        print()
        
        # Listar usuarios restantes
        usuarios_restantes = list(db.usuarios.find({}))
        print(f"📊 Usuarios restantes: {len(usuarios_restantes)}")
        print()
        
        for user in usuarios_restantes:
            email = user.get('email', 'N/A')
            nombre = user.get('nombre', 'N/A')
            es_admin = user.get('es_admin', False)
            activo = user.get('activo', False)
            print(f"   ✅ {email}")
            print(f"      Nombre: {nombre}")
            print(f"      Admin: {es_admin}")
            print(f"      Activo: {activo}")
        
        print()
        print("="*60)
        print("✅ Limpieza completada exitosamente")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    limpiar_usuarios()
