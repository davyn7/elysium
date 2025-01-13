from app.db.config import db_client
from app.personal_finance.models import (
    UserFS
)
from app.personal_finance.schemas import (
    UserFSBase,
    RecurringIncomeBase,
    BonusBase
)
from app.auth.db import User
from sqlmodel import select
from typing import List
import json

async def get_user_db(user: User):
    async with db_client.get_async_session() as session:
        try:
            existing = await session.execute(select(UserFS).where(UserFS.user_id == user.id))
            return existing.first()[0]
        except Exception as e:
            raise e

async def add_user_db(userfs: UserFSBase, user: User, untaxable: float):
    async with db_client.get_async_session() as session:
        try:
            existing = await session.execute(select(UserFS).where(UserFS.user_id == user.id))
            if existing.first():
                return {"message": "UserFS already exists"}
            new_user = UserFS(
                user_id=user.id,
                email=user.email,
                first_name=userfs.first_name,
                last_name=userfs.last_name,
                marital_status=userfs.marital_status,
                kids=userfs.kids,
                untaxable=untaxable
            )
            session.add(new_user)
            await session.commit()
            return {"message": "UserFS added"}
        except Exception as e:
            await session.rollback()
            raise e
        
async def edit_user_db(userfs: UserFSBase, user: User, untaxable: float):
    async with db_client.get_async_session() as session:
        try:
            existing = await session.execute(select(UserFS).where(UserFS.user_id == user.id))
            temp = existing.first()
            if not temp:
                return {"message": "UserFS does not exist"}
            print(temp)
            temp = temp[0]
            temp.first_name = userfs.first_name
            temp.last_name = userfs.last_name
            temp.marital_status = userfs.marital_status
            temp.kids = userfs.kids
            temp.untaxable = untaxable
            session.add(temp)
            await session.commit()
            return {"message": "UserFS updated"}
        except Exception as e:
            await session.rollback()
            raise e
        
async def get_untaxable_db(user: User):
    async with db_client.get_async_session() as session:
        try:
            existing = await session.execute(select(UserFS).where(UserFS.user_id == user.id))
            return existing.first()[0].untaxable
        except Exception as e:
            raise e

async def add_recurring_income_db(base: RecurringIncomeBase, bonuses: List[BonusBase], user: User, i):
    async with db_client.get_async_session() as session:
        try:
            # income = Incomes(
            #     user_id = user.id,
            #     name = base.name,
            #     category = "recurring",
            #     basic_income = base.model_dump_json(),
            #     additional_income = json.dumps([bonus.model_dump() for bonus in bonuses]),
            #     income_obj = json.dumps(i),
            #     start = base.start,
            #     end = base.end
            # )
            # session.add(income)
            await session.commit()
            return {"message": "Recurring income added"}
        except Exception as e:
            raise e

    
