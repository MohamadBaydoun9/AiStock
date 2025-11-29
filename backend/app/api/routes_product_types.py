from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.models.product_type import ProductTypeRead, ProductTypeCreate, ProductTypeUpdate
from app.models.user import UserRead
from app.services.product_type_service import ProductTypeService
from app.api.deps import get_current_user, get_current_admin

router = APIRouter()
product_type_service = ProductTypeService()

@router.get("/", response_model=List[ProductTypeRead])
async def get_product_types():
    """Get all product types (public endpoint for dropdown)"""
    return await product_type_service.get_all_types()

@router.post("/", response_model=ProductTypeRead)
async def create_product_type(
    type_data: ProductTypeCreate,
    current_user: UserRead = Depends(get_current_admin)
):
    """Create a new product type (admin only)"""
    return await product_type_service.create_type(type_data)

@router.put("/{type_id}", response_model=ProductTypeRead)
async def update_product_type(
    type_id: str,
    type_update: ProductTypeUpdate,
    current_user: UserRead = Depends(get_current_admin)
):
    """Update a product type (admin only)"""
    updated_type = await product_type_service.update_type(type_id, type_update)
    if not updated_type:
        raise HTTPException(status_code=404, detail="Product type not found")
    return updated_type

@router.delete("/{type_id}")
async def delete_product_type(
    type_id: str,
    current_user: UserRead = Depends(get_current_admin)
):
    """Delete a product type (admin only)"""
    success = await product_type_service.delete_type(type_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product type not found")
    return {"message": "Product type deleted successfully"}
