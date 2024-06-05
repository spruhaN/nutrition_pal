from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[Depends(auth.get_api_key)],
)


class User(BaseModel):
    name: str
    weight: int #pounds
    height: int #inches

# add user to user db and return user id
@router.post("/")
async def postUser(user: User):
    if user.weight < 60 or user.height < 40:
        raise HTTPException(status_code=422, detail="Cannot input invalid weight or height")

    with db.engine.begin() as connection:
        sql = """
        INSERT INTO users (name, weight, height)
        VALUES (:name, :weight, :height) RETURNING user_id
        """
        result = connection.execute(sqlalchemy.text(sql), user.dict()).scalar_one()
    return {"id": result}

# update user info in db
@router.put("/{user_id}")
async def updateUser(user_id: int, user: User):
    with db.engine.begin() as connection:
        exists = connection.execute(
            sqlalchemy.text("SELECT EXISTS(SELECT 1 FROM customer WHERE customer_id = :id)"),
            {"id": user_id}
        ).scalar_one()
        if not exists:
            raise HTTPException(status_code=404, detail="User not found")

        sql = """
        UPDATE customer SET name=:name, weight=:weight, height=:height
        WHERE customer_id=:id
        """
        connection.execute(sqlalchemy.text(sql), {**user.dict(), "id": user_id})

    return {"status": "User updated successfully"}
