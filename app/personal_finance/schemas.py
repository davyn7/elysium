from sqlmodel import Field, SQLModel
from typing import Optional, List
from datetime import date
from uuid import UUID
from pydantic import BaseModel

class UserFSBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    marital_status: Optional[bool] = False
    kids: Optional[int] = 0

class RecurringIncomeBase(BaseModel):
    name: str
    amount: float
    frequency: str = "monthly" # Can be "annual"
    is_gross: bool = True
    start: date
    end: Optional[date] = None

class BonusBase(BaseModel):
    category: str = "bonus" # Can be "thr" or "commission"
    form: str = "fixed" # Can be "months" or "percentage"
    amount: float
    months_paid: List[str]

class AccountBase(BaseModel):
    name: str

class PortfolioBase(BaseModel):
    name: str

class InvestmentBase(BaseModel):
    name: str

class ExpenseBase(BaseModel):
    name: str

class SupplementaryIncomeBase(BaseModel):
    name: str