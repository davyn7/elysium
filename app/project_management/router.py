from fastapi import Depends, APIRouter
from app.auth.db import User
from app.auth.user_manager import current_active_user
from app.project_management.models import Hero
from app.db.config import db_client
from sqlmodel import select

router = APIRouter(prefix="/project-management", tags=["project-management"])

@router.get("/health_check")
async def health_check():
    return {"status": "ok"}

@router.post("/add_project")
async def add_project(hero: Hero, _: User = Depends(current_active_user)):
    try:
        async with db_client.get_async_session() as session:
            session.add(hero)
            await session.commit()
        return {"message": "Project added"}
    except Exception as e:
        return {"message": f"{str(e)} ERROR IS HERE"}
    
@router.get("/get_projects")
async def get_projects(hero_id: int = 0, _: User = Depends(current_active_user)):
    try:
        async with db_client.get_async_session() as session:
            # statement = select(Hero).where(Hero.id == hero_id)
            # result = await session.execute(statement)
            result = await session.get(Hero, hero_id)
            return result
    except Exception as e:
        return {"message": f"{str(e)} display hero error"}