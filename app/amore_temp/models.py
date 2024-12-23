from sqlmodel import Field, SQLModel
from typing import Optional
from app.db.config import db_client

current_schema = "Amore"

class Ingredient(SQLModel, table=True):
    __tablename__ = "ingredients_table"
    __table_args__ = {"schema": current_schema}
    
    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    package: Optional[str]
    cost_per_package: float
    units_per_package: float
    unit_of_measurement: str
    shrinkage_percentage: float
    price_per_unit: float

class Dish(SQLModel, table=True):
    __tablename__ = "dishes_table"
    __table_args__ = {"schema": current_schema}
    
    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    description: Optional[str]
    cost: float
    batches: Optional[int]
    cost_per_batch: Optional[float]
    contains_secret: bool

class Secret(SQLModel, table=True):
    __tablename__ = "secrets_table"
    __table_args__ = {"schema": current_schema}
    
    id: Optional[int] | None = Field(default=None, primary_key=True)
    name: str
    description: Optional[str]
    cost: float
    batches: Optional[int]
    cost_per_batch: Optional[float]
    contains_secret: bool

class Recipe(SQLModel, table=True):
    __tablename__ = "recipe_table"
    __table_args__ = {"schema": current_schema}
    
    id: Optional[int] | None = Field(default=None, primary_key=True)
    dish_id: int
    ingredient_id: Optional[int]
    secret_id: Optional[int]
    quantity: float
    cost: Optional[float]

class SecretRecipe(SQLModel, table=True):
    __tablename__ = "secretrecipe_table"
    __table_args__ = {"schema": current_schema}

    id: Optional[int] | None = Field(default=None, primary_key=True)
    secret_id: int
    ingredient_id: int
    quantity: float
    cost: Optional[float]

db_client.create_schema(current_schema)
    