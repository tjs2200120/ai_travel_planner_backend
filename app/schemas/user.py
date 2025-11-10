from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模型"""

    email: EmailStr
    username: str = Field(..., min_length=3, max_length=100)


class UserCreate(UserBase):
    """用户注册模型"""

    password: str = Field(..., min_length=6, max_length=100)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    """用户登录模型"""

    username: str
    password: str


class UserResponse(UserBase):
    """用户响应模型"""

    id: int
    full_name: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """令牌响应模型"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """令牌数据模型"""

    user_id: Optional[int] = None
