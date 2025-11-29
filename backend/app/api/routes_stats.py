from fastapi import APIRouter, Depends
from app.services.stats_service import StatsService
from app.models.user import UserRead
from app.api.deps import get_current_user

router = APIRouter()
stats_service = StatsService()

@router.get("/summary")
async def get_stats_summary(current_user: UserRead = Depends(get_current_user)):
    return await stats_service.get_summary()
