from fastapi import FastAPI
from routes.todo import todo_router
# from routes.book import book_router
from database import Base, engine

# todos 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(todo_router) # todo 애플리케이션
# app.include_router(book_router) # 도서관리 애플리케이션