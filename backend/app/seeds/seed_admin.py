import asyncio
from app.db.mongo import mongo_db
from app.services.auth_service import AuthService
from app.models.user import UserCreate


async def seed_admin():
    # Connect to Mongo
    await mongo_db.connect_to_mongo()
    db = mongo_db.db

    # Check if an admin already exists
    existing_admin = await db.users.find_one({"role": "admin"})
    if existing_admin:
        print("Admin user already exists.")
    else:
        auth_service = AuthService()
        admin_data = UserCreate(
            email="admin@smartstock.com",
            password="Admin123!",
            full_name="System Admin"
        )
        try:
            # create_user should be an async method that hashes password & inserts user
            await auth_service.create_user(admin_data, role="admin")
            print("Admin user created successfully.")
            print("Email: admin@smartstock.com")
            print("Password: Admin123!")
        except Exception as e:
            print(f"Error creating admin user: {e}")

    # Close Mongo connection
    await mongo_db.close_mongo_connection()



if __name__ == "__main__":
    asyncio.run(seed_admin())
