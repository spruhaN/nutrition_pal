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



@router.get('/{user_id}')
async def getDailyCalories(user_id: int):
    with db.engine.begin() as connection:
        sql = "SELECT name FROM users WHERE user_id = :user_id"
        res = connection.execute(sqlalchemy.text(sql), [{"user_id" : user_id}]).fetchone()
        if not res:
            raise HTTPException(status_code=404, detail="User does not exist, create an account with /user/")
    
    with db.engine.begin() as connection:
        sql = "SELECT daily_calories FROM goals WHERE user_id = :user_id"
        daily_calories = connection.execute(sqlalchemy.text(sql), 
                                            [{"user_id": user_id}]).fetchone()
        if not daily_calories:
            raise HTTPException(status_code=404, detail="User does not have daily_calories")
        
        sql = """SELECT COALESCE(SUM(calories), 0) FROM meals WHERE user_id = :user_id
            AND EXTRACT(DAY FROM AGE(NOW(), time)) = 0"""
        calories = connection.execute(sqlalchemy.text(sql), 
                                            [{"user_id": user_id}]).fetchone()[0]
        if not calories:
            calories = 0
        calories_left = daily_calories[0] - calories
    return {"calories_left" : calories_left}


# user gets an average calorie intake over the last x days as well as their most caloric meal
@router.get("{user_id}/average")
async def getAverageMeals(user_id: int, over_days: int):
    with db.engine.begin() as connection:
        sql = "SELECT name FROM users WHERE user_id = :user_id"
        res = connection.execute(sqlalchemy.text(sql), [{"user_id" : user_id}]).fetchone()
        if not res:
            raise HTTPException(status_code=404, detail="User does not exist, create an account with /user/")
    
    with db.engine.begin() as connection:
        sql = """
                SELECT name, calories
                FROM meals
                WHERE user_id = :user_id AND EXTRACT(DAY FROM AGE(NOW(), time)) < :range
                ORDER BY calories DESC
            """
        meals = connection.execute(sqlalchemy.text(sql), [{"user_id":user_id, "range":over_days}]).fetchall()

        if not meals:
            raise HTTPException(status_code=404, detail="No meals found for the given period.")
        
        calorie_total = 0
        biggest_meal = meals[0][0]
        for meal in meals:
            calorie_total += meal[1]
        
        calorie_avg = calorie_total / len(meals) if meals else 0
        return {
            "biggest meal": biggest_meal,
            "average calories": calorie_avg
        }