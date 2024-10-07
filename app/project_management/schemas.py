from sqlmodel import Field, SQLModel
from typing import Optional

# class Hero(SQLModel, table=True):
#     id: Optional[int] | None = Field(default=None, primary_key=True)
#     name: str
#     secret_name: str
#     age: int | None = None

class Project(SQLModel):
    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    description: str

class Task(SQLModel):
    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    description: str
    project_id: int
    duration: int
    start_date: str
    end_date: str

class User(SQLModel):
    id: Optional[int] | None = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str
    phone_number: int
    country_code: int
    password: str
    projects: list[Project] = []