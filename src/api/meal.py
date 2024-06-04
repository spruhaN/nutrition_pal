from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/meal",
    tags=["meal"],
    dependencies=[Depends(auth.get_api_key)],
)



class Meal(BaseModel):
    name: str
    calories: int
    rating: int
    type: str

# user uploades meal onto db
@router.post("/{user_id}")
async def postMeal(meal: Meal, user_id: int):
    with db.engine.begin() as connection:
        sql = "SELECT name FROM users WHERE user_id = :user_id"
        res = connection.execute(sqlalchemy.text(sql), [{"user_id" : user_id}]).fetchone()
        if not res:
            raise HTTPException(status_code=422, detail="User does not exist, create an account with /user/")

    if meal.calories < 1:
        raise HTTPException(status_code=422, detail="Cannot input 0 or negative calories")
    
    if meal.rating > 10 or meal.rating <0:
        raise HTTPException(status_code=422, detail="Ratings must be in between 1 and 10")
    
    with db.engine.begin() as connection:
        sql = """INSERT INTO meals (name, calories, user_id, rating, type)
            VALUES (:name, :calories, :user_id, :rating, :type)"""
        
        connection.execute(sqlalchemy.text(sql), 
                                    [{"name": meal.name, "calories": meal.calories, 
                                      "user_id": user_id, "rating" : meal.rating, "type": meal.type}])
    return "OK"


@router.put('/{user_id}/{meal_id}')
async def updateMeal(meal: Meal, user_id: int, meal_id: int):
    with db.engine.begin() as connection:
        sql = "SELECT name FROM users WHERE user_id = :user_id"
        res = connection.execute(sqlalchemy.text(sql), [{"user_id" : user_id}]).fetchone()
        if not res:
            raise HTTPException(status_code=422, detail="User does not exist, create an account with /user/")
        
        sql = "SELECT type FROM meals WHERE meal_id = :meal_id"
        res = connection.execute(sqlalchemy.text(sql), [{"meal_id" : meal_id}]).fetchone()
        if not res:
            raise HTTPException(status_code=422, detail="Meal does not exist, create an meal with POST meal/{user_id}/{meal_id}")

    if meal.calories < 1:
        raise HTTPException(status_code=422, detail="Cannot input 0 or negative calories")
    
    if meal.rating > 10 or meal.rating <0:
        raise HTTPException(status_code=422, detail="Ratings must be in between 1 and 10")
    
    with db.engine.begin() as connection:
            sql = "UPDATE meals SET calories = :calories, name = :name, rating = :rating, type = :type\
                WHERE user_id = :user_id AND meal_id = :meal_id"
            
            connection.execute(sqlalchemy.text(sql), 
                                        [{"name" : meal.name, "calories" : meal.calories,
                                          "rating" : meal.rating, "type" : meal.type,
                                          "user_id" : user_id, "meal_id" : meal_id}])
    return {"status" : "OK", "message": "Meal updated successfully"}



# user gets all meals eaten
@router.get("/{user_id}/day")
async def getAllMeals(user_id: int):
    with db.engine.begin() as connection:
        sql = "SELECT name FROM users WHERE user_id = :user_id"
        res = connection.execute(sqlalchemy.text(sql), [{"user_id" : user_id}]).fetchone()
        if not res:
            raise HTTPException(status_code=422, detail="User does not exist, create an account with /user/")
    
    with db.engine.begin() as connection:
        sql = "SELECT name, calories, type, rating, time, meal_id FROM meals WHERE user_id = :user_id"
        meals = connection.execute(sqlalchemy.text(sql), [{"user_id": user_id}]).fetchall()

        meal_list = []
        for meal in meals:
            meal_list.append(
                {"name": meal.name,
                 "calories": meal.calories,
                 "type": meal.type,
                 "rating" : meal.rating,
                 "time": meal.time,
                 "meal_id" : meal.meal_id
                 }
            )
    return meal_list

# Gets at most 3 meals recommended to the user based on their previous preferences and their caloric needs
@router.get("/{user_id}/recommend")
async def getRecommendedMeal(user_id: int):
    with db.engine.begin() as connection:
        sql = "SELECT name FROM users WHERE user_id = :user_id"
        res = connection.execute(sqlalchemy.text(sql), [{"user_id" : user_id}]).fetchone()
        if not res:
            raise HTTPException(status_code=422, detail="User does not exist, create an account with /user/")
    
    with db.engine.begin() as connection:
        sql = "SELECT daily_calories FROM goals WHERE user_id = :user_id"
        daily_calories = connection.execute(sqlalchemy.text(sql), 
                                            [{"user_id": user_id}]).fetchone()
        if not daily_calories:
            raise HTTPException(status_code=422, detail="User does not have daily_calories, set a goal with /goals/")
        
        sql = """SELECT COALESCE(SUM(calories), 0) FROM meals WHERE user_id = :user_id
            AND EXTRACT(DAY FROM AGE(NOW(), time)) = 0"""
        calories = connection.execute(sqlalchemy.text(sql), 
                                            [{"user_id": user_id}]).fetchone()[0]
        if not calories:
            calories = 0;
        
        calories_left = daily_calories[0] - calories
        print(f"daily cal: {daily_calories[0]} {calories_left}")
        newsql = """SELECT name, calories, type, (CASE WHEN (user_id = :user_id) THEN rating*2 ELSE rating END) as rated
                    FROM meals
                    WHERE calories<:calories_left AND ((EXTRACT(DAY FROM AGE(NOW(), time)) > 2 AND user_id = :user_id) OR user_id != :user_id)
                    ORDER BY rated DESC
                    LIMIT 3"""
        meals = connection.execute(sqlalchemy.text(newsql),
                                        [{"user_id": user_id, "calories_left": calories_left}]).fetchall()
        if not meals or len(meals) == 0:
            raise HTTPException(status_code=422, detail="No prior meals in the database to recommend from")
        
        mealrecs = []
        for meal in meals:
            mealrecs.append({
                "meal_name" : meal.name,
                "calories" : meal.calories,
                "type" : meal.type
            })
    return mealrecs