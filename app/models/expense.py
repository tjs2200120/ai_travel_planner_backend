from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..core.database import Base


class Expense(Base):
    """费用记录模型"""

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    category = Column(String(50), nullable=False)  # transport, accommodation, food, attraction, shopping, other
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="CNY")
    description = Column(Text, nullable=True)
    expense_date = Column(DateTime, default=datetime.utcnow)
    payment_method = Column(String(50), nullable=True)  # cash, credit_card, debit_card, mobile_payment
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    user = relationship("User", back_populates="expenses")
    trip = relationship("Trip", back_populates="expenses")

    def __repr__(self):
        return f"<Expense(id={self.id}, category={self.category}, amount={self.amount})>"
