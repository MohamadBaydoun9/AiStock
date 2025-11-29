"""
Quick test to check if products can be fetched
"""
import asyncio
import sys
sys.path.append('backend')

from app.db.mongo import get_database

async def test_fetch():
    db = await get_database()
    
    # Get first product
    doc = await db.products.find_one()
    
    if not doc:
        print("No products found in database")
        return
    
    print("Product document from DB:")
    print(f"_id: {doc.get('_id')}")
    print(f"product_id: {doc.get('product_id')}")
    print(f"product_name: {doc.get('product_name')}")
    print(f"product_type: {doc.get('product_type')}")
    print(f"price_predicted: {doc.get('price_predicted')}")
    print(f"quantity: {doc.get('quantity')}")
    print(f"date_added: {doc.get('date_added')}")
    print(f"has image: {bool(doc.get('image'))}")
    print(f"age_months: {doc.get('age_months')}")
    print(f"weight_kg: {doc.get('weight_kg')}")  
    print(f"health_status: {doc.get('health_status')}")
    print(f"vaccinated: {doc.get('vaccinated')}")
    
    # Try to create ProductRead
    try:
        from app.models.product import ProductRead
        product_read = ProductRead(
            _id=str(doc["_id"]),
            **{k: v for k, v in doc.items() if k not in ["image", "_id"]},
            has_image=bool(doc.get("image"))
        )
        print("\n✅ ProductRead created successfully!")
        print(f"ProductRead data: {product_read.dict()}")
    except Exception as e:
        print(f"\n❌ Failed to create ProductRead: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_fetch())
