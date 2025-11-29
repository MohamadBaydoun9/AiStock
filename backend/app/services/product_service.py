from app.db.mongo import get_database
from app.models.product import ProductCreate, ProductInDB, ProductUpdate, ProductRead
from fastapi import UploadFile, HTTPException, status
from bson import ObjectId
from typing import List, Optional

class ProductService:
    async def create_product(self, product_data: ProductCreate, image: UploadFile) -> ProductRead:
        db = await get_database()
        image_bytes = await image.read()
        
        db_product = ProductInDB(
            **product_data.model_dump(),
            image=image_bytes
        )
        
        result = await db.products.insert_one(db_product.model_dump())
        
        return ProductRead(
            _id=str(result.inserted_id),
            **db_product.model_dump(exclude={"image"}),
            has_image=True
        )

    async def get_products(self, skip: int = 0, limit: int = 10, search: Optional[str] = None, type: Optional[str] = None) -> List[ProductRead]:
        db = await get_database()
        query = {}
        if search:
            query["product_name"] = {"$regex": search, "$options": "i"}
        if type:
            query["product_type"] = type
            
        cursor = db.products.find(query).skip(skip).limit(limit)
        products = []
        async for doc in cursor:
            product_data = {k: v for k, v in doc.items() if k not in ["image"]}
            product_data["_id"] = str(doc["_id"])
            product_data["has_image"] = bool(doc.get("image"))
            products.append(ProductRead.model_validate(product_data))
        return products

    async def get_published_products(
        self, 
        skip: int = 0, 
        limit: int = 100,
        type: Optional[str] = None,
        breed: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None
    ) -> List[ProductRead]:
        """Get only published products for public shop page with filters"""
        db = await get_database()
        query = {"published": True}
        
        if type:
            query["product_type"] = type
        if breed:
            query["product_name"] = {"$regex": breed, "$options": "i"}
        
        # Price filtering (use modified price if available, otherwise predicted)
        if min_price is not None or max_price is not None:
            price_query = []
            if min_price is not None:
                price_query.append({
                    "$or": [
                        {"price_modified": {"$gte": min_price}},
                        {"$and": [{"price_modified": None}, {"price_predicted": {"$gte": min_price}}]}
                    ]
                })
            if max_price is not None:
                price_query.append({
                    "$or": [
                        {"price_modified": {"$lte": max_price}},
                        {"$and": [{"price_modified": None}, {"price_predicted": {"$lte": max_price}}]}
                    ]
                })
            if price_query:
                query["$and"] = price_query
        
        cursor = db.products.find(query).skip(skip).limit(limit).sort("date_added", -1)
        products = []
        async for doc in cursor:
            product_data = {k: v for k, v in doc.items() if k not in ["image"]}
            product_data["_id"] = str(doc["_id"])
            product_data["has_image"] = bool(doc.get("image"))
            products.append(ProductRead.model_validate(product_data))
        return products

    async def get_product(self, product_id: str) -> Optional[ProductRead]:
        db = await get_database()
        doc = await db.products.find_one({"product_id": product_id})
        if not doc:
            return None
        
        # Prepare data for ProductRead
        product_data = {k: v for k, v in doc.items() if k not in ["image"]}
        product_data["_id"] = str(doc["_id"])
        product_data["has_image"] = bool(doc.get("image"))
        
        return ProductRead.model_validate(product_data)

    async def get_product_image(self, product_id: str) -> Optional[bytes]:
        db = await get_database()
        doc = await db.products.find_one({"product_id": product_id})
        if not doc or "image" not in doc:
            return None
        return doc["image"]

    async def update_product(self, product_id: str, product_update: ProductUpdate) -> Optional[ProductRead]:
        db = await get_database()
        update_data = {k: v for k, v in product_update.model_dump(exclude_unset=True).items()}
        
        if not update_data:
            return await self.get_product(product_id)

        result = await db.products.update_one(
            {"product_id": product_id},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return None
            
        return await self.get_product(product_id)

    async def delete_product(self, product_id: str) -> bool:
        db = await get_database()
        result = await db.products.delete_one({"product_id": product_id})
        return result.deleted_count > 0

    async def get_product_types(self) -> List[str]:
        db = await get_database()
        return await db.products.distinct("product_type")

    async def get_product_names(self, type: Optional[str] = None) -> List[str]:
        db = await get_database()
        query = {}
        if type:
            query["product_type"] = type
        return await db.products.distinct("product_name", query)
