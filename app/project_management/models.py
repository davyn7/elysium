from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from app.db.config import db_client
from typing import List
from uuid import UUID
from app.auth.db import User
# from datetime import datetime

current_schema = "Project-Management"

# class Hero(SQLModel, table=True):
#     __tablename__ = "hero_table"
#     __table_args__ = {"schema": current_schema}
    
#     id: Optional[int] | None = Field(default=None, primary_key=True)
#     name: str
#     secret_name: str
#     age: int | None = None

class UserPM(User, table=True):
    __tablename__ = "project_user_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None = Field(default=None, primary_key=True)
    team_id: Optional[int] = Field(foreign_key=f"{current_schema}.teams_table.id")
    team: Optional["Team"] = Relationship(back_populates="users")


class Project(SQLModel, table=True):
    __tablename__ = "projects_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    description: str
    start_date: str
    end_date: str
    done: int
    teams: List["Team"] = Relationship(back_populates="project")
    # tasks: List["Task"] = Relationship(back_populates="project")


# Team table (each team is related to a project and has multiple users)
class Team(SQLModel, table=True):
    __tablename__ = "teams_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    # user_ids: List[UUID] = Field(default=[], foreign_key="user.id")
    # user: List[User] = Relationship(back_populates="team")  # Link to users
    project_id: Optional[int] = Field(default=None, foreign_key=f"{current_schema}.projects_table.id")
    project: Optional["Project"] = Relationship(back_populates="teams")
    users: List["UserPM"] = Relationship(back_populates="team")


# # Task table (each task is related to a project and has multiple PICs)
# class Task(SQLModel, table=True):
#     __tablename__ = "tasks_table"
#     __table_args__ = {"schema": current_schema}

#     id: Optional[int] = Field(default=None, primary_key=True)
#     project_id: int = Field(foreign_key="projects_table.id")
#     title: str
#     description: str
#     start_date: str
#     end_date: str
#     status: str
#     # pics: List[User] = Relationship(link_model="TaskUserLink")  # Link to users
#     # pics_id: List[UUID] = Field(default=[], foreign_key="user.id")

#     # project: Optional[Project] = Relationship(back_populates="tasks")


# # Link table for Task and User (to support many-to-many PICs for each task)
# class TaskUserLink(SQLModel, table=True):
#     __tablename__ = "task_user_link"
#     __table_args__ = {"schema": current_schema}

#     task_id: int = Field(foreign_key="tasks_table.id", primary_key=True)
#     user_id: UUID = Field(foreign_key="user.id", primary_key=True)  # Use UUID to match User table

db_client.create_schema(current_schema)