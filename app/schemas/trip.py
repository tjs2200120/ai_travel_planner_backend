from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class TripGenerateRequest(BaseModel):
    """AI 生成行程请求"""

    destination: str = Field(..., description="目的地")
    start_date: datetime = Field(..., description="开始日期")
    end_date: datetime = Field(..., description="结束日期")
    budget: Optional[float] = Field(None, description="预算（元）")
    traveler_count: int = Field(1, ge=1, description="同行人数")
    preferences: Optional[Dict[str, Any]] = Field(None, description="旅行偏好")


class TripCreate(BaseModel):
    """创建旅行计划"""

    title: str = Field(..., min_length=1, max_length=255)
    destination: str = Field(..., min_length=1, max_length=255)
    start_date: datetime
    end_date: datetime
    budget: Optional[float] = Field(None, ge=0)
    traveler_count: int = Field(1, ge=1)
    preferences: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class TripUpdate(BaseModel):
    """更新旅行计划"""

    title: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    budget: Optional[float] = None
    traveler_count: Optional[int] = None
    preferences: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    status: Optional[str] = None


class TripActivityResponse(BaseModel):
    """活动响应"""

    id: int
    activity_type: str
    name: str
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    duration: Optional[int] = None
    cost: Optional[float] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    order_index: int

    class Config:
        from_attributes = True


class TripDayResponse(BaseModel):
    """日程响应"""

    id: int
    day_number: int
    date: datetime
    title: Optional[str] = None
    description: Optional[str] = None
    activities: List[TripActivityResponse] = []

    class Config:
        from_attributes = True


class TripResponse(BaseModel):
    """旅行计划响应"""

    id: int
    user_id: int
    title: str
    destination: str
    start_date: datetime
    end_date: datetime
    budget: Optional[float] = None
    traveler_count: int
    preferences: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    status: str
    ai_generated: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    days: List[TripDayResponse] = []

    class Config:
        from_attributes = True
