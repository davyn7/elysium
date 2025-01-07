from app.db.config import db_client
from app.personal_finance.models import (
    UserFS,
    Incomes
)
from app.personal_finance.schemas import (
    UserFSBase,
    RecurringIncomeBase
)
from app.auth.db import User

async def add_user_db(userfs: UserFSBase, user: User, untaxable: float):
    async with db_client.get_async_session() as session:
        print("HEEEELLLOO I'M HERE")
        try:
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
            session.rollback()
            raise e

async def add_recurring_income_db(income: RecurringIncomeBase):
    async with db_client.get_async_session() as session:
        session.add(income)
        await session.commit()
        await session.refresh(income)
        return income