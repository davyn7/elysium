# from fastapi import Depends, APIRouter
# from app.auth.db import User
# from app.auth.user_manager import current_active_user
# # from app.project_management.models import Project, Task, TempTask
# from app.personal_finance.models import Project
# from app.db.config import db_client
# from sqlmodel import select

# router = APIRouter(prefix="/personal-finance", tags=["personal-finance"])

# @router.get("/health_check")
# async def health_check():
#     return {"status": "ok"}

# @router.post("/add_project")
# async def add_project(project: Project, _: User = Depends(current_active_user)):
#     try:
#         async with db_client.get_async_session() as session:
#             session.add(project)
#             await session.commit()
#         return {"message": "Project added"}
#     except Exception as e:
#         return e
    
from fastapi import Depends, APIRouter, HTTPException
from app.auth.db import User
from app.auth.user_manager import current_active_user
from app.personal_finance.models import Category, Income, Expense
from app.personal_finance.schemas import (
    CategoryCreate, CategoryRead,
    IncomeCreate, IncomeRead,
    ExpenseCreate, ExpenseRead
)
from app.db.config import db_client
from sqlmodel import select
from typing import List

router = APIRouter(prefix="/personal-finance", tags=["personal-finance"])

@router.get("/health_check")
async def health_check():
    return {"status": "ok"}

@router.post("/categories", response_model=CategoryRead)
async def create_category(
    category: CategoryCreate,
    current_user: User = Depends(current_active_user)
):
    try:
        category_data = Category.model_validate(category)
        async with db_client.get_async_session() as session:
            session.add(category_data)
            await session.commit()
            await session.refresh(category_data)
            return category_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/income", response_model=IncomeRead)
async def create_income(
    income: IncomeCreate,
    current_user: User = Depends(current_active_user)
):
    try:
        income_data = Income.model_validate(income)
        income_data.user_id = current_user.id
        async with db_client.get_async_session() as session:
            session.add(income_data)
            await session.commit()
            await session.refresh(income_data)
            return income_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/expenses", response_model=ExpenseRead)
async def create_expense(
    expense: ExpenseCreate,
    current_user: User = Depends(current_active_user)
):
    try:
        expense_data = Expense.model_validate(expense)
        expense_data.user_id = current_user.id
        async with db_client.get_async_session() as session:
            session.add(expense_data)
            await session.commit()
            await session.refresh(expense_data)
            return expense_data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/categories", response_model=List[CategoryRead])
async def get_categories(
    current_user: User = Depends(current_active_user)
):
    try:
        async with db_client.get_async_session() as session:
            statement = select(Category)
            results = await session.execute(statement)
            categories = results.scalars().all()
            return categories
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/income", response_model=List[IncomeRead])
async def get_income(
    current_user: User = Depends(current_active_user)
):
    try:
        async with db_client.get_async_session() as session:
            statement = select(Income).where(Income.user_id == current_user.id)
            results = await session.execute(statement)
            income = results.scalars().all()
            return income
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/expenses", response_model=List[ExpenseRead])
async def get_expenses(
    current_user: User = Depends(current_active_user)
):
    try:
        async with db_client.get_async_session() as session:
            statement = select(Expense).where(Expense.user_id == current_user.id)
            results = await session.execute(statement)
            expenses = results.scalars().all()
            return expenses
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))