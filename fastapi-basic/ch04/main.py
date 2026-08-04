from fastapi import FastAPI
from routers.todo import todo_router

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {
        "message": "welcome ch03!!"
    }

# todo 애플리케이션 개발 - CRUD
app.include_router(todo_router)