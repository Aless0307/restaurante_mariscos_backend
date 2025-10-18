from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from app.mongo_database import get_mongodb, serialize_doc
from app.schemas.mongo_schemas import (
    MenuCompleto, CategoriaMenuMongo, ItemMenuMongo, 
    ActualizarItemMenu, ActualizarCategoriaMenu,
    CrearItemMenu, CrearCategoriaMenu
)
from bson import ObjectId
from datetime import datetime
import gridfs

router = APIRouter()

@router.get("/menu-completo", response_model=MenuCompleto)
async def get_menu_completo(db = Depends(get_mongodb)):
    """Obtener el menú completo con todas las categorías e items"""
    try:
        # Obtener todas las categorías activas
        categorias_cursor = db.categorias_menu.find(
            {"activo": True}
        ).sort("orden", 1)
        
        categorias = []
        total_items = 0
        
        for categoria_doc in categorias_cursor:
            categoria = serialize_doc(categoria_doc)
            
            # Obtener items de esta categoría
            items_cursor = db.items_menu.find(
                {"categoria_id": ObjectId(categoria["_id"])}
            ).sort("orden", 1)
            
            items = [serialize_doc(item) for item in items_cursor]
            categoria["items"] = items
            total_items += len(items)
            
            categorias.append(categoria)
        
        return {
            "categorias": categorias,
            "total_categorias": len(categorias),
            "total_items": total_items
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo menú: {str(e)}"
        )

@router.get("/categorias", response_model=List[CategoriaMenuMongo])
async def get_categorias(
    incluir_items: bool = False,
    activas_solo: bool = True,
    db = Depends(get_mongodb)
):
    """Obtener categorías del menú"""
    try:
        # Filtros
        filtros = {}
        if activas_solo:
            filtros["activo"] = True
        
        # Obtener categorías
        categorias_cursor = db.categorias_menu.find(filtros).sort("orden", 1)
        categorias = []
        
        for categoria_doc in categorias_cursor:
            categoria = serialize_doc(categoria_doc)
            
            if incluir_items:
                # Obtener items de esta categoría
                items_cursor = db.items_menu.find(
                    {"categoria_id": ObjectId(categoria["_id"])}
                ).sort("orden", 1)
                categoria["items"] = [serialize_doc(item) for item in items_cursor]
            else:
                categoria["items"] = []
            
            categorias.append(categoria)
        
        return categorias
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo categorías: {str(e)}"
        )

@router.get("/categorias/{categoria_id}", response_model=CategoriaMenuMongo)
async def get_categoria_por_id(categoria_id: str, db = Depends(get_mongodb)):
    """Obtener una categoría específica con sus items"""
    try:
        # Verificar que el ID sea válido
        if not ObjectId.is_valid(categoria_id):
            raise HTTPException(status_code=400, detail="ID de categoría inválido")
        
        # Buscar la categoría
        categoria_doc = db.categorias_menu.find_one({"_id": ObjectId(categoria_id)})
        if not categoria_doc:
            raise HTTPException(status_code=404, detail="Categoría no encontrada")
        
        categoria = serialize_doc(categoria_doc)
        
        # Obtener items de esta categoría
        items_cursor = db.items_menu.find(
            {"categoria_id": ObjectId(categoria_id)}
        ).sort("orden", 1)
        categoria["items"] = [serialize_doc(item) for item in items_cursor]
        
        return categoria
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo categoría: {str(e)}"
        )

@router.get("/items", response_model=List[ItemMenuMongo])
async def get_items_menu(
    categoria_id: Optional[str] = None,
    disponibles_solo: bool = True,
    buscar: Optional[str] = None,
    db = Depends(get_mongodb)
):
    """Obtener items del menú con filtros"""
    try:
        # Construir filtros
        filtros = {}
        
        if categoria_id:
            if not ObjectId.is_valid(categoria_id):
                raise HTTPException(status_code=400, detail="ID de categoría inválido")
            filtros["categoria_id"] = ObjectId(categoria_id)
        
        if disponibles_solo:
            filtros["disponible"] = True
        
        if buscar:
            filtros["nombre"] = {"$regex": buscar, "$options": "i"}
        
        # Obtener items
        items_cursor = db.items_menu.find(filtros).sort("orden", 1)
        items = [serialize_doc(item) for item in items_cursor]
        
        return items
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo items: {str(e)}"
        )

