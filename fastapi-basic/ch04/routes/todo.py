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

    return { "todos": todos } # [{"id":1, "item": "HTML"}, ...]



# id
@todo_router.get("/todo/{id}")
async def getId(id: int) -> dict:
    for todo in todo_list:
        if todo.id == id:
            return {
                "message": todo
            }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo with supplied ID doesn't exist",
    )



# U
@todo_router.put("/todo/{id}")
async def update_todo(todo_data: TodoItem, id: int = Path(...)) -> dict:
    for todo in todo_list:
        if todo.id == id:
            todo.item = todo_data.item
            return {
                "message": "todo 업데이트 성공!!"
            }
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo with supplied ID doesn't exist",
        )

# D
# all
@todo_router.delete("/todo")
async def deleteAll() -> dict:
    if len(todo_list) > 0:
        todo_list.clear()
        return {
            "message": "todo_list 삭제 성공!!"
        }
    return {
        "message": "todo_list 데이터가 존재하지 않음"
    }

# id
@todo_router.delete("/todo/{id}")
async def deleteId(id: int) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == id:
            todo_list.pop(index)
            return {
                "message": "todo 삭제 완료!!"
            }
    raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo with supplied ID doesn't exist",
        )
