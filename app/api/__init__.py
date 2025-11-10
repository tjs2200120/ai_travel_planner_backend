from fastapi import APIRouter
from .auth import router as auth_router
from .trips import router as trips_router
from .expenses import router as expenses_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(trips_router, prefix="/trips", tags=["旅行计划"])
api_router.include_router(expenses_router, prefix="/expenses", tags=["费用管理"])

__all__ = ["api_router"]
