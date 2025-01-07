from sqlmodel import Field, SQLModel
from typing import Optional, List
from datetime import date
from uuid import UUID
from pydantic import BaseModel

class UserFSBase(BaseModel):
    first_name: str
    last_name: str
    marital_status: bool = False
    kids: int = 0

class RecurringIncomeBase(BaseModel):
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

class SupplementaryIncomeBase(BaseModel):
    pass