from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.mongo_database import get_mongodb, serialize_doc
from app.schemas.mongo_schemas import (
    RestauranteInfo, ContactoInfo, CaracteristicaRestaurante, 
    ServicioRestaurante, DatosRestauranteCompleto
)

router = APIRouter()

@router.get("/info", response_model=RestauranteInfo)
async def get_restaurante_info(db = Depends(get_mongodb)):
    """Obtener información general del restaurante"""
    try:
        info_doc = db.restaurante_info.find_one()
        if not info_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Información del restaurante no encontrada"
            )
        
        return serialize_doc(info_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo información del restaurante: {str(e)}"
        )

@router.get("/contacto", response_model=ContactoInfo)
async def get_contacto_info(db = Depends(get_mongodb)):
    """Obtener información de contacto del restaurante"""
    try:
        contacto_doc = db.contacto_info.find_one()
        if not contacto_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Información de contacto no encontrada"
            )
        
        return serialize_doc(contacto_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo información de contacto: {str(e)}"
        )

@router.get("/caracteristicas", response_model=List[CaracteristicaRestaurante])
async def get_caracteristicas(db = Depends(get_mongodb)):
    """Obtener características del restaurante"""
    try:
        caracteristicas_cursor = db.caracteristicas.find()
        caracteristicas = [serialize_doc(doc) for doc in caracteristicas_cursor]
        
        return caracteristicas
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo características: {str(e)}"
        )

@router.get("/servicios", response_model=List[ServicioRestaurante])
async def get_servicios(db = Depends(get_mongodb)):
    """Obtener servicios del restaurante"""
    try:
        servicios_cursor = db.servicios.find()
        servicios = [serialize_doc(doc) for doc in servicios_cursor]
        
        return servicios
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo servicios: {str(e)}"
        )

