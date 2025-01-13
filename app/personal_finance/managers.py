from app.personal_finance.schemas import (
    UserFSBase,
    RecurringIncomeBase,
    SupplementaryIncomeBase,
    BonusBase
)
from app.personal_finance.db import (
    get_user_db,
    add_user_db,
    edit_user_db,
    get_untaxable_db,
    add_recurring_income_db
)
from app.auth.db import User
from datetime import date
from typing import List
import json

MONTHS = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

MONTHS_REVERSED = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

DAYS = {31: [1, 3, 5, 7, 8, 10, 12], 30: [4, 6, 9, 11], 28: [2]}

BRACKETS = {
    1: {"cap": 60000000, "rate": 0.05},
    2: {"cap": 250000000, "rate": 0.15},
    3: {"cap": 500000000, "rate": 0.25},
    4: {"cap": 5000000000, "rate": 0.3},
    5: {"rate": 0.35}
}

MAX_TAX = {
    1: BRACKETS[1]["cap"] * BRACKETS[1]["rate"],
    2: (BRACKETS[2]["cap"] - BRACKETS[1]["cap"]) * BRACKETS[2]["rate"],
    3: (BRACKETS[3]["cap"] - BRACKETS[2]["cap"]) * BRACKETS[3]["rate"],
    4: (BRACKETS[4]["cap"] - BRACKETS[3]["cap"]) * BRACKETS[4]["rate"],
}

MAX_NET = {
    1: BRACKETS[1]["cap"] - MAX_TAX[1],
    2: BRACKETS[1]["cap"] - MAX_TAX[1] + BRACKETS[2]["cap"] - MAX_TAX[2],
    3: BRACKETS[1]["cap"] - MAX_TAX[1] + BRACKETS[2]["cap"] - MAX_TAX[2] + BRACKETS[3]["cap"] - MAX_TAX[3],
    4: BRACKETS[1]["cap"] - MAX_TAX[1] + BRACKETS[2]["cap"] - MAX_TAX[2] + BRACKETS[3]["cap"] - MAX_TAX[3] + BRACKETS[4]["cap"] - MAX_TAX[4]
}

UNTAXABLE = [54000000, 4500000]

TODAY = date.today()

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
    
    async def get_user(self):
        return await get_user_db(self.user)
    
    async def add_user(self):
        return await add_user_db(self.userfs, self.user, self.calculate_untaxable())
    
    async def edit_user(self):
        return await edit_user_db(self.userfs, self.user, self.calculate_untaxable())

class RecurringIncomeManager:
    def __init__(self, income: RecurringIncomeBase, bonuses: List[BonusBase], user: User):
        self.income = income
        self.bonuses = bonuses
        self.user = user

    def calculate_income(self, untaxable):
        income = self.income
        bonuses = self.bonuses

        start, end = 1, 12
        months = 12

        if income.end.year == TODAY.year:
            end = income.end.month
            months = income.end.month
        if income.start.year == TODAY.year:
            start = income.start.month
            months -= income.start.month

        monthly = {i: 0 for i in range(1, 13)}
        annual = 0
        amount = income.amount

        monthly_bonuses = monthly.copy()
        annual_bonuses = 0

        if income.frequency == "monthly":
            annual += (amount * months)
        else:
            annual += (amount * months / 12)
            amount = annual / months
        
        if not income.is_gross:
            # Gross up
            annual = calculate_gross(annual, untaxable)
            amount = annual / months
        
        for m in range(start, end + 1):
            monthly[m] += amount

        monthly_base = monthly.copy()
        annual_base = annual

        for bonus in bonuses:
            amount_b = bonus.amount
            if months < 12:
                amount_b = amount_b * months / 12
            if bonus.form == "fixed" and not income.is_gross:
                amount_b = calculate_marginal_gross(amount_b, annual_base, untaxable) # Calculate marginal gross
            elif bonus.form == "percentage":
                amount_b *= annual_base
            elif bonus.form == "months":
                amount_b *= amount
        
            for m in bonus.months_paid:
                monthly_bonuses[MONTHS[m]] += amount_b
                monthly[MONTHS[m]] += amount_b
                annual_bonuses += amount_b
                annual += amount_b

        ret = {
            "monthly": monthly,
            "annual": annual,
            "monthly_base": monthly_base,
            "annual_base": annual_base,
            "monthly_bonuses": monthly_bonuses,
            "annual_bonuses": annual_bonuses
        }

        return ret

    async def add_recurring_income(self):
        untaxable = await get_untaxable_db(self.user)
        i = self.calculate_income(untaxable)
        return await add_recurring_income_db(self.income, self.bonuses, self.user, i)

class SupplementaryIncomeManager:
    def __init__(self):
        pass

class IncomesManager:
    def __init__(self):
        pass

### Helper Functions

def calculate_gross(income, untaxable):
    if income <= untaxable:
        return income
    income -= untaxable
    ret = [untaxable]
    if income <= MAX_NET[1]:
        ret.append(income / (1 - BRACKETS[1]["rate"]))
    else:
        ret.append(BRACKETS[1]["cap"])
        if income <= MAX_NET[2]:
            ret.append((income - MAX_NET[1]) / (1 - BRACKETS[2]["rate"]))
        else:
            ret.append(BRACKETS[2]["cap"])
            if income <= MAX_NET[3]:
                ret.append((income - MAX_NET[2]) / (1 - BRACKETS[3]["rate"]))
            else:
                ret.append(BRACKETS[3]["cap"])
                if income <= MAX_NET[4]:
                    ret.append((income - MAX_NET[3]) / (1 - BRACKETS[4]["rate"]))
                else:
                    ret.append(BRACKETS[4]["cap"])
                    ret.append((income - MAX_NET[4]) / (1 - BRACKETS[5]["rate"]))
    return sum(ret)

def calculate_marginal_gross(income, gross, untaxable):
    net = gross - calculate_tax(gross - untaxable)
    return calculate_gross(income + net, untaxable) - net

def calculate_tax(income):
    ret = []
    if income <= BRACKETS[1]["cap"]:
        ret.append(income * BRACKETS[1]["rate"])
    else:
        ret.append(MAX_TAX[1])
        if income <= BRACKETS[2]["cap"]:
            ret.append((income - BRACKETS[1]["cap"]) * BRACKETS[2]["rate"])
        else:
            ret.append(MAX_TAX[2])
            if income <= BRACKETS[3]["cap"]:
                ret.append((income - BRACKETS[2]["cap"]) * BRACKETS[3]["rate"])
            else:
                ret.append(MAX_TAX[3])
                if income <= BRACKETS[4]["cap"]:
                    ret.append((income - BRACKETS[3]["cap"]) * BRACKETS[4]["rate"])
                else:
                    ret.append(MAX_TAX[4])
                    ret.append((income - BRACKETS[4]["cap"]) * BRACKETS[5]["rate"])
    return sum(ret)

def reversetojson(d):
    income = {}
    for m, i in d.items():
        income[MONTHS_REVERSED[m]] = i
    return json.dumps(income)