from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from ..mongo_database import get_mongodb
from ..schemas.mongo_schemas import SeccionImagen, ActualizarSeccionImagen
from ..services.auth_mongo_simple import AuthService

router = APIRouter(prefix="/api/secciones-imagenes", tags=["Secciones de Imágenes"])

# Definición de secciones disponibles
SECCIONES_DISPONIBLES = {
    "hero": {
        "titulo": "Imagen Principal (Hero)",
        "descripcion": "Imagen destacada en la página principal",
        "orden": 1
    },
    "logo": {
        "titulo": "Logo del Restaurante",
        "descripcion": "Logo principal del restaurante",
        "orden": 2
    },
    "menu": {
        "titulo": "Imagen de Menú",
        "descripcion": "Imagen representativa del menú",
        "orden": 3
    },
    "galeria": {
        "titulo": "Galería",
        "descripcion": "Imágenes para la galería del restaurante",
        "orden": 4
    },
    "about": {
        "titulo": "Sobre Nosotros",
        "descripcion": "Imagen de la sección 'Sobre Nosotros'",
        "orden": 5
    },
    "banner": {
        "titulo": "Banner Promocional",
        "descripcion": "Banner para promociones especiales",
        "orden": 6
    }
}

@router.get("/", response_model=List[SeccionImagen])
async def obtener_secciones_imagenes():
    """Obtener todas las secciones de imágenes"""
    db = get_mongodb()
    collection = db["secciones_imagenes"]
    
    # Buscar secciones existentes
    secciones_cursor = collection.find()
    secciones_existentes = {}
    
    async for seccion in secciones_cursor:
        seccion["_id"] = str(seccion["_id"])
        secciones_existentes[seccion["seccion"]] = seccion
    
    # Crear secciones faltantes con configuración por defecto
    secciones_completas = []
    for key, config in SECCIONES_DISPONIBLES.items():
        if key in secciones_existentes:
            secciones_completas.append(secciones_existentes[key])
        else:
            # Crear sección por defecto
            nueva_seccion = {
                "seccion": key,
                "titulo": config["titulo"],
                "descripcion": config["descripcion"],
                "imagen_id": None,
                "imagen_url": None,
                "orden": config["orden"],
                "activo": True,
                "fecha_actualizacion": datetime.utcnow()
            }
            
            # Insertar en BD
            result = await collection.insert_one(nueva_seccion)
            nueva_seccion["_id"] = str(result.inserted_id)
            secciones_completas.append(nueva_seccion)
    
    # Ordenar por orden
    secciones_completas.sort(key=lambda x: x["orden"])
    return secciones_completas

@router.get("/{seccion}", response_model=SeccionImagen)
async def obtener_seccion_imagen(seccion: str):
    """Obtener una sección específica"""
    if seccion not in SECCIONES_DISPONIBLES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sección '{seccion}' no encontrada"
        )
    
    db = get_mongodb()
    collection = db["secciones_imagenes"]
    
    seccion_doc = await collection.find_one({"seccion": seccion})
    
    if not seccion_doc:
        # Crear sección por defecto si no existe
        config = SECCIONES_DISPONIBLES[seccion]
        nueva_seccion = {
            "seccion": seccion,
            "titulo": config["titulo"],
            "descripcion": config["descripcion"],
            "imagen_id": None,
            "imagen_url": None,
            "orden": config["orden"],
            "activo": True,
            "fecha_actualizacion": datetime.utcnow()
        }
        
        result = await collection.insert_one(nueva_seccion)
        nueva_seccion["_id"] = str(result.inserted_id)
        return nueva_seccion
    
    seccion_doc["_id"] = str(seccion_doc["_id"])
    return seccion_doc

@router.put("/{seccion}", response_model=SeccionImagen)
async def actualizar_seccion_imagen(
    seccion: str,
    datos: ActualizarSeccionImagen,
    admin=Depends(AuthService.get_current_admin_user)
):
    """Actualizar imagen de una sección"""
    if seccion not in SECCIONES_DISPONIBLES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sección '{seccion}' no encontrada"
        )
    
    db = get_mongodb()
    collection = db["secciones_imagenes"]
    
    # Preparar datos de actualización
    datos_actualizacion = {
        "fecha_actualizacion": datetime.utcnow()
    }
    
    for field, value in datos.model_dump(exclude_unset=True).items():
        datos_actualizacion[field] = value
    
    # Actualizar documento
    result = await collection.find_one_and_update(
        {"seccion": seccion},
        {"$set": datos_actualizacion},
        return_document=True
    )
    
    if not result:
        # Si no existe, crear nuevo
        config = SECCIONES_DISPONIBLES[seccion]
        nueva_seccion = {
            "seccion": seccion,
            "titulo": config["titulo"],
            "descripcion": config["descripcion"],
            "orden": config["orden"],
            "activo": True,
            **datos_actualizacion
        }
        
        insert_result = await collection.insert_one(nueva_seccion)
        nueva_seccion["_id"] = str(insert_result.inserted_id)
        return nueva_seccion
    
    result["_id"] = str(result["_id"])
    return result

@router.delete("/{seccion}/imagen")
async def eliminar_imagen_seccion(
    seccion: str,
    admin=Depends(AuthService.get_current_admin_user)
):
    """Eliminar la imagen de una sección específica"""
    if seccion not in SECCIONES_DISPONIBLES:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sección '{seccion}' no encontrada"
        )
    
    db = get_mongodb()
    collection = db["secciones_imagenes"]
    
    # Limpiar imagen de la sección
    result = await collection.find_one_and_update(
        {"seccion": seccion},
        {
            "$set": {
                "imagen_id": None,
                "imagen_url": None,
                "fecha_actualizacion": datetime.utcnow()
            }
        },
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sección '{seccion}' no encontrada en la base de datos"
        )
    
    return {"message": f"Imagen de la sección '{seccion}' eliminada correctamente"}

@router.get("/secciones/disponibles")
async def obtener_secciones_disponibles():
    """Obtener lista de secciones disponibles"""
    return SECCIONES_DISPONIBLES