from sqlmodel import Field, SQLModel
from typing import Optional
from app.db.config import db_client

current_schema = "Heros"

class Hero(SQLModel, table=True):
    __tablename__ = "hero_table"
    __table_args__ = {"schema": current_schema}
    
    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

db_client.create_schema(current_schema)