@router.get("/info-publica")
async def get_info_publica(db = Depends(get_mongodb)):
    """Obtener información pública del restaurante para el frontend"""
    try:
        # Obtener información básica del restaurante
        restaurante_info = db.restaurante_info.find_one()
        print(f"📊 DEBUG: Datos de restaurante encontrados: {restaurante_info is not None}")
        
        # Obtener información de contacto
        contacto_info = db.contacto_info.find_one()
        print(f"📞 DEBUG: Datos de contacto encontrados: {contacto_info is not None}")
        
        # Crear estructura base con valores por defecto
        info_completa = {
            "nombre": "Dario Restaurante",
            "descripcion_corta": "Los mariscos más frescos del mar, preparados con pasión y tradición desde 1969",
            "descripcion_larga": "En Dario Restaurante, llevamos más de dos décadas dedicados a ofrecer la mejor experiencia gastronómica de mariscos. Nuestra pasión por los productos del mar nos ha convertido en el destino favorito para los amantes de los mariscos frescos.",
            "telefono": "+52 229 109 6048",
            "whatsapp": "522291096048",
            "email": "restaurantedario1@outlook.com",
            "direccion": "Carr. Veracruz - Medellin km 2.5, Veracruz, Ver., México",
            "horarios": "Todos los días: 9:00 AM - 6:00 PM",
            "facebook": "https://facebook.com/dariorestaurante",
            "instagram": "https://instagram.com/dariorestaurante",
            "website": "https://dariorestaurante.com",
            "logo_url": "/logo-cangrejo.png",
            "imagen_banner_url": "https://images.unsplash.com/photo-1730698306944-544a5cb282e3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHNlYXJjaHwxfHxmcmVzaCUyMHNlYWZvb2QlMjBwbGF0dGVyJTIwc2hyaW1wJTIwbG9ic3RlcnxlbnwxfHx8fDE3NTgwNTg0NDd8MA&ixlib=rb-4.1.0&q=80&w=1080",
            "imagen_sobre_nosotros_url": "https://images.unsplash.com/photo-1667388968964-4aa652df0a9b?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHxyZXN0YXVyYW50JTIwaW50ZXJpb3IlMjBkaW5pbmd8ZW58MXx8fHwxNzU3MzcyODA1fDA&ixlib=rb-4.1.0&q=80&w=1080",
            "anos_experiencia": 20,
            "clientes_satisfechos": 10000,
            "platos_unicos": 50
        }
        
        # Aplicar datos de restaurante_info si existen
        if restaurante_info:
            for key, value in restaurante_info.items():
                if key != "_id" and key in info_completa:
                    # Corregir URLs específicas que están mal formateadas
                    if key == "logo_url" and value and "figma:asset" in str(value):
                        info_completa[key] = "/logo-cangrejo.png"
                    elif key == "imagen_banner_url" and value and "figma:asset" in str(value):
                        info_completa[key] = "https://images.unsplash.com/photo-1730698306944-544a5cb282e3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHNlYXJjaHwxfHxmcmVzaCUyMHNlYWZvb2QlMjBwbGF0dGVyJTIwc2hyaW1wJTIwbG9ic3RlcnxlbnwxfHx8fDE3NTgwNTg0NDd8MA&ixlib=rb-4.1.0&q=80&w=1080"
                    elif not isinstance(value, dict) and value:
                        info_completa[key] = value
        
        # Aplicar datos de contacto_info si existen
        if contacto_info:
            for key, value in contacto_info.items():
                if key != "_id" and key in info_completa:
                    # Convertir objetos complejos a strings
                    if key == "direccion" and isinstance(value, dict):
                        direccion_parts = []
                        if value.get("calle"): direccion_parts.append(value["calle"])
                        if value.get("ciudad"): direccion_parts.append(value["ciudad"])
                        if value.get("estado"): direccion_parts.append(value["estado"])
                        if value.get("pais"): direccion_parts.append(value["pais"])
                        if value.get("codigo_postal"): direccion_parts.append(value["codigo_postal"])
                        info_completa[key] = ", ".join(direccion_parts) if direccion_parts else info_completa[key]
                    elif key == "horarios" and isinstance(value, dict):
                        if value.get("todos_los_dias"):
                            info_completa[key] = value["todos_los_dias"]
                    elif not isinstance(value, dict) and value:
                        info_completa[key] = value
        
        print(f"✅ DEBUG: Información pública preparada")
        return info_completa
        
    except Exception as e:
        print(f"❌ DEBUG: Error en get_info_publica: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener información pública: {str(e)}"
        )

@router.get("/menu-publico")
async def get_menu_publico():
    """Obtener menú público del restaurante para el frontend - usando ambas colecciones"""
    try:
        from app.mongo_database import get_mongodb
        from bson import ObjectId
        
        db = get_mongodb()
        count = db.categorias_menu.count_documents({})
        
        if count > 0:
            # Obtener todas las categorías activas de categorias_menu
            categorias = list(db.categorias_menu.find({"activo": {"$ne": False}}))
            
            menu_publico = []
            for cat in categorias:
                # Obtener items de esta categoría desde items_menu
                items_cursor = db.items_menu.find({"categoria_id": ObjectId(cat["_id"])})
                items_list = []
                
                for item in items_cursor:
                    if item.get("disponible", True):  # Solo items disponibles
                        items_list.append({
                            "id": str(item["_id"]),
                            "nombre": item.get("nombre", ""),
                            "descripcion": item.get("descripcion", ""),
                            "precio": item.get("precio", 0),
                            "disponible": item.get("disponible", True),
                            "categoria_id": str(cat["_id"]),
                            "categoria_nombre": cat.get("nombre", ""),
                            "orden": item.get("orden", 0)
                        })
                
                # Ordenar items por orden
                items_list.sort(key=lambda x: x.get("orden", 0))
                
                categoria_publico = {
                    "id": str(cat["_id"]),
                    "nombre": cat.get("nombre", "Sin nombre"),
                    "descripcion": cat.get("descripcion", ""),
                    "imagen_url_original": cat.get("imagen_url_original", ""),
                    "color": cat.get("color", "#10B981"),
                    "icono": cat.get("icono", "🍽️"),
                    "orden": cat.get("orden", 0),
                    "activo": cat.get("activo", True),
                    "items": items_list
                }
                
                menu_publico.append(categoria_publico)
            
            # Ordenar categorías por orden
            menu_publico.sort(key=lambda x: x.get("orden", 0))
            
            total_items = sum(len(cat["items"]) for cat in menu_publico)
            
            return {
                "categorias": menu_publico,
                "total_categorias": len(menu_publico),
                "total_items": total_items,
                "mensaje": "Menú completo cargado desde MongoDB"
            }
        else:
            return {
                "categorias": [],
                "total_categorias": 0,
                "total_items": 0,
                "mensaje": "No hay categorías en la base de datos"
            }
            
    except Exception as e:
        import traceback
        print(f"❌ ERROR en menu-publico: {str(e)}")
        print(f"❌ TRACEBACK: {traceback.format_exc()}")
        return {
            "categorias": [],
            "total_categorias": 0,
            "total_items": 0,
            "error": str(e),
            "mensaje": "Error al cargar menú desde MongoDB"
        }

