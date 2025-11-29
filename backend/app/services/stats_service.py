from app.db.mongo import get_database

class StatsService:
    async def get_summary(self):
        db = await get_database()
        
        pipeline = [
            {
                "$group": {
                    "_id": None,
                    "total_products": {"$sum": 1},
                    "total_items": {"$sum": "$quantity"},
                    "total_value": {
                        "$sum": {
                            "$multiply": [
                                "$quantity",
                                {"$ifNull": ["$price_modified", "$price_predicted"]}
                            ]
                        }
                    }
                }
            }
        ]
        
        result = await db.products.aggregate(pipeline).to_list(length=1)
        
        if not result:
            return {
                "total_products": 0,
                "total_items": 0,
                "total_value": 0.0
            }
            
        stats = result[0]
        return {
            "total_products": stats["total_products"],
            "total_items": stats["total_items"],
            "total_value": round(stats["total_value"], 2)
        }