@router.get("/items/{item_id}", response_model=ItemMenuMongo)
async def get_item_por_id(item_id: str, db = Depends(get_mongodb)):
    """Obtener un item específico del menú"""
    try:
        if not ObjectId.is_valid(item_id):
            raise HTTPException(status_code=400, detail="ID de item inválido")
        
        item_doc = db.items_menu.find_one({"_id": ObjectId(item_id)})
        if not item_doc:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        
        return serialize_doc(item_doc)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo item: {str(e)}"
        )

# Rutas de administración (requieren autenticación - comentadas por ahora)

# @router.post("/categorias", response_model=CategoriaMenuMongo)
# async def crear_categoria(
#     categoria: CrearCategoriaMenu,
#     db = Depends(get_mongodb),
#     # current_user = Depends(AuthService.get_current_admin_user)
# ):
#     """Crear nueva categoría (solo admin)"""
#     try:
#         categoria_doc = {
#             **categoria.dict(),
#             "activo": True,
#             "fecha_creacion": datetime.now(),
#             "fecha_actualizacion": datetime.now()
#         }
        
#         result = db.categorias_menu.insert_one(categoria_doc)
#         categoria_doc["_id"] = result.inserted_id
        
#         return serialize_doc(categoria_doc)
        
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error creando categoría: {str(e)}"
#         )

# @router.post("/items", response_model=ItemMenuMongo)
# async def crear_item(
#     item: CrearItemMenu,
#     db = Depends(get_mongodb),
#     # current_user = Depends(AuthService.get_current_admin_user)
# ):
#     """Crear nuevo item de menú (solo admin)"""
#     try:
#         # Verificar que la categoría existe
#         if not ObjectId.is_valid(item.categoria_id):
#             raise HTTPException(status_code=400, detail="ID de categoría inválido")
        
#         categoria = db.categorias_menu.find_one({"_id": ObjectId(item.categoria_id)})
#         if not categoria:
#             raise HTTPException(status_code=400, detail="Categoría no encontrada")
        
#         # Obtener el próximo orden
#         ultimo_item = db.items_menu.find_one(
#             {"categoria_id": ObjectId(item.categoria_id)},
#             sort=[("orden", -1)]
#         )
#         proximo_orden = 1 if not ultimo_item else ultimo_item.get("orden", 0) + 1
        
#         item_doc = {
#             **item.dict(),
#             "categoria_id": ObjectId(item.categoria_id),
#             "categoria_nombre": categoria["nombre"],
#             "orden": proximo_orden,
#             "fecha_creacion": datetime.now(),
#             "fecha_actualizacion": datetime.now()
#         }
        
#         result = db.items_menu.insert_one(item_doc)
#         item_doc["_id"] = result.inserted_id
        
#         return serialize_doc(item_doc)
        
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Error creando item: {str(e)}"
#         )

@router.get("/imagen/{imagen_id}")
async def get_imagen(imagen_id: str, db = Depends(get_mongodb)):
    """Obtener imagen almacenada en GridFS"""
    try:
        if not ObjectId.is_valid(imagen_id):
            raise HTTPException(status_code=400, detail="ID de imagen inválido")
        
        fs = gridfs.GridFS(db)
        
        try:
            archivo = fs.get(ObjectId(imagen_id))
            
            from fastapi.responses import StreamingResponse
            import io
            
            return StreamingResponse(
                io.BytesIO(archivo.read()),
                media_type="image/jpeg",
                headers={"Content-Disposition": f"inline; filename={archivo.filename}"}
            )
            
        except gridfs.NoFile:
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error obteniendo imagen: {str(e)}"
        )