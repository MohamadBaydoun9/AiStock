from app.db.mongo import get_database
from app.models.user import UserCreate, UserInDB
from app.core.security import get_password_hash, verify_password
from fastapi import HTTPException, status

class AuthService:
    def __init__(self):
        pass

    async def create_user(self, user: UserCreate, role: str = "user") -> UserInDB:
        db = await get_database()
        existing_user = await db.users.find_one({"email": user.email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        hashed_password = get_password_hash(user.password)
        user_dict = user.dict()
        user_dict['role'] = role  # Override the role
        db_user = UserInDB(
            **user_dict,
            password_hash=hashed_password
        )
        
        await db.users.insert_one(db_user.dict())
        return db_user

    async def authenticate_user(self, email: str, password: str):
        db = await get_database()
        user = await db.users.find_one({"email": email})
        if not user:
            return None
        if not verify_password(password, user["password_hash"]):
            return None
        return user
