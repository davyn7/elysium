from fastapi import Depends, APIRouter, HTTPException
from app.auth.db import User
from app.auth.user_manager import current_active_user
from app.personal_finance.schemas import (
    UserFSBase,
    RecurringIncomeBase,
    SupplementaryIncomeBase,
    BonusBase,
    AccountBase,
    PortfolioBase,
    InvestmentBase,
    ExpenseBase
)
from app.personal_finance.managers import (
    UserFSManager,
    RecurringIncomeManager
)
from app.db.config import db_client
from sqlmodel import select
from typing import Optional, List

router = APIRouter(prefix="/personal-finance", tags=["personal-finance"])

@router.get("/health_check")
async def health_check():
    return {"status": "ok"}

# UserFS management

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

# Account management

@router.get("/get_accounts")
async def get_accounts(user: User = Depends(current_active_user)):
    pass

@router.get("/get_account")
async def get_account(account_id: int, user: User = Depends(current_active_user)):
    pass

@router.post("/add_account")
async def add_account(account: AccountBase, user: User = Depends(current_active_user)):
    pass

@router.post("/edit_account")
async def edit_account(account: AccountBase, user: User = Depends(current_active_user)):
    pass

@router.post("/delete_account")
async def delete_account(account_id: int, user: User = Depends(current_active_user)):
    pass

# Income & Bonus Management

# When a user adds an Income, first create a Base, then convert to RecurringIncomeObject or a SupplementaryIncomeObject 
# and then use helper functions to create the Income object and add it to DB
@router.post("/add_recurring_income_contract/with_bonuses")
async def add_recurring_income(income: RecurringIncomeBase, bonuses: List[BonusBase], user: User = Depends(current_active_user)):
    try:
        # Create manager
        print(income)
        print(bonuses)
        return {"message": "Recurring income added"}
    except Exception as e:
        return e
    
@router.post("/add_recurring_income_contract/without_bonuses")
async def add_recurring_income(income: RecurringIncomeBase, user: User = Depends(current_active_user)):
    try:
        print(income)
        return {"message": "Recurring income added"}
    except Exception as e:
        return e
    
@router.post("/edit_recurring_income_contract/with_bonuses")
async def edit_recurring_income_contract(contract_id: int, income: RecurringIncomeBase, bonuses: List[BonusBase], user: User = Depends(current_active_user)):
    pass

@router.post("/edit_recurring_income_contract/without_bonuses")
async def edit_recurring_income_contract(contract_id: int, income: RecurringIncomeBase, user: User = Depends(current_active_user)):
    pass

@router.post("/add_bonus_structure")
async def add_bonus_structure(contract_id: int, bonus: BonusBase, user: User = Depends(current_active_user)):
    try:
        print(bonus)
        return {"message": "Bonus structure added"}
    except Exception as e:
        return e
    
@router.post("/edit_bonus_structure")
async def edit_bonus_structure(bonus_id: int, bonus: BonusBase, user: User = Depends(current_active_user)):
    try:
        print(bonus)
        return {"message": "Bonus structure edited"}
    except Exception as e:
        return e
    
@router.post("/delete_bonus_structure")
async def delete_bonus_structure(bonus_id: int, user: User = Depends(current_active_user)):
    try:
        return {"message": "Bonus structure deleted"}
    except Exception as e:
        return e

@router.post("/add_supplementary_income")
async def add_supplementary_income(income: SupplementaryIncomeBase, _: User = Depends(current_active_user)):
    try:
        print(income)
        return {"message": "Supplementary income added"}
    except Exception as e:
        return e
    
@router.get("/get_income_contracts")
async def get_income_contracts(user: User = Depends(current_active_user)):
    pass

@router.get("/get_income_contract")
async def get_income_contract(contract_id: int, user: User = Depends(current_active_user)):
    pass

@router.post("/delete_income_contract")
async def delete_income_contract(contract_id: int, user: User = Depends(current_active_user)):
    pass

@router.post("/end_income_contract")
async def end_income_contract(contract_id: int, user: User = Depends(current_active_user)):
    pass

@router.get("/get_monthly_income")
async def get_monthly_income(month: int, user: User = Depends(current_active_user)):
    pass

@router.post("/mark_income_as_paid")
async def mark_income_as_paid(month: int, user: User = Depends(current_active_user)):
    pass

# Portfolio Management

@router.get("/get_portfolios")
async def get_portfolios(user: User = Depends(current_active_user)):
    pass

@router.get("/get_portfolio")
async def get_portfolio(portfolio_id: int, user: User = Depends(current_active_user)):
    pass

@router.post("/add_portfolio")
async def add_portfolio(portfolio: PortfolioBase, user: User = Depends(current_active_user)):
    pass

@router.post("/edit_portfolio")
async def edit_portfolio(portfolio: PortfolioBase, user: User = Depends(current_active_user)):
    pass

@router.post("/delete_portfolio")
async def delete_portfolio(portfolio_id: int, user: User = Depends(current_active_user)):
    pass

# Investment Management

@router.get("/get_investments")
async def get_investments(user: User = Depends(current_active_user)):
    pass

@router.get("/get_investment")
async def get_investment(investment_id: int, user: User = Depends(current_active_user)):
    pass

@router.post("/add_investment")
async def add_investment(investment: InvestmentBase, user: User = Depends(current_active_user)):
    pass

@router.post("/edit_investment")
async def edit_investment(investment: InvestmentBase, user: User = Depends(current_active_user)):
    pass

@router.post("/close_investment")
async def close_investment(investment_id: int, user: User = Depends(current_active_user)):
    pass

@router.post("/delete_investment")
async def delete_investment(investment_id: int, user: User = Depends(current_active_user)):
    pass

# Expense Management

@router.get("/get_expenses")
async def get_expenses(user: User = Depends(current_active_user)):
    pass

@router.get("/get_expense")
async def get_expense(expense_id: int, user: User = Depends(current_active_user)):
    pass

@router.post("/add_expense")
async def add_expense(expense: ExpenseBase, user: User = Depends(current_active_user)):
    pass

@router.post("/edit_expense")
async def edit_expense(expense: ExpenseBase, user: User = Depends(current_active_user)):
    pass

@router.post("/delete_expense")
async def delete_expense(expense_id: int, user: User = Depends(current_active_user)):
    pass

# Analytics

@router.get("/get_income_analytics")
async def get_income_analytics(year: int, month: Optional[int] = None, user: User = Depends(current_active_user)):
    pass

@router.get("/get_expense_analytics")
async def get_expense_analytics(year: int, month: Optional[int] = None, user: User = Depends(current_active_user)):
    pass

@router.get("/get_investment_analytics")
async def get_investment_analytics(year: int, month: Optional[int] = None, user: User = Depends(current_active_user)):
    pass

@router.get("/get_portfolio_analytics")
async def get_portfolio_analytics(year: int, month: Optional[int] = None, user: User = Depends(current_active_user)):
    pass

