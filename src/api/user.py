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
    if user.weight < 1 or user.weight < 1:
        raise HTTPException(status_code=422, detail="Cannot input 0 weight or height")

    with db.engine.begin() as connection:
        sql = """
        INSERT INTO users (name, weight, height)
        VALUES (:name, :weight, :height) RETURNING user_id
        """
        result = connection.execute(sqlalchemy.text(sql), user.dict()).scalar_one()
    return {"id": result}