@router.get("/datos-completos", response_model=DatosRestauranteCompleto)
async def get_datos_completos(db = Depends(get_mongodb)):
    """Obtener todos los datos del restaurante en una sola consulta"""
    try:
        # Obtener información del restaurante
        info_doc = db.restaurante_info.find_one()
        if not info_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Información del restaurante no encontrada"
            )
        
        # Obtener información de contacto
        contacto_doc = db.contacto_info.find_one()
        if not contacto_doc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Información de contacto no encontrada"
            )
        
        # Obtener características
        caracteristicas_cursor = db.caracteristicas.find()
        caracteristicas = [serialize_doc(doc) for doc in caracteristicas_cursor]
        
        # Obtener servicios
        servicios_cursor = db.servicios.find()
        servicios = [serialize_doc(doc) for doc in servicios_cursor]
        
        return {
            "restaurante": serialize_doc(info_doc),
            "contacto": serialize_doc(contacto_doc),
            "caracteristicas": caracteristicas,
            "servicios": servicios
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo datos completos: {str(e)}"
        )

@router.get("/menu-publico-test")
async def get_menu_publico_test():
    """Test endpoint para verificar que funciona"""
    try:
        from app.mongo_database import get_mongodb
        from bson import ObjectId
        
        db = get_mongodb()
        count = db.categorias_menu.count_documents({})
        
        if count > 0:
            # Obtener todas las categorías activas
            categorias = list(db.categorias_menu.find({"activo": {"$ne": False}}))
            
            menu_test = []
            for cat in categorias:
                # Obtener items de esta categoría desde items_menu
                items_cursor = db.items_menu.find({"categoria_id": ObjectId(cat["_id"])})
                items_list = []
                
                for item in items_cursor:
                    if item.get("disponible", True):  # Solo items disponibles
                        items_list.append({
                            "id": str(item["_id"]),
                            "nombre": item.get("nombre", ""),
                            "descripcion": item.get("descripcion", ""),
                            "precio": item.get("precio", 0),
                            "disponible": item.get("disponible", True),
                            "categoria_id": str(cat["_id"]),
                            "categoria_nombre": cat.get("nombre", ""),
                            "orden": item.get("orden", 0)
                        })
                
                # Ordenar items por orden
                items_list.sort(key=lambda x: x.get("orden", 0))
                
                categoria_test = {
                    "id": str(cat["_id"]),
                    "nombre": cat.get("nombre", "Sin nombre"),
                    "descripcion": cat.get("descripcion", ""),
                    "imagen_url_original": cat.get("imagen_url_original", ""),
                    "color": cat.get("color", "#10B981"),
                    "icono": cat.get("icono", "🍽️"),
                    "orden": cat.get("orden", 0),
                    "activo": cat.get("activo", True),
                    "items": items_list
                }
                
                menu_test.append(categoria_test)
            
            # Ordenar categorías por orden
            menu_test.sort(key=lambda x: x.get("orden", 0))
            
            total_items = sum(len(cat["items"]) for cat in menu_test)
            
            return {
                "categorias": menu_test,
                "total_categorias": len(menu_test),
                "total_items": total_items,
                "mensaje": "Menú completo desde test endpoint"
            }
        else:
            return {
                "categorias": [],
                "total_categorias": 0,
                "total_items": 0,
                "mensaje": "No hay categorías en DB"
            }
            
    except Exception as e:
        import traceback
        return {
            "categorias": [],
            "total_categorias": 0,
            "total_items": 0,
            "error": str(e),
            "traceback": traceback.format_exc()
        }

