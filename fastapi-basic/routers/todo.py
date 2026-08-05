from fastapi import APIRouter, Path
from pydantic import BaseModel

todo_router = APIRouter()

# Item model
class Item(BaseModel):
    item: str
    status: str

# Todo model
class Todo(BaseModel):
    id: int
    item: Item

# Todo list
todo_list = []    

# C: Create
@todo_router.post("/todo")
async def create_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {
        "message": "create!!",
        "todo_list": todo_list
    }

# R: Read - all
@todo_router.get("/todo/all")
async def read_todo() -> dict:
    return {
        "message::All": todo_list
    }

# R: Read - id별 조회
@todo_router.get("/todo/{id}")
async def read_todo(id: int) -> dict:
    for todo in todo_list:
        if todo.id == id:
            return {
                "todo": todo
            }
    return {
        "message": "read!!"
    }


# U: Update
@todo_router.put("/todo/{id}")
async def update_todo(new_item:Item, id:int = Path(..., title="id")) -> dict:
    for todo in todo_list:
        if  todo.id == id:
            todo.item = new_item
            return { "message": "update 성공!!"}
    return {
        "message": "id 확인!!"
    }


# D: Delete - 전체 삭제 
@todo_router.delete("/todo")
async def delete_todo() -> dict:
    if len(todo_list) > 0:
        todo_list.clear()
        return { "message": "삭제 성공!!"}
    return {
        "message": "데이터 없음!!"
    }

# D: Delete - id별 
@todo_router.delete("/todo/{id}")
async def delete_todo(id: int) -> dict:
    for index in range(len(todo_list)):
        todo = todo_list[index]
        if todo.id == id:
            todo_list.pop(index)
            return { "message": "삭제 성공!!"}
    return {
        "message": "id 확인!!"
    }
