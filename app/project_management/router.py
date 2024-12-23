from fastapi import Depends, APIRouter
from app.auth.db import User
from app.auth.user_manager import current_active_user
# from app.project_management.models import Project, Task, TempTask
from app.project_management.models import Project, Team, Sprint, Task
from app.db.config import db_client
from sqlmodel import select

router = APIRouter(prefix="/project-management", tags=["project-management"])

@router.get("/health_check")
async def health_check():
    return {"status": "ok"}

@router.post("/add_team")
async def add_team(team: Team, _: User = Depends(current_active_user)):
    try:
        async with db_client.get_async_session() as session:
            session.add(team)
            await session.commit()
        return {"message": "Team added"}
    except Exception as e:
        return e
    
# @router.post("/add_user")
# async def add_user(user: UserPM, _: User = Depends(current_active_user)):
#     try:
#         async with db_client.get_async_session() as session:
#             session.add(user)
#             await session.commit()
#         return {"message": "User added"}
#     except Exception as e:
#         return e

@router.post("/add_project")
async def add_project(project: Project, _: User = Depends(current_active_user)):
    try:
        async with db_client.get_async_session() as session:
            session.add(project)
            await session.commit()
        return {"message": "Project added"}
    except Exception as e:
        return e
    
@router.get("/get_project")
async def get_project(project_id: int = 0, _: User = Depends(current_active_user)):
    try:
        async with db_client.get_async_session() as session:
            # statement = select(Hero).where(Hero.id == hero_id)
            # result = await session.execute(statement)
            result = await session.get(Project, project_id)
            return result
    except Exception as e:
        return e
    
@router.get("/get_all_projects")
async def get_all_projects(_: User = Depends(current_active_user)):
    try:
        async with db_client.get_async_session() as session:
            statement = select(Project)
            result = await session.execute(statement)
            return result.all()
    except Exception as e:
        return e
    
@router.post("/add_sprint")
async def add_sprint(sprint: Sprint, _: User = Depends(current_active_user)):
    try:
        async with db_client.get_async_session() as session:
            session.add(sprint)
            await session.commit()
        return {"message": "Sprint added"}
    except Exception as e:
        return e
    
@router.post("/add_task")
async def add_task(task: Task, _: User = Depends(current_active_user)):
    try:
        async with db_client.get_async_session() as session:
            session.add(task)
            await session.commit()
        return {"message": "Task added"}
    except Exception as e:
        return e
    
# @router.post("/add_task")
# async def add_task(task: Task, _: User = Depends(current_active_user)):
#     try:
#         async with db_client.get_async_session() as session:
#             session.add(task)
#             await session.commit()
#         return {"message": "Task added"}
#     except Exception as e:
#         return {"message": f"{str(e)} display hero error"}
    
# @router.post("/update_task_status")
# async def update_task_status(task: TempTask, _: User = Depends(current_active_user)):
#     try:
#         async with db_client.get_async_session() as session:
#             curr_task = session.get(Task, task.id)
#             curr_task.status = task.status
#             session.add(curr_task)
#             # Update Project Progress too
#             await session.commit()
#         return {"message": "Task status updated"}
#     except Exception as e:
#         return {"message": f"{str(e)} display hero error"}
    
# @router.post("/edit_task")
# async def edit_task(task: TempTask, _: User = Depends(current_active_user)):
#     try:
#         async with db_client.get_async_session() as session:
#             pass
#         return {"message": "Task edited"}
#     except Exception as e:
#         return {"message": f"{str(e)} display hero error"}