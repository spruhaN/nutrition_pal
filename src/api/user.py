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
        sql = "SELECT name FROM users WHERE user_id = :user_id"
        res = connection.execute(sqlalchemy.text(sql), [{"user_id" : user_id}]).fetchone()
        if not res:
            raise HTTPException(status_code=422, detail="User does not exist, create an account with /user/")
    
        if user.weight < 60 or user.height < 40:
            raise HTTPException(status_code=422, detail="Cannot input invalid weight or height")

        sql = """
        update users
            set
            name = :name,
            weight = :weight,
            height = :height
            where
            users.user_id = :user_id;
        """
        result = connection.execute(sqlalchemy.text(sql), user.dict()|{"user_id":user_id}).scalar_one()

    return {"status": "User updated successfully"}
