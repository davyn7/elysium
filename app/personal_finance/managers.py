from app.personal_finance.schemas import (
    UserFSBase,
    RecurringIncomeBase,
    SupplementaryIncomeBase
)
from app.personal_finance.db import (
    add_user_db,
    add_recurring_income_db
)
from app.auth.db import User

UNTAXABLE = [54000000, 4500000]

class UserFSManager:
    def __init__(self, userfs: UserFSBase, user: User):
        self.userfs = userfs
        self.user = user

    def calculate_untaxable(self):
        ret = UNTAXABLE[0]
        if self.userfs.marital_status:
            ret += UNTAXABLE[1]
        for i in range(3):
            if self.userfs.kids > i:
                ret += UNTAXABLE[1]
        return ret
    
    async def add_user(self):
        print("PASSED HERE TOO")
        return await add_user_db(self.userfs, self.user, self.calculate_untaxable())

class RecurringIncomeManager:
    def __init__(self, income: RecurringIncomeBase):
        self.income = income
        self.x = 1
        self.y = 2
        self.z = 3

    async def add_recurring_income(self):
        x = await add_recurring_income_db(self.income)
        return x

class SupplementaryIncomeManager:
    def __init__(self):
        pass

class IncomesManagers:
    def __init__(self):
        pass