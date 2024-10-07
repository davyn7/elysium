from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
from app.auth.router import router as auth_router
from app.project_management.router import router as project_management

load_dotenv()

app = FastAPI()

app.include_router(auth_router)
app.include_router(project_management)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# @app.get("/test_db_connection")
# def test_db_connection():
#     conn = psycopg.connect(
#         dbname=os.getenv("DB_NAME"),
#         user=os.getenv("DB_USER"),
#         password=os.getenv("DB_PASSWORD"),
#         host=os.getenv("DB_HOST"),
#         port=os.getenv("DB_PORT")
#     )
#     conn.close()
#     return {"message": "Connection successful"}

# @app.post("/test_db_insert")
# def test_db_insert(hero: test_schema.Hero):
#     with Session(engine) as session:
#         session.add(hero)
#         session.commit()
#     return {"message": "Data inserted"}

# @app.post("/test_db_delete")
# def test_db_delete(hero_id: int):
#     with Session(engine) as session:
#         hero = session.get(test_schema.Hero, hero_id)
#         session.delete(hero)
#         session.commit()
#     return {"message": "Data deleted"}

# @app.post("/test_db_update")
# def test_db_update(hero: test_schema.TempHero):
#     with Session(engine) as session:
#         curr_hero = session.get(test_schema.Hero, hero.id)
#         curr_hero.name = hero.name
#         curr_hero.secret_name = hero.secret_name
#         curr_hero.age = hero.age
#         session.add(curr_hero)
#         session.commit()
#     return {"message": "Data updated"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}