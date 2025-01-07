from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from app.db.config import db_client
from typing import List
from uuid import UUID
from app.auth.db import User
# from datetime import datetime

current_schema = "Project-Management"

# User to Tasks: Many-to-Many relationship
# User to Teams: Many-to-Many relationship
# User to Projects: Many-to-Many relationship

class UserPM(SQLModel, table=True):
    __tablename__ = "userpm_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None = Field(default=None, primary_key=True)
    user_id: Optional[UUID] = Field(default=None)
    first_name: str
    last_name: str
    email: str

    # Update these
    # role: str # 'admin', 'member'
    # project_id: Optional[int] = Field(default=None, foreign_key=f"{current_schema}.projects_table.id")
    # project: Optional["Project"] = Relationship(back_populates="users")
    # team_id: Optional[int] = Field(default=None, foreign_key=f"{current_schema}.teams_table.id")
    # team: Optional["Team"] = Relationship(back_populates="users")

# Project table (each project has multiple teams, sprints, and tasks)
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
    sprints: List["Sprint"] = Relationship(back_populates="project")
    tasks: List["Task"] = Relationship(back_populates="project")
    # users: List["UserPM"] = Relationship(back_populates="project")

# Team table (each team is related to a project and has multiple users)
class Team(SQLModel, table=True):
    __tablename__ = "teams_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    project_id: Optional[int] = Field(default=None, foreign_key=f"{current_schema}.projects_table.id")
    project: Optional["Project"] = Relationship(back_populates="teams")
    # user_ids: List[UUID] = Field(default=[], foreign_key="user.id")
    # user: List[User] = Relationship(back_populates="team")  # Link to users
    # users: List["UserPM"] = Relationship(back_populates="team")

# Sprint table (each sprint is related to a project and has multiple tasks)
class Sprint(SQLModel, table=True):
    __tablename__ = "sprints_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None = Field(default=None, primary_key=True)
    title: str
    description: str
    start_date: str
    end_date: str
    done: int
    project_id: Optional[int] = Field(default=None, foreign_key=f"{current_schema}.projects_table.id")
    project: Optional["Project"] = Relationship(back_populates="sprints")
    tasks: List["Task"] = Relationship(back_populates="sprint")

# Task table (each task is related to a sprint & project and has multiple PICs)
class Task(SQLModel, table=True):
    __tablename__ = "tasks_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None  = Field(default=None, primary_key=True)
    title: str
    description: str
    start_date: str
    end_date: str
    mandays: int
    status: str
    sprint_id: int = Field(default=None, foreign_key=f"{current_schema}.sprints_table.id")
    sprint: Optional["Sprint"] = Relationship(back_populates="tasks")
    project_id: int = Field(default=None, foreign_key=f"{current_schema}.projects_table.id")
    project: Optional["Project"] = Relationship(back_populates="tasks")

    # pics: List[User] = Relationship(link_model="TaskUserLink")  # Link to users
    # pics_id: List[UUID] = Field(default=[], foreign_key="user.id")


# # Link table for Task and User (to support many-to-many PICs for each task)
# class TaskUserLink(SQLModel, table=True):
#     __tablename__ = "task_user_link"
#     __table_args__ = {"schema": current_schema}

#     task_id: int = Field(foreign_key="tasks_table.id", primary_key=True)
#     user_id: UUID = Field(foreign_key="user.id", primary_key=True)  # Use UUID to match User table

db_client.create_schema(current_schema)