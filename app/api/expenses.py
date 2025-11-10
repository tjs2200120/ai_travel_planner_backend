from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from ..core.database import get_db
from ..models.user import User
from ..models.expense import Expense
from ..schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from ..services.ai_service import AIService
from .deps import get_current_user

router = APIRouter()


@router.post("/", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
def create_expense(
    expense_data: ExpenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """创建费用记录"""
    expense = Expense(
        user_id=current_user.id,
        trip_id=expense_data.trip_id,
        category=expense_data.category,
        amount=expense_data.amount,
        currency=expense_data.currency,
        description=expense_data.description,
        expense_date=expense_data.expense_date,
        payment_method=expense_data.payment_method,
        notes=expense_data.notes,
    )

    db.add(expense)
    db.commit()
    db.refresh(expense)

    return expense


@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(
    trip_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取费用记录列表"""
    query = db.query(Expense).filter(Expense.user_id == current_user.id)

    if trip_id:
        query = query.filter(Expense.trip_id == trip_id)

    expenses = query.order_by(Expense.expense_date.desc()).offset(skip).limit(limit).all()
    return expenses


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """获取单个费用记录"""
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == current_user.id)
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="费用记录不存在",
        )

    return expense


@router.put("/{expense_id}", response_model=ExpenseResponse)
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """更新费用记录"""
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == current_user.id)
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="费用记录不存在",
        )

    update_data = expense_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(expense, field, value)

    db.commit()
    db.refresh(expense)

    return expense


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除费用记录"""
    expense = (
        db.query(Expense)
        .filter(Expense.id == expense_id, Expense.user_id == current_user.id)
        .first()
    )

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="费用记录不存在",
        )

    db.delete(expense)
    db.commit()

    return None


@router.get("/analysis/{trip_id}")
def analyze_trip_budget(
    trip_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """分析旅行预算"""
    from ..models.trip import Trip

    # 获取旅行计划
    trip = (
        db.query(Trip)
        .filter(Trip.id == trip_id, Trip.user_id == current_user.id)
        .first()
    )

    if not trip:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="旅行计划不存在",
        )

    # 获取该旅行的所有费用
    expenses = (
        db.query(Expense)
        .filter(Expense.trip_id == trip_id, Expense.user_id == current_user.id)
        .all()
    )

    # 转换为字典列表
    expenses_data = [
        {"amount": exp.amount, "category": exp.category} for exp in expenses
    ]

    # 使用 AI 服务分析预算
    ai_service = AIService()
    analysis = ai_service.analyze_budget(expenses_data, trip.budget or 0)

    return analysis
