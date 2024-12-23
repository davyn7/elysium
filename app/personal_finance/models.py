from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from app.db.config import db_client
from uuid import UUID
from datetime import date

current_schema = "Personal-Finance"

class Category(SQLModel, table=True):
    __tablename__ = "categories_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    type: str  # 'income' or 'expense'
    parent_id: Optional[int] = None  # For hierarchical categories

class Income(SQLModel, table=True):
    __tablename__ = "income_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    # user_id: UUID = Field(foreign_key="auth.user.id")
    # category_id: int = Field(foreign_key=f"{current_schema}.categories_table.id")
    # amount: float
    # date: date
    # description: Optional[str] = None
    # is_recurring: bool = False
    # frequency: Optional[str] = None  # 'monthly', 'weekly', etc.
    # source: str  # 'employment', 'freelance', 'project'
    # status: str = 'pending'  # 'pending', 'received'

class Expense(SQLModel, table=True):
    __tablename__ = "expenses_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    # user_id: UUID = Field(foreign_key="auth.user.id")
    # category_id: int = Field(foreign_key=f"{current_schema}.categories_table.id")
    # amount: float
    # date: date
    # description: Optional[str] = None
    # is_recurring: bool = False
    # frequency: Optional[str] = None
    # payment_method: str  # 'cash', 'credit_card', 'bank_transfer'
    # status: str = 'pending'  # 'pending', 'paid'
    # invoice_url: Optional[str] = None

db_client.create_schema(current_schema)