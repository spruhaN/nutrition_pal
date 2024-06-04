from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/goal",
    tags=["goal"],
    dependencies=[Depends(auth.get_api_key)],
)


class Goal(BaseModel):
    goal: str
    type: str
    daily_calories: int

# set goals to goal db with attached user id
@router.post("/{user_id}")
async def postGoals(goal: Goal, user_id: int):
    with db.engine.begin() as connection:
        sql = "SELECT name FROM users WHERE user_id = :user_id"
        res = connection.execute(sqlalchemy.text(sql), [{"user_id" : user_id}]).fetchone()
        if not res:
            raise HTTPException(status_code=422, detail="User does not exist, create an account with /user/")
    
        if goal.daily_calories < 1:
            raise HTTPException(status_code=422, detail="Cannot input calorie goal of less than 1")
        
        try:
            with db.engine.begin() as connection:
                sql = """
                INSERT INTO goals (type, goal, user_id, daily_calories)
                VALUES (:type, :goal, :user_id, :daily_calories)
                """
                connection.execute(sqlalchemy.text(sql), goal.dict() | {"user_id": user_id})
            return "OK"
        
        except:
            print("User already has goal, edit it with PUT request")
            return "Cannot have multiple goals"
    

# Updates goal information
@router.put("/{user_id}")
async def updateGoal(goal: Goal, user_id: int):
    with db.engine.begin() as connection:
        sql = "SELECT name FROM users WHERE user_id = :user_id"
        res = connection.execute(sqlalchemy.text(sql), [{"user_id" : user_id}]).fetchone()
        if not res:
            raise HTTPException(status_code=422, detail="User does not exist, create an account with /user/")
    
        if goal.daily_calories < 1:
            raise HTTPException(status_code=422, detail="Cannot input calorie goal of less than 1")
        
        sql = """
        UPDATE goals SET type = :type, goal = :goal, daily_calories = :daily_calories
        WHERE user_id = :user_id
        """
        connection.execute(sqlalchemy.text(sql), goal.dict() | {"user_id": user_id})
    return {"status": "OK", "message" : "Successful update"}