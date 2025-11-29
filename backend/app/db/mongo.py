from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

settings = get_settings()

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    async def connect_to_mongo(self):
        self.client = AsyncIOMotorClient(settings.MONGODB_URI)
        self.db = self.client[settings.MONGODB_DB_NAME]
        print("Connected to MongoDB")

    async def close_mongo_connection(self):
        if self.client:
            self.client.close()
            print("Closed MongoDB connection")

mongo_db = MongoDB()

async def get_database():
    return mongo_db.db
