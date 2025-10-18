from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.schemas.schemas import ItemMenu, ItemMenuCreate, ItemMenuUpdate, CategoriaMenu, CategoriaMenuCreate
from app.models.models import ItemMenu as ItemMenuModel, CategoriaMenu as CategoriaMenuModel
from app.services.auth_service import AuthService

router = APIRouter()

# Rutas para Categorías de Menú
@router.get("/categorias", response_model=List[CategoriaMenu])
async def get_categorias(db: Session = Depends(get_db)):
    """Obtener todas las categorías del menú"""
    categorias = db.query(CategoriaMenuModel).filter(CategoriaMenuModel.activo == True).all()
    return categorias

@router.post("/categorias", response_model=CategoriaMenu)
async def create_categoria(
    categoria: CategoriaMenuCreate,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_admin_user)
):
    """Crear una nueva categoría (solo admin)"""
    db_categoria = CategoriaMenuModel(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

# Rutas para Items del Menú
@router.get("/items", response_model=List[ItemMenu])
async def get_menu_items(
    categoria_id: Optional[int] = None,
    disponible: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Obtener items del menú con filtros opcionales"""
    query = db.query(ItemMenuModel)
    
    if categoria_id:
        query = query.filter(ItemMenuModel.categoria_id == categoria_id)
    
    if disponible is not None:
        query = query.filter(ItemMenuModel.disponible == disponible)
    
    items = query.all()
    return items

@router.get("/items/{item_id}", response_model=ItemMenu)
async def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    """Obtener un item específico del menú"""
    item = db.query(ItemMenuModel).filter(ItemMenuModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item

@router.post("/items", response_model=ItemMenu)
async def create_menu_item(
    item: ItemMenuCreate,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_admin_user)
):
    """Crear un nuevo item del menú (solo admin)"""
    # Verificar que la categoría existe
    categoria = db.query(CategoriaMenuModel).filter(CategoriaMenuModel.id == item.categoria_id).first()
    if not categoria:
        raise HTTPException(status_code=400, detail="Categoría no encontrada")
    
    db_item = ItemMenuModel(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/items/{item_id}", response_model=ItemMenu)
async def update_menu_item(
    item_id: int,
    item_update: ItemMenuUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_admin_user)
):
    """Actualizar un item del menú (solo admin)"""
    db_item = db.query(ItemMenuModel).filter(ItemMenuModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    # Actualizar solo los campos proporcionados
    update_data = item_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/items/{item_id}")
async def delete_menu_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(AuthService.get_current_admin_user)
):
    """Eliminar un item del menú (solo admin)"""
    db_item = db.query(ItemMenuModel).filter(ItemMenuModel.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Item eliminado correctamente"}