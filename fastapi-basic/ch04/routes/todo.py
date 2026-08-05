from fastapi import APIRouter, Path, HTTPException, status, Depends
from schemas.todo_schema import Todo, TodoItem, TodoItems

from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from database import get_db
from models.todo_model import TodoModel

todo_router = APIRouter()

# todo_list
todo_list = []

# C: Insert 
@todo_router.post("/todo", 
                    response_model=Todo,
                    status_code=status.HTTP_201_CREATED)
async def add_todo(todo: TodoItem,
                    db: Session = Depends(get_db)) -> dict:
    todo_data = TodoModel(item=todo.item)

    db.add(todo_data)
    db.commit()
    db.refresh(todo_data)

    return todo_data    


# R : Select
# all
@todo_router.get("/todo", response_model=TodoItems)
async def getAll(db: Session = Depends(get_db)) -> list[TodoItem]:
    result = db.execute(
        select(TodoModel).order_by(TodoModel.id)
    )
    todos = result.scalars().all()

    return { "todos": todos } # {"todos": [{"id":1, "item": "HTML"}, ...] }


# id
@todo_router.get("/todo/{id}", response_model=Todo)
async def getId(id: int,
                db: Session=Depends(get_db)) -> dict:
    todo = db.get(TodoModel, id) # -> select ~~

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo with supplied ID doesn't exist",
        )

    return todo


# U
@todo_router.put("/todo/{id}", response_model=Todo)
async def update_todo(todo_data: TodoItem, 
                        id: int = Path(...),
                        db: Session=Depends(get_db)) -> dict:
    todo = db.get(TodoModel, id) # ORM(SQL 생성) => DB(SQL 실행) => 결과 리턴

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo with supplied ID doesn't exist",
        )

    todo.item = todo_data.item   # DB Old item => New item 교체
    db.commit()  # update 실행 - update todos set item=? where id=?
    db.refresh(todo) # update 실행 - update todos set item='JS' where id=1

    return todo


# D
# all - 전체 삭제
@todo_router.delete("/todo")
async def deleteAll(db: Session = Depends(get_db)) -> dict:
    result = db.execute(
        delete(TodoModel)
    )
    db.commit()

    if result.rowcount == 0:
        return {
            "message": "todos 테이블의 데이터가 존재하지 않음"
        }
    return {
        "message": "전체 데이터 삭제 완료!!"
    }


# id별 todo 삭제
@todo_router.delete("/todo/{id}")
async def deleteId(id: int,
                    db: Session=Depends(get_db)) -> dict:
    todo = db.get(TodoModel, id)
    if todo is None:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo with supplied ID doesn't exist",
            )
    db.delete(todo)
    db.commit()

    return {
        "message": "todo 삭제 완료!!"
    }
