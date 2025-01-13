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

    # Relationships
    accounts: List["Account"] = Relationship(back_populates="user_fs")
    income_contracts: List["IncomeContract"] = Relationship(back_populates="user_fs")
    investments: List["Investment"] = Relationship(back_populates="user_fs")
    portfolios: List["Portfolio"] = Relationship(back_populates="user_fs")
    expenses: List["Expense"] = Relationship(back_populates="user_fs")

class Account(SQLModel, table=True):
    __tablename__ = "accounts_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None = Field(default=None, primary_key=True)
    userfs_id: Optional[int] = Field(default=None, foreign_key=f"{current_schema}.userfs_table.id")
    name: str
    account_type: str # savings, checking, investment, credit_card
    balance: float = 0
    credit_limit: Optional[float] = 0

    # Relationships
    userfs: Optional["UserFS"] = Relationship(back_populates="accounts")
    # transactions: List["Transaction"] = Relationship(back_populates="account")
    monthly_incomes: List["MonthlyIncome"] = Relationship(back_populates="account")
    investments: List["Investment"] = Relationship(back_populates="account")
    portfolios: List["Portfolio"] = Relationship(back_populates="account")
    expenses: List["Expense"] = Relationship(back_populates="account")

class IncomeContract(SQLModel, table=True):
    __tablename__ = "incomecontracts_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] = Field(default=None, primary_key=True)
    userfs_id: Optional[int] = Field(default=None, foreign_key=f"{current_schema}.userfs_table.id")
    income_type: str # recurring, one_time
    gross_amount: float = 0
    start_date: date
    end_date: Optional[date] = None
    frequency: str = "monthly" # monthly, annual
    status: str = "active" # active, inactive
    
    # Relationships
    user_fs: UserFS = Relationship(back_populates="income_contracts")
    monthly_incomes: List["MonthlyIncome"] = Relationship(back_populates="contract")
    bonus_structures: List["BonusStructure"] = Relationship(back_populates="contract")

class BonusStructure(SQLModel, table=True):
    __tablename__ = "bonusstructures_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] = Field(default=None, primary_key=True)
    contract_id: Optional[int] = Field(default=None, foreign_key=f"{current_schema}.incomecontracts_table.id")
    category: str = "bonus" # thr, commission, bonus
    bonus_type: str = "fixed" # fixed, percentage, months
    amount: float = 0  # fixed amount/percentage/number of months
    months_paid: str  # months paid for bonus, json str of months
    condition: Optional[str]
    
    # Relationships
    contract: IncomeContract = Relationship(back_populates="bonus_structures")
    monthly_incomes: List["MonthlyIncome"] = Relationship(back_populates="bonus")

class MonthlyIncome(SQLModel, table=True):
    __tablename__ = "monthlyincomes_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] = Field(default=None, primary_key=True)
    contract_id: int = Field(default=None, foreign_key=f"{current_schema}.incomecontracts_table.id")
    bonus_id: Optional[int] = Field(default=None, foreign_key=f"{current_schema}.bonusstructures_table.id")
    account_id: int = Field(default=None, foreign_key=f"{current_schema}.accounts_table.id")
    month: int
    gross_amount: float = 0
    net_amount: float = 0
    income_type: str = ""
    status: str = "pending" # pending, paid
    
    # Relationships
    contract: IncomeContract = Relationship(back_populates="monthly_incomes")
    bonus: Optional["BonusStructure"] = Relationship(back_populates="monthly_incomes")
    account: Account = Relationship(back_populates="monthly_incomes")

# class Transaction(SQLModel, table=True):
#     __tablename__ = "transactions_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] = Field(default=None, primary_key=True)
#     account_id: int = Field(default=None, foreign_key=f"{current_schema}.accounts_table.id")
#     # linked_account_id: Optional[int] = Field(default=None, foreign_key=f"{current_schema}.accounts_table.id")
#     amount: float
#     transaction_type: str # deposit, withdrawal, transfer
#     category: Optional[str] = ""
#     timestamp: date
#     status: str = "pending" # pending, completed
    
#     # Relationships
#     account: Account = Relationship(back_populates="transactions", foreign_key="account_id")
#     # linked_account: Optional[Account] = Relationship(foreign_key="linked_account_id")

class Portfolio(SQLModel, table=True):
    __tablename__ = "portfolios_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] = Field(default=None, primary_key=True)
    userfs_id: int = Field(default=None, foreign_key=f"{current_schema}.userfs_table.id")
    account_id: int = Field(default=None, foreign_key=f"{current_schema}.accounts_table.id")
    name: str
    portfolio_type: str # retirement, brokerage, roth_ira, traditional_ira

    # Relationships
    user_fs: UserFS = Relationship(back_populates="portfolios")
    account: Account = Relationship(back_populates="portfolios")
    investments: List["Investment"] = Relationship(back_populates="portfolio")

class Investment(SQLModel, table=True):
    __tablename__ = "investments_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] = Field(default=None, primary_key=True)
    userfs_id: int = Field(default=None, foreign_key=f"{current_schema}.userfs_table.id")
    account_id: int = Field(default=None, foreign_key=f"{current_schema}.accounts_table.id")
    portfolio_id: Optional[int] = Field(default=None, foreign_key=f"{current_schema}.portfolios_table.id")
    investment_type: str # stock, bond, mutual_fund, etf, crypto
    symbol: str
    quantity: float
    purchase_price: float
    purchase_date: date
    sell_price: Optional[float] = None
    sell_date: Optional[date] = None
    status: str = "open" # open, closed
    
    # Relationships
    user_fs: UserFS = Relationship(back_populates="investments")
    account: Account = Relationship(back_populates="investments")
    portfolio: Optional[Portfolio] = Relationship(back_populates="investments")
    # transactions: List["Transaction"] = Relationship()

class Expense(SQLModel, table=True):
    __tablename__ = "expenses_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] = Field(default=None, primary_key=True)
    userfs_id: int = Field(default=None, foreign_key=f"{current_schema}.userfs_table.id")
    account_id: int = Field(default=None, foreign_key=f"{current_schema}.accounts_table.id")  # payment source
    expense_type: str # fixed, variable
    category: Optional[str] = ""
    amount: float
    frequency: str = "one_time" # one_time, monthly, annually, quarterly
    due_date: date
    status: str = "pending" # pending, paid
    
    # Relationships
    user_fs: UserFS = Relationship(back_populates="expenses")
    account: Account = Relationship(back_populates="expenses")
    # transactions: List["Transaction"] = Relationship()

# class Incomes(SQLModel, table=True):
#     __tablename__ = "incomes_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] | None = Field(default=None, primary_key=True)
#     user_id: Optional[UUID] = Field(default=None)
#     name: str
#     category: str # Recurring or Supplementary
#     basic_income: str = ""
#     additional_income: Optional[str] = ""
#     income_obj: str = ""
#     start: date
#     end: Optional[date] = None

db_client.create_schema(current_schema)