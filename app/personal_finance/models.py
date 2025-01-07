from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from app.db.config import db_client
from uuid import UUID
from datetime import date

current_schema = "Personal-Finance"

class UserFS(SQLModel, table=True):
    __tablename__ = "userfs_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None = Field(default=None, primary_key=True)
    user_id: Optional[UUID] = Field(default=None)
    first_name: str
    last_name: str
    email: str
    marital_status: bool = False
    kids: int = 0
    untaxable: int = 54000000
    # incomes: List["Incomes"] = Relationship(back_populates="user")
    # recurring_incomes: List["RecurringIncome"] = Relationship(back_populates="user")
    # supplementary_incomes: List["SupplementaryIncome"] = Relationship(back_populates="user")
    # income_paid: float = 0.0
    # taxes_paid: float = 0.0

# class RecurringIncome(SQLModel, table=True):
#     __tablename__ = "recurring_income_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] | None = Field(default=None, primary_key=True)
#     user: Optional["UserFS"] = Relationship(back_populates="recurring_incomes")
#     name: str
#     description: Optional[str] = None
#     monthly_gross: float
#     annual_gross: float
#     base_monthly_gross: str
#     base_annual_gross: float
#     additional_monthly_gross: str
#     additional_annual_gross: float
#     monthly_paid: Optional[str] = ""
#     start: date
#     end: Optional[date] = None

# class SupplementaryIncome(SQLModel, table=True):
#     __tablename__ = "supplementary_income_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] | None = Field(default=None, primary_key=True)
#     user: Optional["UserFS"] = Relationship(back_populates="supplementary_incomes")
#     name: str
#     description: Optional[str] = None
#     gross_amount: float
#     paid_amount: float
#     paid_date: date

class Incomes(SQLModel, table=True):
    __tablename__ = "incomes_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None = Field(default=None, primary_key=True)
    category: str # Recurring or Supplementary

# class FixedExpense(SQLModel, table=True):
#     __tablename__ = "fixed_expenses_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] | None = Field(default=None, primary_key=True)

# class VariableExpense(SQLModel, table=True):
#     __tablename__ = "variable_expenses_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] | None = Field(default=None, primary_key=True)

# class Expenses(SQLModel, table=True):
#     __tablename__ = "expenses_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] | None = Field(default=None, primary_key=True)

# class Savings(SQLModel, table=True):
#     __tablename__ = "savings_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] | None = Field(default=None, primary_key=True)

# class Debts(SQLModel, table=True):
#     __tablename__ = "debts_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] | None = Field(default=None, primary_key=True)

# class Investment(SQLModel, table=True):
#     __tablename__ = "investments_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] | None = Field(default=None, primary_key=True)

# class InvestmentPortfolio(SQLModel, table=True):
#     __tablename__ = "investments_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] | None = Field(default=None, primary_key=True)

# class Category(SQLModel, table=True):
#     __tablename__ = "categories_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] | None = Field(default=None, primary_key=True)
#     name: str
#     description: Optional[str] = None
#     type: str  # 'income' or 'expense'
#     parent_id: Optional[int] = None  # For hierarchical categories

# class Income(SQLModel, table=True):
#     __tablename__ = "income_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] | None = Field(default=None, primary_key=True)
#     user_id: Optional[UUID] = Field(default=None)
#     name: str
#     description: Optional[str] = None
#     category_id: int = Field(foreign_key=f"{current_schema}.categories_table.id")
#     amount: float
#     currency: str = "IDR"
#     is_recurring: bool = False
#     frequency: Optional[str] = None  # 'monthly', 'weekly', etc.
#     source: str  # 'employment', 'freelance', 'project'
#     # date: date
#     # status: str = 'pending'  # 'pending', 'received'

# class Expense(SQLModel, table=True):
#     __tablename__ = "expenses_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] | None = Field(default=None, primary_key=True)
#     name: str
#     description: Optional[str] = None
#     user_id: Optional[UUID] = Field(default=None)
#     category_id: int = Field(foreign_key=f"{current_schema}.categories_table.id")
#     amount: float
#     currency: str = "IDR"
#     date: date
#     is_recurring: bool = False
#     frequency: Optional[str] = None
#     payment_method: str  # 'cash', 'credit_card', 'bank_transfer'
#     status: str = 'pending'  # 'pending', 'paid'
#     invoice_url: Optional[str] = None

db_client.create_schema(current_schema)