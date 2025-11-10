from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Trip(Base):
    """旅行计划模型"""

    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    budget = Column(Float, nullable=True)
    traveler_count = Column(Integer, default=1)
    preferences = Column(JSON, nullable=True)  # 旅行偏好（JSON 格式）
    description = Column(Text, nullable=True)
    status = Column(String(50), default="planning")  # planning, ongoing, completed, cancelled
    ai_generated = Column(JSON, nullable=True)  # AI 生成的完整行程（JSON 格式）
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    user = relationship("User", back_populates="trips")
    days = relationship("TripDay", back_populates="trip", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="trip", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Trip(id={self.id}, title={self.title}, destination={self.destination})>"


class TripDay(Base):
    """旅行日程（每天的行程）"""

    __tablename__ = "trip_days"

    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    day_number = Column(Integer, nullable=False)  # 第几天
    date = Column(DateTime, nullable=False)
    title = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    trip = relationship("Trip", back_populates="days")
    activities = relationship("TripActivity", back_populates="day", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<TripDay(id={self.id}, trip_id={self.trip_id}, day={self.day_number})>"


class TripActivity(Base):
    """旅行活动（景点、餐厅、交通等）"""

    __tablename__ = "trip_activities"

    id = Column(Integer, primary_key=True, index=True)
    day_id = Column(Integer, ForeignKey("trip_days.id"), nullable=False)
    activity_type = Column(String(50), nullable=False)  # attraction, restaurant, hotel, transport, other
    name = Column(String(255), nullable=False)
    location = Column(String(500), nullable=True)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    duration = Column(Integer, nullable=True)  # 持续时间（分钟）
    cost = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    order_index = Column(Integer, default=0)  # 当天活动的顺序
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    day = relationship("TripDay", back_populates="activities")

    def __repr__(self):
        return f"<TripActivity(id={self.id}, name={self.name}, type={self.activity_type})>"
