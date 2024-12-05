# /c/Users/관리자/Desktop/projects/todos/src/main.py 내용
from fastapi import FastAPI
from src.api import todo, user

app = FastAPI()
app.include_router(todo.router)
app.include_router(user.router)

# 첫 화면 API
@app.get("/")
def health_check_handler():
    return {"ping": "pong"}