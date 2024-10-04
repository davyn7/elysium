from sqlmodel import Field, SQLModel
from typing import Optional

class Hero(SQLModel, table=True):
    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None

class TempHero(SQLModel):
    id: int
    name: str
    secret_name: str
    age: int | None = None

# More code here later 👇