#!/usr/bin/env python3
"""
Script de migración para agregar campos de slogan a la base de datos
"""
from app.mongo_database import get_mongodb

def migrar_campos_slogan():
    """Agregar campos slogan y slogan_subtitulo a restaurante_info"""
    db = get_mongodb()
    
    print("🔄 Iniciando migración de campos de slogan...")
    
    # Verificar si ya existe el documento
    restaurante_info = db.restaurante_info.find_one()
    
    if restaurante_info:
        print(f"📊 Documento encontrado con ID: {restaurante_info['_id']}")
        
        # Verificar si ya tiene los campos
        tiene_slogan = 'slogan' in restaurante_info
        tiene_slogan_subtitulo = 'slogan_subtitulo' in restaurante_info
        
        if tiene_slogan and tiene_slogan_subtitulo:
            print("✅ Los campos ya existen en la base de datos:")
            print(f"   - slogan: {restaurante_info.get('slogan')}")
            print(f"   - slogan_subtitulo: {restaurante_info.get('slogan_subtitulo')}")
        else:
            # Preparar los campos a agregar
            campos_nuevos = {}
            
            if not tiene_slogan:
                campos_nuevos['slogan'] = "Donde cada plato cuenta una historia del mar"
                print("➕ Agregando campo 'slogan'")
            
            if not tiene_slogan_subtitulo:
                campos_nuevos['slogan_subtitulo'] = "Restaurante Dario, tradición veracruzana desde 1969"
                print("➕ Agregando campo 'slogan_subtitulo'")
            
            # Actualizar el documento
            if campos_nuevos:
                result = db.restaurante_info.update_one(
                    {"_id": restaurante_info["_id"]},
                    {"$set": campos_nuevos}
                )
                
                if result.modified_count > 0:
                    print(f"✅ Migración exitosa! {result.modified_count} documento(s) actualizado(s)")
                    print("\nCampos agregados:")
                    for key, value in campos_nuevos.items():
                        print(f"   - {key}: {value}")
                else:
                    print("⚠️  No se modificaron documentos (puede que ya existieran los valores)")
    else:
        print("📝 No existe documento de restaurante_info, creando uno nuevo...")
        nuevo_documento = {
            "nombre": "Dario Restaurante",
            "descripcion_corta": "Los mariscos más frescos del mar, preparados con pasión y tradición desde 1969",
            "descripcion_larga": "En Dario Restaurante, llevamos más de dos décadas dedicados a ofrecer la mejor experiencia gastronómica de mariscos. Nuestra pasión por los productos del mar nos ha convertido en el destino favorito para los amantes de los mariscos frescos.",
            "slogan": "Donde cada plato cuenta una historia del mar",
            "slogan_subtitulo": "Restaurante Dario, tradición veracruzana desde 1969",
            "logo_url": "/logo-cangrejo.png",
            "anos_experiencia": 20,
            "clientes_satisfechos": 10000,
            "platos_unicos": 50
        }
        
        result = db.restaurante_info.insert_one(nuevo_documento)
        print(f"✅ Documento creado con ID: {result.inserted_id}")
    
    print("\n🎉 Migración completada exitosamente!")
    print("\nPuedes verificar los cambios con:")
    print("  GET /api/restaurante/info-publica")
    print("  GET /api/admin/restaurante")

if __name__ == "__main__":
    migrar_campos_slogan()
