from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.models.user import UserCreate, UserRead, UserLogin
from app.services.auth_service import AuthService
from app.core.security import create_access_token
from app.api.deps import get_current_user
from datetime import timedelta

router = APIRouter()
auth_service = AuthService()

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate):
    return await auth_service.create_user(user)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user["user_id"])
    return {
        "access_token": access_token, 
        "token_type": "bearer",
        "user": UserRead(**user)
    }

@router.get("/me", response_model=UserRead)
async def read_users_me(current_user: UserRead = Depends(get_current_user)):
    return current_user
