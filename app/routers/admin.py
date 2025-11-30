from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import StreamingResponse
from typing import List, Optional
from datetime import datetime
from app.mongo_database import get_mongo_db
from app.schemas.auth_schemas import UsuarioMongo
from app.schemas.mongo_schemas import *
from app.services.auth_mongo_simple import AuthService
from app.cache import cache
import gridfs
from bson import ObjectId
import io
from PIL import Image

router = APIRouter()

# Helper para limpiar caché del menú
def limpiar_cache_menu():
    """Limpia todo el caché relacionado con el menú"""
    cache.delete("menu_publico_completo")
    cache.invalidate_pattern("menu_")
    cache.invalidate_pattern("categoria_")
    print("🗑️ Caché del menú limpiado completamente")

# =============================================================================
# ENDPOINTS DE GESTIÓN DE INFORMACIÓN DEL RESTAURANTE
# =============================================================================

@router.get("/restaurante")
async def obtener_info_restaurante(
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Obtener información del restaurante"""
    try:
        print("🔍 DEBUG: Buscando información del restaurante en la base de datos...")
        
        # Obtener información básica del restaurante
        restaurante_info = db.restaurante_info.find_one()
        print(f"📊 DEBUG: Datos de restaurante encontrados: {restaurante_info is not None}")
        if restaurante_info:
            print(f"📋 DEBUG: Estructura completa de restaurante_info: {restaurante_info}")
        
        # Obtener información de contacto
        contacto_info = db.contacto_info.find_one()
        print(f"📊 DEBUG: Datos de contacto encontrados: {contacto_info is not None}")
        if contacto_info:
            print(f"📋 DEBUG: Estructura completa de contacto_info: {contacto_info}")
        
        # Crear estructura base con valores por defecto más completos
        info_completa = {
            "nombre": "Dario Restaurante",
            "descripcion_corta": "Los mariscos más frescos del mar, preparados con pasión y tradición desde 1969",
            "descripcion_larga": "En Dario Restaurante, llevamos más de dos décadas dedicados a ofrecer la mejor experiencia gastronómica de mariscos. Nuestra pasión por los productos del mar nos ha convertido en el destino favorito para los amantes de los mariscos frescos.",
            "slogan": "Donde cada plato cuenta una historia del mar",
            "slogan_subtitulo": "Restaurante Dario, tradición veracruzana desde 1969",
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
                        # Forzar actualización del logo a la ruta correcta
                        print(f"🔧 DEBUG: Corrigiendo logo_url de '{value}' a '/logo-cangrejo.png'")
                        info_completa[key] = "/logo-cangrejo.png"
                        # Actualizar en la base de datos también
                        db.restaurante_info.update_one(
                            {"_id": restaurante_info["_id"]},
                            {"$set": {"logo_url": "/logo-cangrejo.png"}}
                        )
                    elif key == "imagen_banner_url" and value and "figma:asset" in str(value):
                        # Forzar actualización del banner a la URL de Unsplash
                        banner_url = "https://images.unsplash.com/photo-1730698306944-544a5cb282e3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHNlYXJjaHwxfHxmcmVzaCUyMHNlYWZvb2QlMjBwbGF0dGVyJTIwc2hyaW1wJTIwbG9ic3RlcnxlbnwxfHx8fDE3NTgwNTg0NDd8MA&ixlib=rb-4.1.0&q=80&w=1080"
                        print(f"🔧 DEBUG: Corrigiendo imagen_banner_url de '{value}' a '{banner_url}'")
                        info_completa[key] = banner_url
                        # Actualizar en la base de datos también
                        db.restaurante_info.update_one(
                            {"_id": restaurante_info["_id"]},
                            {"$set": {"imagen_banner_url": banner_url}}
                        )
                    # Convertir objetos complejos a strings si es necesario
                    elif key == "direccion" and isinstance(value, dict):
                        # Convertir objeto dirección a string
                        direccion_parts = []
                        if value.get("calle"):
                            direccion_parts.append(value["calle"])
                        if value.get("ciudad"):
                            direccion_parts.append(value["ciudad"])
                        if value.get("estado"):
                            direccion_parts.append(value["estado"])
                        if value.get("pais"):
                            direccion_parts.append(value["pais"])
                        if value.get("codigo_postal"):
                            direccion_parts.append(value["codigo_postal"])
                        info_completa[key] = ", ".join(direccion_parts) if direccion_parts else info_completa[key]
                    elif key == "horarios" and isinstance(value, dict):
                        # Convertir objeto horarios a string
                        if value.get("todos_los_dias"):
                            info_completa[key] = value["todos_los_dias"]
                        else:
                            # Si tiene horarios específicos por día, crear un string descriptivo
                            horarios_desc = []
                            dias_map = {
                                "lunes": "Lunes",
                                "martes": "Martes", 
                                "miercoles": "Miércoles",
                                "jueves": "Jueves",
                                "viernes": "Viernes",
                                "sabado": "Sábado",
                                "domingo": "Domingo"
                            }
                            for dia, horario in value.items():
                                if dia in dias_map and horario:
                                    horarios_desc.append(f"{dias_map[dia]}: {horario}")
                            info_completa[key] = "; ".join(horarios_desc) if horarios_desc else info_completa[key]
                    else:
                        # Solo sobrescribir si el valor no está vacío y no es un objeto complejo
                        if value and str(value).strip() and not isinstance(value, dict):
                            info_completa[key] = value
        
        # Aplicar datos de contacto_info si existen
        if contacto_info:
            print("📞 DEBUG: Aplicando información de contacto encontrada")
            for key, value in contacto_info.items():
                if key != "_id" and key in info_completa:
                    # Corregir URLs específicas que están mal formateadas
                    if key == "logo_url" and value and "figma:asset" in str(value):
                        # Forzar actualización del logo a la ruta correcta
                        print(f"🔧 DEBUG: Corrigiendo logo_url en contacto de '{value}' a '/logo-cangrejo.png'")
                        info_completa[key] = "/logo-cangrejo.png"
                        # Actualizar en la base de datos también
                        db.contacto_info.update_one(
                            {"_id": contacto_info["_id"]},
                            {"$set": {"logo_url": "/logo-cangrejo.png"}}
                        )
                    elif key == "imagen_banner_url" and value and "figma:asset" in str(value):
                        # Forzar actualización del banner a la URL de Unsplash
                        banner_url = "https://images.unsplash.com/photo-1730698306944-544a5cb282e3?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w3Nzg4Nzd8MHwxfHNlYXJjaHwxfHNlYXJjaHwxfHxmcmVzaCUyMHNlYWZvb2QlMjBwbGF0dGVyJTIwc2hyaW1wJTIwbG9ic3RlcnxlbnwxfHx8fDE3NTgwNTg0NDd8MA&ixlib=rb-4.1.0&q=80&w=1080"
                        print(f"🔧 DEBUG: Corrigiendo imagen_banner_url en contacto de '{value}' a '{banner_url}'")
                        info_completa[key] = banner_url
                        # Actualizar en la base de datos también
                        db.contacto_info.update_one(
                            {"_id": contacto_info["_id"]},
                            {"$set": {"imagen_banner_url": banner_url}}
                        )
                    # Convertir objetos complejos a strings
                    elif key == "direccion" and isinstance(value, dict):
                        # Convertir objeto dirección a string
                        direccion_parts = []
                        if value.get("calle"):
                            direccion_parts.append(value["calle"])
                        if value.get("ciudad"):
                            direccion_parts.append(value["ciudad"])
                        if value.get("estado"):
                            direccion_parts.append(value["estado"])
                        if value.get("pais"):
                            direccion_parts.append(value["pais"])
                        if value.get("codigo_postal"):
                            direccion_parts.append(value["codigo_postal"])
                        info_completa[key] = ", ".join(direccion_parts) if direccion_parts else info_completa[key]
                    elif key == "horarios" and isinstance(value, dict):
                        # Convertir objeto horarios a string
                        if value.get("todos_los_dias"):
                            info_completa[key] = value["todos_los_dias"]
                        else:
                            # Si tiene horarios específicos por día, crear un string descriptivo
                            horarios_desc = []
                            dias_map = {
                                "lunes": "Lunes",
                                "martes": "Martes", 
                                "miercoles": "Miércoles",
                                "jueves": "Jueves",
                                "viernes": "Viernes",
                                "sabado": "Sábado",
                                "domingo": "Domingo"
                            }
                            for dia, horario in value.items():
                                if dia in dias_map and horario:
                                    horarios_desc.append(f"{dias_map[dia]}: {horario}")
                            info_completa[key] = "; ".join(horarios_desc) if horarios_desc else info_completa[key]
                    else:
                        # Solo sobrescribir si el valor no está vacío y es string/número
                        if value and str(value).strip() and not isinstance(value, dict):
                            info_completa[key] = value
        
        # Convertir ObjectId a string y agregar _id
        if restaurante_info:
            info_completa["_id"] = str(restaurante_info["_id"])
        elif contacto_info:
            info_completa["_id"] = str(contacto_info["_id"])
        
        print(f"✅ DEBUG: Información combinada final: {info_completa}")
        
        return info_completa
    except Exception as e:
        print(f"❌ DEBUG: Error en obtener_info_restaurante: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener información del restaurante: {str(e)}"
        )

@router.put("/restaurante", response_model=dict)
async def actualizar_info_restaurante(
    info_update: RestauranteInfoUpdate,
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Actualizar información del restaurante"""
    try:
        print(f"🔄 DEBUG: Actualizando información del restaurante...")
        
        update_data = info_update.dict(exclude_unset=True)
        print(f"📝 DEBUG: Datos recibidos para actualizar: {update_data}")
        
        # Separar campos por colección
        campos_restaurante = ["nombre", "descripcion_corta", "descripcion_larga", "slogan", "slogan_subtitulo", "logo_url", "imagen_banner_url", "imagen_sobre_nosotros_url", "anos_experiencia", "clientes_satisfechos", "platos_unicos"]
        campos_contacto = ["telefono", "whatsapp", "email", "direccion", "horarios", "facebook", "instagram", "website"]
        
        # Datos para restaurante_info
        datos_restaurante = {k: v for k, v in update_data.items() if k in campos_restaurante}
        
        # Datos para contacto_info  
        datos_contacto = {k: v for k, v in update_data.items() if k in campos_contacto}
        
        print(f"📊 DEBUG: Datos para restaurante_info: {datos_restaurante}")
        print(f"📞 DEBUG: Datos para contacto_info: {datos_contacto}")
        
        # Actualizar restaurante_info si hay datos para esa colección
        if datos_restaurante:
            info_existente = db.restaurante_info.find_one()
            if info_existente:
                result = db.restaurante_info.update_one(
                    {"_id": info_existente["_id"]},
                    {"$set": datos_restaurante}
                )
                print(f"✅ DEBUG: restaurante_info actualizado: {result.modified_count} documentos")
            else:
                result = db.restaurante_info.insert_one(datos_restaurante)
                print(f"✅ DEBUG: restaurante_info creado con ID: {result.inserted_id}")
        
        # Actualizar contacto_info si hay datos para esa colección
        if datos_contacto:
            contacto_existente = db.contacto_info.find_one()
            if contacto_existente:
                result = db.contacto_info.update_one(
                    {"_id": contacto_existente["_id"]},
                    {"$set": datos_contacto}
                )
                print(f"✅ DEBUG: contacto_info actualizado: {result.modified_count} documentos")
            else:
                result = db.contacto_info.insert_one(datos_contacto)
                print(f"✅ DEBUG: contacto_info creado con ID: {result.inserted_id}")
        
        # Limpiar caché de información pública
        cache.delete("restaurante_info_publica")
        print("🗑️ Caché de información pública limpiado")
        
        return {
            "message": "Información del restaurante actualizada exitosamente",
            "campos_actualizados": list(update_data.keys())
        }
    except Exception as e:
        print(f"❌ DEBUG: Error actualizando información: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar información del restaurante: {str(e)}"
        )

# =============================================================================
# ENDPOINTS DE GESTIÓN DE MENÚ (MongoDB)
# =============================================================================

@router.get("/categorias")
async def obtener_categorias_admin(
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Obtener todas las categorías para administración"""
    try:
        # Obtener categorías
        categorias = list(db.categorias_menu.find().sort("orden", 1))
        
        # Agregar conteo de items y convertir ObjectId a string
        categorias_con_items = []
        for categoria in categorias:
            categoria["_id"] = str(categoria["_id"])
            categoria["id"] = categoria["_id"]
            
            # Generar imagen_url basada en imagen_url_original
            if categoria.get("imagen_url_original"):
                # Si es una URL completa (externa), usarla directamente
                if categoria["imagen_url_original"].startswith(("http://", "https://")):
                    categoria["imagen_url"] = categoria["imagen_url_original"]
                else:
                    # Si es un ID de GridFS, generar la URL del endpoint
                    categoria["imagen_url"] = f"/api/imagenes/{categoria['imagen_url_original']}"
            else:
                categoria["imagen_url"] = None
            
            # Obtener items de AMBOS lugares para mostrar todos
            # 1. Items almacenados dentro del documento de la categoría (nuevos)
            items_en_categoria = categoria.get("items", [])
            print(f"🔍 DEBUG: Categoría '{categoria['nombre']}' - Items en documento: {len(items_en_categoria)}")
            
            # 2. Items almacenados en la colección separada items_menu (existentes)
            from bson import ObjectId
            categoria_objectid = ObjectId(categoria["_id"])
            items_cursor = db.items_menu.find({"categoria_id": categoria_objectid}).sort("orden", 1)
            items_en_coleccion = []
            
            for item in items_cursor:
                item["_id"] = str(item["_id"])
                item["categoria_id"] = str(item["categoria_id"])
                items_en_coleccion.append(item)
            
            print(f"🔍 DEBUG: Categoría '{categoria['nombre']}' - Items en colección: {len(items_en_coleccion)}")
            
            # 3. Combinar ambos tipos de items
            todos_los_items = []
            
            # Agregar items de la colección separada primero (mantener orden original)
            todos_los_items.extend(items_en_coleccion)
            
            # Agregar items del documento de categoría
            for item in items_en_categoria:
                if "_id" in item:
                    item["_id"] = str(item["_id"])
                if "categoria_id" in item:
                    item["categoria_id"] = str(item["categoria_id"])
                todos_los_items.append(item)
            
            print(f"✅ DEBUG: Categoría '{categoria['nombre']}' - Total items combinados: {len(todos_los_items)}")
            
            # Asignar todos los items combinados y el conteo total
            categoria["items"] = todos_los_items
            categoria["total_items"] = len(todos_los_items)
            
            categorias_con_items.append(categoria)
        
        return categorias_con_items
    except Exception as e:
        print(f"Error en obtener_categorias_admin: {str(e)}")  # Debug
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener categorías: {str(e)}"
        )

@router.post("/categorias", response_model=dict)
async def crear_categoria(
    categoria: CategoriaMenuMongoCreate,
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Crear nueva categoría"""
    try:
        # Verificar que no exista una categoría con el mismo nombre
        if db.categorias_menu.find_one({"nombre": categoria.nombre}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una categoría con ese nombre"
            )
        
        # Obtener el siguiente orden
        ultima_categoria = db.categorias_menu.find_one(sort=[("orden", -1)])
        siguiente_orden = (ultima_categoria["orden"] + 1) if ultima_categoria else 1
        
        categoria_dict = categoria.dict()
        categoria_dict["orden"] = siguiente_orden
        categoria_dict["activo"] = True
        
        result = db.categorias_menu.insert_one(categoria_dict)
        
        # Limpiar caché del menú
        limpiar_cache_menu()
        
        return {
            "message": "Categoría creada exitosamente",
            "id": str(result.inserted_id)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear categoría: {str(e)}"
        )

@router.put("/categorias/{categoria_id}", response_model=dict)
async def actualizar_categoria(
    categoria_id: str,
    categoria: CategoriaMenuMongoUpdate,
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Actualizar categoría existente"""
    try:
        # Verificar que la categoría existe
        if not db.categorias_menu.find_one({"_id": ObjectId(categoria_id)}):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )
        
        # Preparar datos para actualizar (solo campos no nulos)
        update_data = {k: v for k, v in categoria.dict().items() if v is not None}
        
        if update_data:
            result = db.categorias_menu.update_one(
                {"_id": ObjectId(categoria_id)},
                {"$set": update_data}
            )
            
            if result.modified_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se realizaron cambios"
                )
        
        # Limpiar caché del menú
        limpiar_cache_menu()
        
        return {"message": "Categoría actualizada exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar categoría: {str(e)}"
        )

@router.delete("/categorias/{categoria_id}", response_model=dict)
async def eliminar_categoria(
    categoria_id: str,
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Eliminar categoría completamente junto con todos sus items"""
    try:
        # Verificar que la categoría existe
        categoria = db.categorias_menu.find_one({"_id": ObjectId(categoria_id)})
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )
        
        print(f"🗑️ DEBUG: Eliminando categoría '{categoria['nombre']}' con ID: {categoria_id}")
        
        # 1. Eliminar todos los items asociados de la colección items_menu
        items_eliminados = db.items_menu.delete_many({"categoria_id": ObjectId(categoria_id)})
        print(f"🗑️ DEBUG: Eliminados {items_eliminados.deleted_count} items de la colección items_menu")
        
        # 2. Eliminar la categoría completa del documento
        result = db.categorias_menu.delete_one({"_id": ObjectId(categoria_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No se pudo eliminar la categoría"
            )
        
        print(f"✅ DEBUG: Categoría '{categoria['nombre']}' eliminada completamente")
        
        # Limpiar caché del menú
        limpiar_cache_menu()
        
        return {
            "message": "Categoría eliminada exitosamente",
            "categoria_eliminada": categoria['nombre'],
            "items_eliminados": items_eliminados.deleted_count
        }
    except Exception as e:
        print(f"❌ DEBUG: Error al eliminar categoría: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar categoría: {str(e)}"
        )

# =============================================================================
# ENDPOINTS DE GESTIÓN DE ITEMS
# =============================================================================

@router.get("/items/{categoria_id}", response_model=List[ItemMenuMongo])
async def obtener_items_categoria_admin(
    categoria_id: str,
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Obtener todos los items de una categoría para administración"""
    try:
        categoria = db.categorias_menu.find_one({"_id": ObjectId(categoria_id)})
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )
        
        items = categoria.get("items", [])
        return [ItemMenuMongo(**item) for item in items]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener items: {str(e)}"
        )

@router.post("/categorias/{categoria_id}/items", response_model=dict)
async def crear_item(
    categoria_id: str,
    item: CrearItemMenu,
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Crear nuevo item en una categoría"""
    try:
        # Verificar que la categoría existe
        categoria = db.categorias_menu.find_one({"_id": ObjectId(categoria_id)})
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )
        
        # Obtener el siguiente orden basándose en items existentes en la colección items_menu
        ultimo_item = db.items_menu.find_one(
            {"categoria_id": ObjectId(categoria_id)},
            sort=[("orden", -1)]
        )
        siguiente_orden = 1 if not ultimo_item else ultimo_item.get("orden", 0) + 1
        
        item_dict = item.dict()
        item_dict["categoria_id"] = ObjectId(categoria_id)  # Mantener como ObjectId para consistencia
        item_dict["categoria_nombre"] = categoria["nombre"]
        item_dict["orden"] = siguiente_orden
        item_dict["fecha_creacion"] = datetime.now()
        item_dict["fecha_actualizacion"] = datetime.now()
        
        print(f"🔍 DEBUG: Creando item en colección items_menu: {item_dict['nombre']} para categoría {categoria['nombre']}")
        
        # Insertar el item en la colección items_menu
        result = db.items_menu.insert_one(item_dict)
        
        if not result.inserted_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se pudo crear el item"
            )
        
        print(f"✅ DEBUG: Item creado con ID: {result.inserted_id}")
        
        # Limpiar caché del menú
        limpiar_cache_menu()
        
        return {"message": "Item creado exitosamente", "item_id": str(result.inserted_id)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al crear item: {str(e)}"
        )

@router.put("/categorias/{categoria_id}/items/{item_nombre}", response_model=dict)
async def actualizar_item(
    categoria_id: str,
    item_nombre: str,
    item: ActualizarItemMenu,
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Actualizar item existente - Busca en ambos almacenamientos y permite cambio de categoría"""
    try:
        print(f"🔄 DEBUG: Actualizando item '{item_nombre}' en categoría {categoria_id}")
        
        # Verificar que la categoría actual existe
        categoria_actual = db.categorias_menu.find_one({"_id": ObjectId(categoria_id)})
        if not categoria_actual:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría actual no encontrada"
            )
        
        # Preparar datos para actualizar
        update_data = {k: v for k, v in item.dict().items() if v is not None}
        update_data["fecha_actualizacion"] = datetime.now()
        
        # Verificar si se está cambiando de categoría
        nueva_categoria_id = update_data.pop("categoria_id", None)
        cambio_categoria = nueva_categoria_id and nueva_categoria_id != categoria_id
        
        if cambio_categoria:
            print(f"🔀 DEBUG: Cambiando item de categoría {categoria_id} a {nueva_categoria_id}")
            
            # Verificar que la nueva categoría existe
            nueva_categoria = db.categorias_menu.find_one({"_id": ObjectId(nueva_categoria_id)})
            if not nueva_categoria:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Nueva categoría no encontrada"
                )
            
            # Actualizar categoria_nombre con el nombre de la nueva categoría
            update_data["categoria_nombre"] = nueva_categoria["nombre"]
        
        print(f"📝 DEBUG: Datos a actualizar: {update_data}")
        
        items_actualizados = 0
        
        # 1. Buscar y actualizar en la colección items_menu
        item_en_coleccion = db.items_menu.find_one({
            "categoria_id": ObjectId(categoria_id),
            "nombre": item_nombre
        })
        
        if item_en_coleccion:
            print(f"✅ DEBUG: Item encontrado en colección items_menu")
            
            if cambio_categoria:
                # Si cambia de categoría, actualizar el categoria_id
                update_data["categoria_id"] = ObjectId(nueva_categoria_id)
            
            result = db.items_menu.update_one(
                {"_id": item_en_coleccion["_id"]},
                {"$set": update_data}
            )
            if result.modified_count > 0:
                items_actualizados += 1
                print(f"✅ DEBUG: Item actualizado en colección items_menu")
        else:
            print(f"⚠️ DEBUG: Item NO encontrado en colección items_menu")
        
        # 2. Buscar y actualizar/mover en el array embebido de la categoría
        items = categoria_actual.get("items", [])
        item_index = -1
        item_encontrado = None
        
        for i, item_actual in enumerate(items):
            if item_actual.get("nombre") == item_nombre:
                item_index = i
                item_encontrado = item_actual.copy()
                break
        
        if item_index != -1:
            print(f"✅ DEBUG: Item encontrado en array embebido en índice {item_index}")
            
            if cambio_categoria:
                # Mover item a nueva categoría en array embebido
                print(f"🔀 DEBUG: Moviendo item en arrays embebidos")
                
                # Actualizar datos del item
                item_encontrado.update(update_data)
                
                # Eliminar de categoría actual
                db.categorias_menu.update_one(
                    {"_id": ObjectId(categoria_id)},
                    {"$pull": {"items": {"nombre": item_nombre}}}
                )
                
                # Agregar a nueva categoría
                db.categorias_menu.update_one(
                    {"_id": ObjectId(nueva_categoria_id)},
                    {"$push": {"items": item_encontrado}}
                )
                
                items_actualizados += 1
                print(f"✅ DEBUG: Item movido en arrays embebidos")
            else:
                # Solo actualizar en la misma categoría
                set_operations = {}
                for key, value in update_data.items():
                    set_operations[f"items.{item_index}.{key}"] = value
                
                result = db.categorias_menu.update_one(
                    {"_id": ObjectId(categoria_id)},
                    {"$set": set_operations}
                )
                if result.modified_count > 0:
                    items_actualizados += 1
                    print(f"✅ DEBUG: Item actualizado en array embebido")
        else:
            print(f"⚠️ DEBUG: Item NO encontrado en array embebido")
        
        # Verificar si se actualizó algo
        if items_actualizados == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item '{item_nombre}' no encontrado en la categoría"
            )
        
        # Limpiar caché del menú
        limpiar_cache_menu()
        
        print(f"🎉 DEBUG: Total items actualizados: {items_actualizados}")
        
        mensaje = "Item actualizado exitosamente"
        if cambio_categoria:
            mensaje = f"Item movido a nueva categoría y actualizado exitosamente"
        
        return {
            "message": mensaje,
            "items_actualizados": items_actualizados,
            "item_nombre": item_nombre,
            "categoria_cambio": cambio_categoria
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ DEBUG: Error al actualizar item: {str(e)}")
        import traceback
        print(f"❌ TRACEBACK: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar item: {str(e)}"
        )

@router.delete("/categorias/{categoria_id}/items/{item_nombre}", response_model=dict)
async def eliminar_item(
    categoria_id: str,
    item_nombre: str,
    item_index: int,
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Eliminar item de una categoría (busca en ambos almacenamientos)"""
    try:
        # Verificar que la categoría existe
        categoria = db.categorias_menu.find_one({"_id": ObjectId(categoria_id)})
        if not categoria:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Categoría no encontrada"
            )
        
        print(f"🗑️ DEBUG: Eliminando item '{item_nombre}' de categoría '{categoria['nombre']}'")
        
        # Intentar eliminar del almacenamiento híbrido
        items_eliminados = 0
        
        # 1. Intentar eliminar de la colección items_menu primero
        result_coleccion = db.items_menu.delete_one({
            "categoria_id": ObjectId(categoria_id),
            "nombre": item_nombre
        })
        
        if result_coleccion.deleted_count > 0:
            items_eliminados += 1
            print(f"✅ DEBUG: Item '{item_nombre}' eliminado de colección items_menu")
        else:
            print(f"⚠️ DEBUG: Item '{item_nombre}' no encontrado en colección items_menu")
        
        # 2. Si no se encontró en la colección, buscar en el array embebido de la categoría
        items = categoria.get("items", [])
        if item_index < len(items) and items[item_index].get("nombre") == item_nombre:
            # Remover el item del array embebido
            result_array = db.categorias_menu.update_one(
                {"_id": ObjectId(categoria_id)},
                {"$unset": {f"items.{item_index}": 1}}
            )
            
            # Limpiar el array de nulls
            db.categorias_menu.update_one(
                {"_id": ObjectId(categoria_id)},
                {"$pull": {"items": None}}
            )
            
            if result_array.modified_count > 0:
                items_eliminados += 1
                print(f"✅ DEBUG: Item '{item_nombre}' eliminado del array embebido")
            else:
                print(f"⚠️ DEBUG: No se pudo eliminar item '{item_nombre}' del array embebido")
        
        # Verificar si se eliminó algo
        if items_eliminados == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Item '{item_nombre}' no encontrado"
            )
        
        print(f"✅ DEBUG: Total items eliminados: {items_eliminados}")
        
        # Limpiar caché del menú
        limpiar_cache_menu()
        
        return {
            "message": "Item eliminado exitosamente",
            "item_eliminado": item_nombre,
            "total_eliminados": items_eliminados
        }
    except Exception as e:
        print(f"❌ DEBUG: Error al eliminar item: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al eliminar item: {str(e)}"
        )

# =============================================================================
# ENDPOINTS DE GESTIÓN DE IMÁGENES
# =============================================================================

@router.post("/upload-image", response_model=dict)
async def subir_imagen(
    file: UploadFile = File(...),
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Subir imagen para categorías o items"""
    try:
        # Validar que es una imagen
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El archivo debe ser una imagen"
            )
        
        # Leer y procesar la imagen
        contents = await file.read()
        
        # Redimensionar imagen si es necesario (opcional)
        image = Image.open(io.BytesIO(contents))
        
        # Convertir RGBA a RGB si es necesario (para imágenes PNG con transparencia)
        if image.mode == 'RGBA':
            # Crear fondo blanco
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])  # 3 es el canal alpha
            image = background
        elif image.mode != 'RGB':
            # Convertir cualquier otro modo a RGB
            image = image.convert('RGB')
        
        if image.width > 1200 or image.height > 800:
            image.thumbnail((1200, 800), Image.Resampling.LANCZOS)
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=85)
            contents = img_byte_arr.getvalue()
        else:
            # Guardar como JPEG incluso si no se redimensiona
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='JPEG', quality=85)
            contents = img_byte_arr.getvalue()
        
        # Subir a GridFS
        fs = gridfs.GridFS(db)
        file_id = fs.put(
            contents,
            filename=file.filename,
            content_type='image/jpeg'
        )
        
        return {
            "message": "Imagen subida exitosamente",
            "image_id": str(file_id),
            "file_id": str(file_id),
            "filename": file.filename,
            "image_url": f"/api/imagenes/{str(file_id)}"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al subir imagen: {str(e)}"
        )

@router.get("/imagenes", response_model=List[dict])
async def listar_imagenes(
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Listar todas las imágenes disponibles"""
    try:
        fs = gridfs.GridFS(db)
        imagenes = []
        
        for file_info in fs.find():
            imagenes.append({
                "_id": str(file_info._id),
                "filename": file_info.filename,
                "upload_date": file_info.upload_date.isoformat(),
                "length": file_info.length,
                "content_type": file_info.content_type,
                "url": f"http://localhost:8000/api/imagenes/{str(file_info._id)}"
            })
        
        return imagenes
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener imágenes: {str(e)}"
        )

# Alias para compatibilidad
@router.get("/images", response_model=List[dict])
async def listar_imagenes_alias(
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Listar todas las imágenes disponibles (alias)"""
    return await listar_imagenes(current_user, db)

@router.delete("/imagenes/{file_id}", response_model=dict)
async def eliminar_imagen(
    file_id: str,
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Eliminar imagen de GridFS"""
    try:
        fs = gridfs.GridFS(db)
        fs.delete(ObjectId(file_id))
        return {"message": "Imagen eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagen no encontrada"
        )

# Alias para compatibilidad
@router.delete("/images/{file_id}", response_model=dict)
async def eliminar_imagen_alias(
    file_id: str,
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Eliminar imagen de GridFS (alias)"""
    return await eliminar_imagen(file_id, current_user, db)

# =============================================================================
# ENDPOINTS DE GESTIÓN DE INFORMACIÓN DEL RESTAURANTE
# =============================================================================

@router.get("/restaurante-info", response_model=RestauranteInfoMongo)
async def obtener_info_restaurante_admin(
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Obtener información del restaurante para administración"""
    try:
        info = db.restaurante_info.find_one()
        if not info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Información del restaurante no encontrada"
            )
        return RestauranteInfoMongo(**info)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al obtener información: {str(e)}"
        )

@router.put("/restaurante-info", response_model=dict)
async def actualizar_info_restaurante(
    info: RestauranteInfoMongoUpdate,
    current_user: UsuarioMongo = Depends(AuthService.get_current_admin_user),
    db = Depends(get_mongo_db)
):
    """Actualizar información del restaurante"""
    try:
        # Preparar datos para actualizar
        update_data = {k: v for k, v in info.dict().items() if v is not None}
        
        if update_data:
            result = db.restaurante_info.update_one(
                {},  # Actualizar el primer documento
                {"$set": update_data}
            )
            
            if result.matched_count == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Información del restaurante no encontrada"
                )
        
        return {"message": "Información del restaurante actualizada exitosamente"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al actualizar información: {str(e)}"
        )