@router.get("/menu-publico")
async def get_menu_publico():
    """Obtener menú público del restaurante para el frontend"""
    print("🚀 INICIO: Endpoint menu-publico llamado")
    
    try:
        from app.mongo_database import get_mongodb
        from bson import ObjectId
        
        print("📦 Importaciones exitosas")
        
        db = get_mongodb()
        print("🔗 Conexión a DB obtenida")
        
        # Test simple: solo contar categorías
        count = db.categorias_menu.count_documents({})
        print(f"� Conteo total: {count}")
        
        if count == 0:
            return {"categorias": [], "total_categorias": 0, "mensaje": "No hay categorías"}
        
        # Obtener solo las primeras 3 categorías para debug
        categorias = list(db.categorias_menu.find().limit(3))
        print(f"🔍 Categorías obtenidas: {len(categorias)}")
        
        menu_simple = []
        for cat in categorias:
            cat_simple = {
                "id": str(cat["_id"]),
                "nombre": cat.get("nombre", "Sin nombre"),
                "orden": cat.get("orden", 0),
                "activo": cat.get("activo", True),
                "items": []
            }
            
            # Obtener items de esta categoría
            items_count = db.items_menu.count_documents({"categoria_id": ObjectId(cat["_id"])})
            print(f"� {cat_simple['nombre']}: {items_count} items")
            
            # Si está activa, agregarla
            if cat_simple["activo"]:
                menu_simple.append(cat_simple)
                print(f"✅ Agregada: {cat_simple['nombre']}")
            else:
                print(f"❌ Saltada (inactiva): {cat_simple['nombre']}")
        
        print(f"🎯 Resultado: {len(menu_simple)} categorías activas")
        
        return {
            "categorias": menu_simple,
            "total_categorias": len(menu_simple),
            "total_items": 0,
            "debug": "Versión simplificada funcionando"
        }
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return {
            "categorias": [],
            "total_categorias": 0,
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        
    except Exception as e:
        print(f"❌ DEBUG: Error en get_menu_publico: {str(e)}")
        print(f"❌ DEBUG: Tipo de error: {type(e)}")
        import traceback
        traceback.print_exc()
        
        # Devolver menú por defecto en caso de error
        return {
            "categorias": [
                {
                    "id": "default_1",
                    "nombre": "Mariscos Frescos",
                    "descripcion": "Los mejores mariscos del día",
                    "imagen_url": "https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80",
                    "color": "#10B981",
                    "icono": "🦐",
                    "orden": 1,
                    "activo": True,
                    "items": [
                        {
                            "id": "default_item_1",
                            "nombre": "Camarones al Ajo",
                            "descripcion": "Camarones frescos salteados con ajo y especias",
                            "precio": 280,
                            "imagen_url": "",
                            "disponible": True,
                            "categoria_id": "default_1",
                            "categoria_nombre": "Mariscos Frescos",
                            "orden": 1
                        }
                    ]
                }
            ],
            "total_categorias": 1,
            "total_items": 1
        }