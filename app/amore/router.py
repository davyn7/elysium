from fastapi import Depends, APIRouter
from app.auth.db import User
from app.auth.user_manager import current_active_user
from app.amore.models import Recipe
from app.db.config import db_client
from sqlmodel import select

router = APIRouter(prefix="/amore", tags=["amore-liora"])

@router.get("/health_check")
async def health_check():
    return {"status": "ok"}

@router.post("/add_recipe")
async def add_project(recipe: Recipe, _: User = Depends(current_active_user)):
    try:
        async with db_client.get_async_session() as session:
            session.add(recipe)
            await session.commit()
        return {"message": "Recipe added"}
    except Exception as e:
        return {"message": f"{str(e)} ERROR IS HERE"}