from typing import Union
from fastapi import FastAPI
from dotenv import load_dotenv
from app.auth.router import router as auth_router
from app.project_management.router import router as project_management
from app.personal_finance.router import router as personal_finance
# from app.amore.router import router as amore
from app.amore_temp.router import router as amore

load_dotenv()

app = FastAPI()

app.include_router(auth_router)
app.include_router(project_management)
app.include_router(personal_finance)
app.include_router(amore)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}