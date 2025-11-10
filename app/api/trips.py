from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models.user import User
from ..schemas.trip import (
    TripCreate,
    TripUpdate,
    TripResponse,
    TripGenerateRequest,
)
from ..services.trip_service import TripService
from .deps import get_current_user

router = APIRouter()


@router.post("/generate", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def generate_trip(
    request: TripGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """使用 AI 生成旅行计划"""
    trip_service = TripService(db)
    trip = trip_service.generate_ai_trip(current_user.id, request)
    return trip


@router.post("/", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(
    trip_data: TripCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建旅行计划（手动）"""
    trip_service = TripService(db)
    trip = trip_service.create_trip(current_user.id, trip_data)
    return trip


@router.get("/", response_model=List[TripResponse])
def get_trips(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取用户的所有旅行计划"""
    trip_service = TripService(db)
    trips = trip_service.get_user_trips(current_user.id, skip, limit)
    return trips


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取单个旅行计划详情"""
    trip_service = TripService(db)
    trip = trip_service.get_trip(trip_id, current_user.id)

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="旅行计划不存在",
        )

    return trip


@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(
    trip_id: int,
    trip_data: TripUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新旅行计划"""
    trip_service = TripService(db)
    trip = trip_service.update_trip(trip_id, current_user.id, trip_data)

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="旅行计划不存在",
        )

    return trip


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除旅行计划"""
    trip_service = TripService(db)
    success = trip_service.delete_trip(trip_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="旅行计划不存在",
        )

    return None
