from sqlmodel import Field, SQLModel
from typing import Optional
import uuid
from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from fastapi_users import schemas
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin

class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass