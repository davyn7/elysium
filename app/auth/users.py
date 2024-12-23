from sqlmodel import Field, SQLModel
from typing import Optional
import uuid
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users import schemas
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass
    # team_id: Optional[int]  # Include team_id in the read schema


class UserCreate(schemas.BaseUserCreate):
    pass
    # team_id: Optional[int]  # Include team_id in the create schema


class UserUpdate(schemas.BaseUserUpdate):
    pass
    # team_id: Optional[int]  # Include team_id in the update schema