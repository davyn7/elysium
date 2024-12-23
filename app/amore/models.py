from sqlmodel import Field, SQLModel
from typing import Optional
from app.db.config import db_client
from datetime import datetime

current_schema = "Amore"

class Recipe(SQLModel, table=True):
    __tablename__ = "recipes_table"
    __table_args__ = {"schema": current_schema}
    
    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    