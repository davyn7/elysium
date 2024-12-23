from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import date
from uuid import UUID

# class Hero(SQLModel, table=True):
#     id: Optional[int] | None = Field(default=None, primary_key=True)
#     name: str
#     secret_name: str
#     age: int | None = None

class Project(SQLModel):
    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    description: str

class CategoryBase(SQLModel):
    name: str
    description: Optional[str] = None
    type: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int

class IncomeBase(SQLModel):
    category_id: int
    amount: float
    date: date
    description: Optional[str] = None
    is_recurring: bool = False
    frequency: Optional[str] = None
    source: str
    status: str = 'pending'

class IncomeCreate(IncomeBase):
    pass

class IncomeRead(IncomeBase):
    id: int
    user_id: UUID

class ExpenseBase(SQLModel):
    category_id: int
    amount: float
    date: date
    description: Optional[str] = None
    is_recurring: bool = False
    frequency: Optional[str] = None
    payment_method: str
    status: str = 'pending'
    invoice_url: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseRead(ExpenseBase):
    id: int
    user_id: UUID