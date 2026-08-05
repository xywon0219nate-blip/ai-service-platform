from pydantic import BaseModel, ConfigDict

# post 메소드 호출시 매핑되는 모델
class Book(BaseModel):
    id: int
    title: str
    price: int
    isbn: int

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "title": "FastAPI",
                    "price": 20000,
                    "isbn": 1234
                }
            ]
        }
    )