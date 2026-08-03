from fastapi import FastAPI
#from routers.hello import hello_router
from routers.todo import todo_router
from routers.book import book_router


app = FastAPI() # FastAPI 서버 생성 

@app.get("/")
async def welcome() -> dict:   # { key: value ...}
    return {
        "message": "GET:: welcome to FastAPI world!!"
    }

# @app.post("/")
# async def welcome() -> dict:   # { key: value ...}
#     return {
#         "message": "POST:: welcome to FastAPI world!!"
#     }

# todo 애플리케이션개발 - CRUD
# app.include_router(hello_router)
app.include_router(todo_router) # todo 애플리케이션
app.include_router(book_router) # 도서관리 애플리케이션
