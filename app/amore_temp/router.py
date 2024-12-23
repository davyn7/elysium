from fastapi import Depends, APIRouter
from app.auth.db import User
# from app.auth.user_manager import current_active_user
from app.amore_temp.models import Ingredient, Dish, Secret, Recipe, SecretRecipe
from app.db.config import db_client
from sqlmodel import select

router = APIRouter(prefix="/amore", tags=["amore-liora"])

@router.get("/health_check")
async def health_check():
    return {"status": "ok"}
    
@router.post("/add_ingredient")
async def add_ingredient(ingredient: Ingredient):
    try:
        async with db_client.get_async_session() as session:
            session.add(ingredient)
            await session.commit()
        return {"message": "Ingredient added"}
    except Exception as e:
        return e
    
@router.post("/edit_ingredient")
async def edit_ingredient(ingredient: Ingredient):
    try:
        # What if I only wanna edit a single field?
        async with db_client.get_async_session() as session:
            curr_ingredient = session.get(Ingredient, ingredient.id)
            curr_ingredient.name = ingredient.name
            curr_ingredient.package = ingredient.package
            curr_ingredient.cost_per_package = ingredient.cost_per_package
            curr_ingredient.units_per_package = ingredient.units_per_package
            curr_ingredient.unit_of_measurement = ingredient.unit_of_measurement
            curr_ingredient.shrinkage_percentage = ingredient.shrinkage_percentage
            curr_ingredient.price_per_unit = ingredient.price_per_unit
            session.add(curr_ingredient)
            await session.commit()
        return {"message": "Ingredient updated"}
    except Exception as e:
        return e
    
@router.post("/delete_ingredient")
async def delete_ingredient(ingredient_id: int):
    try:
        async with db_client.get_async_session() as session:
            ingredient = session.get(Ingredient, ingredient_id)
            session.delete(ingredient)
            await session.commit()
        return {"message": "Ingredient deleted"}
    except Exception as e:
        return e
    
@router.post("/add_recipe")
async def add_recipe(recipe: Recipe):
    try:
        async with db_client.get_async_session() as session:
            session.add(recipe)
            await session.commit()
        return {"message": "Recipe added"}
    except Exception as e:
        return e

# @router.post("/add_recipe")
# async def add_project(recipe: Recipe, _: User = Depends(current_active_user)):
#     try:
#         async with db_client.get_async_session() as session:
#             session.add(recipe)
#             await session.commit()
#         return {"message": "Recipe added"}
#     except Exception as e:
#         return {"message": f"{str(e)} ERROR IS HERE"}