from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from app.mongo_database import get_mongo_db
import gridfs
from bson import ObjectId
import io

router = APIRouter()

@router.get("/imagenes/{file_id}")
async def obtener_imagen_publica(
    file_id: str,
    db = Depends(get_mongo_db)
):
    """Obtener imagen por ID - acceso público"""
    try:
        fs = gridfs.GridFS(db)
        file = fs.get(ObjectId(file_id))
        
        return StreamingResponse(
            io.BytesIO(file.read()),
            media_type=file.content_type or "image/jpeg",
            headers={"Content-Disposition": f"inline; filename={file.filename}"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Imagen no encontrada"
        )

@router.get("/admin/imagenes/{file_id}")
async def obtener_imagen_admin(
    file_id: str,
    db = Depends(get_mongo_db)
):
    """Obtener imagen por ID - alias para admin (sin autenticación)"""
    return await obtener_imagen_publica(file_id, db)