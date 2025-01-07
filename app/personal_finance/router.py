from fastapi import Depends, APIRouter, HTTPException
from app.auth.db import User
from app.auth.user_manager import current_active_user
from app.personal_finance.models import (
    UserFS,
    Incomes
)
from app.personal_finance.schemas import (
    UserFSBase,
    RecurringIncomeBase,
    SupplementaryIncomeBase,
    BonusBase
)
from app.personal_finance.managers import (
    UserFSManager,
    RecurringIncomeManager
)
from app.db.config import db_client
from sqlmodel import select
from typing import List

router = APIRouter(prefix="/personal-finance", tags=["personal-finance"])

@router.get("/health_check")
async def health_check():
    return {"status": "ok"}

@router.post("/add_user")
async def add_user(userfs: UserFSBase, user: User = Depends(current_active_user)):
    try:
        manager = UserFSManager(userfs, user)
        print("PAAAASSED")
        return await manager.add_user()
    except Exception as e:
        raise e

# When a user adds an Income, first create a Base, then convert to RecurringIncomeObject or a SupplementaryIncomeObject 
# and then use helper functions to create the Income object and add it to DB
@router.post("/add_recurring_income")
async def add_recurring_income(income: RecurringIncomeBase, bonuses: List[BonusBase], _: User = Depends(current_active_user)):
    try:
        # async with db_client.get_async_session() as session:
        #     session.add(team)
        #     await session.commit()
        print(income)
        print(bonuses)
        return {"message": "Recurring income added"}
    except Exception as e:
        return e
    
@router.post("/add_supplementary_income")
async def add_supplementary_income(income: SupplementaryIncomeBase, _: User = Depends(current_active_user)):
    try:
        print(income)
        return {"message": "Supplementary income added"}
    except Exception as e:
        return e

# @router.post("/categories", response_model=CategoryRead)
# async def create_category(
#     category: CategoryCreate,
#     current_user: User = Depends(current_active_user)
# ):
#     try:
#         category_data = Category.model_validate(category)
#         async with db_client.get_async_session() as session:
#             session.add(category_data)
#             await session.commit()
#             await session.refresh(category_data)
#             return category_data
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.post("/income", response_model=IncomeRead)
# async def create_income(
#     income: IncomeCreate,
#     current_user: User = Depends(current_active_user)
# ):
#     try:
#         income_data = Income.model_validate(income)
#         income_data.user_id = current_user.id
#         async with db_client.get_async_session() as session:
#             session.add(income_data)
#             await session.commit()
#             await session.refresh(income_data)
#             return income_data
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.post("/expenses", response_model=ExpenseRead)
# async def create_expense(
#     expense: ExpenseCreate,
#     current_user: User = Depends(current_active_user)
# ):
#     try:
#         expense_data = Expense.model_validate(expense)
#         expense_data.user_id = current_user.id
#         async with db_client.get_async_session() as session:
#             session.add(expense_data)
#             await session.commit()
#             await session.refresh(expense_data)
#             return expense_data
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.get("/categories", response_model=List[CategoryRead])
# async def get_categories(
#     current_user: User = Depends(current_active_user)
# ):
#     try:
#         async with db_client.get_async_session() as session:
#             statement = select(Category)
#             results = await session.execute(statement)
#             categories = results.scalars().all()
#             return categories
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.get("/income", response_model=List[IncomeRead])
# async def get_income(
#     current_user: User = Depends(current_active_user)
# ):
#     try:
#         async with db_client.get_async_session() as session:
#             statement = select(Income).where(Income.user_id == current_user.id)
#             results = await session.execute(statement)
#             income = results.scalars().all()
#             return income
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @router.get("/expenses", response_model=List[ExpenseRead])
# async def get_expenses(
#     current_user: User = Depends(current_active_user)
# ):
#     try:
#         async with db_client.get_async_session() as session:
#             statement = select(Expense).where(Expense.user_id == current_user.id)
#             results = await session.execute(statement)
#             expenses = results.scalars().all()
#             return expenses
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))