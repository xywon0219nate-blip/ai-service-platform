# /books or /book => CRUD
# Book 클래스 = {
#    id: int
#    item: BookItem
#}
#BookItem 클래스 = {
#    title: str
#    publisher: str
#    price: int
#    isbn: int
#}

#-----------------------------------------
# 
#-----------------------------------------

from fastapi import APIRouter, Path
from pydantic import BaseModel

book_router = APIRouter()

# Item model
class Book(BaseModel):
   id: int
   item: BookItem

# Book model
class BookItem(BaseModel):
   id: int
   title: str
   price: int
   isbn: int

# Book list
book_list = []    

# C: Create
@book_router.post("/book")
async def create_book(book: Book) -> dict:
   book_list.append(book)
   return {
      "message": "create!!",
      "book_list": book_list
   }

# R: Read - all
@book_router.get("/book/all")
async def read_book() -> dict:
   return {
      "message::All": book_list
   }

# R: Read - id별 조회
@book_router.get("/book/{id}")
async def read_book(id: int) -> dict:
   for book in book_list:
      if book.id == id:
         return {
               "book": book
         }
   return {
      "message": "read!!"
   }


# U: Update
@book_router.put("/book/{id}")
async def update_book(new_item:Book, id:int = Path(..., title="id")) -> dict:
   for book in book_list:
      if  book.id == id:
         book.item = new_item
         return { "message": "update 성공!!"}
   return {
      "message": "id 확인!!"
   }


# D: Delete - 전체 삭제 
@book_router.delete("/book")
async def delete_todo() -> dict:
   if len(book_list) > 0:
      book_list.clear()
      return { "message": "삭제 성공!!"}
   return {
      "message": "데이터 없음!!"
   }

# D: Delete - id별 
@book_router.delete("/book/{id}")
async def delete_book(id: int) -> dict:
   for index in range(len(book_list)):
      book = book_list[index]
      if book.id == id:
         book_list.pop(index)
         return { "message": "삭제 성공!!"}
   return {
      "message": "id 확인!!"
   }
