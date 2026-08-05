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
@todo_router.get("/todo/{id}", response_model=Todo)
async def getId(id: int,
               db: Session = Depends(get_db)) -> dict:
   # for todo in todo_list:
   #    if todo.id == id:
   #       return {
   #             "message": todo
   #       }
   
   todo = db.get(TodoModel,id) 

   if todo is None:
      raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail="Todo with supplied ID doesn't exist",
      )
   return todo



# U
@todo_router.put("/todo/{id}",response_model=Todo)
async def update_todo(todo_data: TodoItem, id: int = Path(...),db: Session = Depends(get_db)) -> dict:
   
   # for todo in todo_list:
   #    if todo.id == id:
   #       todo.item = todo_data.item
   #       return {
   #             "message": "todo 업데이트 성공!!"
   #       }

   todo = db.get(TodoModel,id) #

   if todo is None:
      raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo with supplied ID doesn't exist",
         )

   Todo.item = todo_data.item
   db.commit() # updata 실행
   db.refresh(todo)

   return todo


# D
# all
@todo_router.delete("/todo")
async def deleteAll( db: Session = Depends(get_db)) -> dict:
   result = db.execute()

   # if len(todo_list) > 0:
   #    todo_list.clear()
      return {
         "message": "todo_list 삭제 성공!!"
      }
   return {
      "message": "todo_list 데이터가 존재하지 않음"
   }

# id별 todo삭제
@todo_router.delete("/todo/{id}", response_model=Todo)
async def deleteId(id: int, db: Session = Depends(get_db)) -> dict:
   # for index in range(len(todo_list)):
   #    todo = todo_list[index]
   #    if todo.id == id:
   #       todo_list.pop(index)


   todo = db.get(TodoModel,id)
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