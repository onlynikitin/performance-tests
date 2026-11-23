from fastapi import FastAPI, Query, Path, Body  # Body — для аннотации тела запроса
from pydantic import BaseModel                  # BaseModel — базовый класс для моделей

app = FastAPI(title="basics")


# Pydantic-модель для описания структуры пользователя
class User(BaseModel):
    username: str  # логин пользователя
    email: str     # email пользователя
    age: int       # возраст пользователя


# GET-эндпоинт с query- и path-параметрами
@app.get("/api/v1/basics/{item_id}")
async def get_basics(
    name: str = Query("Alise", description="Имя пользователя"),
    item_id: int = Path(..., description="Идентификатор элемента")
):
    return {
        "message": f"Hello, {name}!",
        "description": f"Item number {item_id}"
    }


# POST-эндпоинт для создания пользователя
@app.post("/api/v1/basics/users")
async def create_user(
    user: User = Body(..., description="Данные нового пользователя")
):
    # FastAPI автоматически:
    # 1) распарсит JSON из тела запроса
    # 2) провалидирует его по полям модели User
    return {
        "username": user.username,
        "email": user.email,
        "age": user.age,
        "message": "User created successfully!"
    }
