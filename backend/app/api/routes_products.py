from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Response
from typing import List, Optional
from app.models.product import ProductRead, ProductCreate, ProductUpdate
from app.models.user import UserRead
from app.services.product_service import ProductService
from app.api.deps import get_current_user, get_current_admin

router = APIRouter()
product_service = ProductService()

@router.post("/", response_model=ProductRead)
async def create_product(
    product_name: str = Form(...),
    product_type: str = Form(...),
    price_predicted: float = Form(...),
    quantity: int = Form(...),
    image: UploadFile = File(...),
    age_months: Optional[int] = Form(None),
    weight_kg: Optional[float] = Form(None),
    health_status: Optional[int] = Form(None),
    vaccinated: Optional[bool] = Form(None),
    country: Optional[str] = Form(None),
    predicted_breed: Optional[str] = Form(None),
    prediction_confidence: Optional[float] = Form(None),
    current_user: UserRead = Depends(get_current_user)
):
    product_data = ProductCreate(
        product_name=product_name,
        product_type=product_type,
        price_predicted=price_predicted,
        quantity=quantity,
        age_months=age_months,
        weight_kg=weight_kg,
        health_status=health_status,
        vaccinated=vaccinated,
        country=country,
        predicted_breed=predicted_breed,
        prediction_confidence=prediction_confidence
    )
    return await product_service.create_product(product_data, image)

@router.get("/shop/published", response_model=List[ProductRead])
async def get_shop_products(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    breed: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """Public endpoint - get published products for shop page"""
    return await product_service.get_published_products(
        skip=skip,
        limit=limit,
        type=type,
        breed=breed,
        min_price=min_price,
        max_price=max_price
    )

@router.get("/", response_model=List[ProductRead])
async def read_products(
    skip: int = 0, 
    limit: int = 10, 
    search: Optional[str] = None, 
    type: Optional[str] = None
):
    return await product_service.get_products(skip=skip, limit=limit, search=search, type=type)

@router.get("/{product_id}", response_model=ProductRead)
async def read_product(product_id: str):
    product = await product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/{product_id}/image")
async def get_product_image(product_id: str):
    image_bytes = await product_service.get_product_image(product_id)
    if not image_bytes:
        raise HTTPException(status_code=404, detail="Image not found")
    return Response(content=image_bytes, media_type="image/jpeg")

@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: str, 
    product_update: ProductUpdate,
    current_user: UserRead = Depends(get_current_user)
):
    updated_product = await product_service.update_product(product_id, product_update)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/{product_id}")
async def delete_product(
    product_id: str,
    current_user: UserRead = Depends(get_current_admin)
):
    success = await product_service.delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
