from fastapi import FastAPI
from routers.todo import todo_router
from routers.book import book_router

app = FastAPI()

@app.get("/")
async def welcome() -> dict:
    return {
        "message": "welcome ch03!!"
    }


app.include_router(todo_router) # todo 애플리케이션
app.include_router(book_router) # 도서관리 애플리케이션