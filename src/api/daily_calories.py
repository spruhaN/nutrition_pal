from fastapi import APIRouter, Depends, HTTPException
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
                                            [{"customer_id": customer_id}]).fetchone()
        if not daily_calories:
            raise HTTPException(status_code=404, detail="User does not have daily_calories")
        
        sql = "SELECT COALESCE(SUM(calories), 0) FROM meal WHERE customer_id = :customer_id\
            AND DATE(time) = DATE('now')"
        calories = connection.execute(sqlalchemy.text(sql), 
                                            [{"customer_id": customer_id}]).fetchone()[0]
        
        calories_left = daily_calories[0] - calories
    return {"calories_left" : calories_left}


# Customer gets an average calorie intake over the last x days as well as their most caloric meal
@router.get("{customer_id}/average")
async def getAverageMeals(customer_id: int, over_days: int):
    with db.engine.begin() as connection:
        sql = """
                SELECT name, calories
                FROM meal
                WHERE customer_id = :customer_id AND DATEDIFF(DATE('now'),DATE(time))<:range
                ORDER BY calories
            """
        calories = connection.execute(sqlalchemy.text(sql), [{"customer_id":customer_id, "range":over_days}]).fetchall()

        calorie_total = 0
        biggest_meal = ""
        i = 0
        for cal in calories:
            if i == 0:
                biggest_meal = cal[0]
            calorie_total+=cal[1]
            i+=1
        calorie_avg = calorie_total/over_days
        return {
            "biggest meal": biggest_meal,
            "average calories": calorie_avg
        }