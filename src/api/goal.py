from fastapi import APIRouter, Depends
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
@router.post("/{customer_id}")
async def postGoals(goal: Goal, customer_id: int):
    with db.engine.begin() as connection:
        sql = """
        INSERT INTO goals (type, goal, customer_id, daily_calories)
        VALUES (:type, :goal, :customer_id, :daily_calories)
        """
        connection.execute(sqlalchemy.text(sql), goal.dict() | {"customer_id": customer_id})
    return "OK"