from fastapi import Depends, APIRouter, HTTPException
from app.auth.db import User
from app.auth.user_manager import current_active_user
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

@router.get("/get_user")
async def get_user(user: User = Depends(current_active_user)):
    try:
        manager = UserFSManager(None, user)
        return await manager.get_user()
    except Exception as e:
        raise e

@router.post("/add_user")
async def add_user(userfs: UserFSBase, user: User = Depends(current_active_user)):
    try:
        manager = UserFSManager(userfs, user)
        return await manager.add_user()
    except Exception as e:
        raise e

@router.post("/edit_user")
async def edit_user(userfs: UserFSBase, user: User = Depends(current_active_user)):
    try:
        manager = UserFSManager(userfs, user)
        return await manager.edit_user()
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
