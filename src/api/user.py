from fastapi import APIRouter, Depends
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
    weight: int
    height: int

# add user to user db and return user id
@router.post("/")
async def postUser(user: User):
    with db.engine.begin() as connection:
        sql = """
        INSERT INTO customer (name, weight, height)
        VALUES (:name, :weight, :height) RETURNING customer_id
        """
        result = connection.execute(sqlalchemy.text(sql), user.dict()).fetchone()
    return {"id": result.customer_id}