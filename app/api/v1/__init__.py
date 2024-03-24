from fastapi import APIRouter
from .user import router as user_router

router = APIRouter(
    tags=["api/v1"],
    prefix="/api/v1"
)

router.include_router(user_router)
