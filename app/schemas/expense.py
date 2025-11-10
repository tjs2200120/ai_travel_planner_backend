from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ExpenseCreate(BaseModel):
    """创建费用记录"""

    trip_id: Optional[int] = None
    category: str = Field(..., description="分类：transport, accommodation, food, attraction, shopping, other")
    amount: float = Field(..., ge=0)
    currency: str = Field("CNY", max_length=10)
    description: Optional[str] = None
    expense_date: datetime = Field(default_factory=datetime.utcnow)
    payment_method: Optional[str] = Field(None, description="支付方式")
    notes: Optional[str] = None


class ExpenseUpdate(BaseModel):
    """更新费用记录"""

    trip_id: Optional[int] = None
    category: Optional[str] = None
    amount: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = None
    description: Optional[str] = None
    expense_date: Optional[datetime] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None


class ExpenseResponse(BaseModel):
    """费用记录响应"""

    id: int
    user_id: int
    trip_id: Optional[int] = None
    category: str
    amount: float
    currency: str
    description: Optional[str] = None
    expense_date: datetime
    payment_method: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
