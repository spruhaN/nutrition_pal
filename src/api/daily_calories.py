from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/daily_calories",
    tags=["daily_calories"],
    dependencies=[Depends(auth.get_api_key)],
)



@router.get('/{customer_id}')
async def getDailyCalories(customer_id: int):
    with db.engine.begin() as connection:
        sql = "SELECT daily_calories FROM goals WHERE customer_id = :customer_id"
        daily_calories = connection.execute(sqlalchemy.text(sql), 
                                            [{"customer_id": customer_id}]).fetchone()[0]
        
        sql = "SELECT COALESCE(SUM(calories), 0) FROM meal WHERE customer_id = :customer_id\
            AND DATE(time) = DATE('now')"
        calories = connection.execute(sqlalchemy.text(sql), 
                                            [{"customer_id": customer_id}]).fetchone()[0]
        
        calories_left = daily_calories - calories
    return {"calories_left" : calories_left}
