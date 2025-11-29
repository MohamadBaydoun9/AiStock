from app.db.mongo import get_database
from app.models.product_type import ProductTypeCreate, ProductTypeInDB, ProductTypeUpdate, ProductTypeRead
from fastapi import HTTPException, status
from typing import List, Optional

class ProductTypeService:
    async def get_all_types(self) -> List[ProductTypeRead]:
        db = await get_database()
        cursor = db.product_types.find()
        types = []
        async for doc in cursor:
            # Count products using this type
            product_count = await db.products.count_documents({"product_type": doc["name"]})
            types.append(ProductTypeRead(
                type_id=doc["type_id"],
                name=doc["name"],
                created_at=doc["created_at"],
                product_count=product_count
            ))
        return types

    async def create_type(self, type_data: ProductTypeCreate) -> ProductTypeRead:
        db = await get_database()
        
        # Check if type already exists
        existing = await db.product_types.find_one({"name": type_data.name})
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product type already exists"
            )
        
        db_type = ProductTypeInDB(**type_data.dict())
        await db.product_types.insert_one(db_type.dict())
        
        return ProductTypeRead(
            type_id=db_type.type_id,
            name=db_type.name,
            created_at=db_type.created_at,
            product_count=0
        )

    async def update_type(self, type_id: str, type_update: ProductTypeUpdate) -> Optional[ProductTypeRead]:
        db = await get_database()
        
        # Check if new name already exists (if name is being changed)
        existing_type = await db.product_types.find_one({"type_id": type_id})
        if not existing_type:
            return None
            
        if type_update.name != existing_type["name"]:
            duplicate = await db.product_types.find_one({"name": type_update.name})
            if duplicate:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Product type name already exists"
                )
        
        # Update the type
        result = await db.product_types.update_one(
            {"type_id": type_id},
            {"$set": {"name": type_update.name}}
        )
        
        if result.matched_count == 0:
            return None
        
        # Also update all products using this type
        old_name = existing_type["name"]
        await db.products.update_many(
            {"product_type": old_name},
            {"$set": {"product_type": type_update.name}}
        )
        
        # Get updated type
        updated_doc = await db.product_types.find_one({"type_id": type_id})
        product_count = await db.products.count_documents({"product_type": type_update.name})
        
        return ProductTypeRead(
            type_id=updated_doc["type_id"],
            name=updated_doc["name"],
            created_at=updated_doc["created_at"],
            product_count=product_count
        )

    async def delete_type(self, type_id: str) -> bool:
        db = await get_database()
        
        # Get the type to find its name
        type_doc = await db.product_types.find_one({"type_id": type_id})
        if not type_doc:
            return False
        
        # Check if any products use this type
        product_count = await db.products.count_documents({"product_type": type_doc["name"]})
        if product_count > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete type. {product_count} product(s) are using this type."
            )
        
        result = await db.product_types.delete_one({"type_id": type_id})
        return result.deleted_count > 0
