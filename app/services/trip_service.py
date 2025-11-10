from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from ..models.trip import Trip, TripDay, TripActivity
from ..schemas.trip import TripCreate, TripUpdate, TripGenerateRequest
from .ai_service import AIService


class TripService:
    """旅行计划服务"""

    def __init__(self, db: Session):
        self.db = db
        self.ai_service = AIService()

    def create_trip(self, user_id: int, trip_data: TripCreate) -> Trip:
        """创建旅行计划"""
        trip = Trip(
            user_id=user_id,
            title=trip_data.title,
            destination=trip_data.destination,
            start_date=trip_data.start_date,
            end_date=trip_data.end_date,
            budget=trip_data.budget,
            traveler_count=trip_data.traveler_count,
            preferences=trip_data.preferences,
            description=trip_data.description,
        )

        self.db.add(trip)
        self.db.commit()
        self.db.refresh(trip)
        return trip

    def generate_ai_trip(self, user_id: int, request: TripGenerateRequest) -> Trip:
        """使用 AI 生成旅行计划"""

        # 调用 AI 服务生成行程
        ai_plan = self.ai_service.generate_trip_plan(
            destination=request.destination,
            start_date=request.start_date,
            end_date=request.end_date,
            budget=request.budget,
            traveler_count=request.traveler_count,
            preferences=request.preferences,
        )

        # 创建旅行计划
        trip = Trip(
            user_id=user_id,
            title=f"{request.destination}之旅",
            destination=request.destination,
            start_date=request.start_date,
            end_date=request.end_date,
            budget=request.budget,
            traveler_count=request.traveler_count,
            preferences=request.preferences,
            description=ai_plan.get("summary", ""),
            ai_generated=ai_plan,
        )

        self.db.add(trip)
        self.db.flush()  # 获取 trip.id

        # 创建每天的行程
        if "days" in ai_plan:
            for day_data in ai_plan["days"]:
                day_number = day_data.get("day", 1)
                day_date = datetime.fromisoformat(day_data["date"])

                trip_day = TripDay(
                    trip_id=trip.id,
                    day_number=day_number,
                    date=day_date,
                    title=day_data.get("title", f"第{day_number}天"),
                    description=day_data.get("description", ""),
                )

                self.db.add(trip_day)
                self.db.flush()  # 获取 trip_day.id

                # 创建每天的活动
                activities = day_data.get("activities", [])
                for idx, activity_data in enumerate(activities):
                    activity = TripActivity(
                        day_id=trip_day.id,
                        activity_type=activity_data.get("type", "other"),
                        name=activity_data.get("name", ""),
                        location=activity_data.get("location", ""),
                        start_time=self._parse_time(
                            day_date, activity_data.get("time", "")
                        ),
                        duration=activity_data.get("duration", 60),
                        cost=activity_data.get("cost", 0),
                        description=activity_data.get("description", ""),
                        order_index=idx,
                    )
                    self.db.add(activity)

        self.db.commit()
        self.db.refresh(trip)
        return trip

    def get_trip(self, trip_id: int, user_id: int) -> Optional[Trip]:
        """获取旅行计划"""
        return (
            self.db.query(Trip)
            .filter(Trip.id == trip_id, Trip.user_id == user_id)
            .first()
        )

    def get_user_trips(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Trip]:
        """获取用户的所有旅行计划"""
        return (
            self.db.query(Trip)
            .filter(Trip.user_id == user_id)
            .order_by(Trip.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update_trip(self, trip_id: int, user_id: int, trip_data: TripUpdate) -> Optional[Trip]:
        """更新旅行计划"""
        trip = self.get_trip(trip_id, user_id)
        if not trip:
            return None

        update_data = trip_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(trip, field, value)

        self.db.commit()
        self.db.refresh(trip)
        return trip

    def delete_trip(self, trip_id: int, user_id: int) -> bool:
        """删除旅行计划"""
        trip = self.get_trip(trip_id, user_id)
        if not trip:
            return False

        self.db.delete(trip)
        self.db.commit()
        return True

    def _parse_time(self, date: datetime, time_str: str) -> datetime:
        """解析时间字符串为 datetime"""
        try:
            if ":" in time_str:
                hour, minute = map(int, time_str.split(":"))
                return date.replace(hour=hour, minute=minute, second=0)
        except:
            pass
        return date
