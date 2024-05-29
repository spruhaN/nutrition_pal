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

# Customer uploades meal onto db
@router.post("/{customer_id}")
async def postMeal(meal: Meal, customer_id: int):

    if meal.calories < 1:
        raise HTTPException(status_code=422, detail="Cannot input 0 or negative calories")
    
    with db.engine.begin() as connection:
        sql = "INSERT INTO meal (name, calories, customer_id, ingredient_id, rating)\
            VALUES (:name, :calories, :customer_id, :ingredient_id, :rating)"
        
        result = connection.execute(sqlalchemy.text(sql), 
                                    [{"name": meal.name, "calories": meal.calories, 
                                      "customer_id": customer_id, "ingredient_id": 1,
                                      "rating" : meal.rating}])
    return "OK"


@router.put('/{customer_id}/{meal_id}')
async def updateMeal(meal: Meal, customer_id: int, meal_id: int):

    if meal.calories < 1:
        raise HTTPException(status_code=422, detail="Cannot input 0 or negative calories")
    
    with db.engine.begin() as connection:
            sql = "UPDATE meal SET calories = :calories, meal = :meal, rating = :rating\
                WHERE customer_id = :customer_id AND meal_id = :meal_id"
            
            update = connection.execute(sqlalchemy.text(sql), 
                                        [{"name" : meal.name, "calories" : meal.calories,
                                          "customer_id" : customer_id, "meal_id" : meal_id}])
    return {"status" : "OK", "message": "Meal updated successfully"}



# Customer gets all meals eaten
@router.get("/meal/{customer_id}/day")
async def getAllMeals(customer_id: int):
    with db.engine.begin() as connection:
        sql = "SELECT name, calories, time, type, meal_id FROM meal WHERE customer_id = :customer_id"
        meals = connection.execute(sqlalchemy.text(sql), [{"customer_id": customer_id}]).fetchall()

        meal_list = []
        for meal in meals:
            meal_list.append(
                {"name": meal.name,
                 "calories": meal.calories,
                 "time": meal.time,
                 "type": meal.type,
                 "meal_id" : meal.meal_id
                 }
            )
    return meal_list

# Gets at most 3 meals recommended to the customer based on their previous preferences and their caloric needs
@router.get("/{customer_id}/recommend")
async def getRecommendedMeal(customer_id: int):
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
        newsql = "SELECT name, calories, (CASE WHEN (customer_id = :customer_id) THEN rating*2 ELSE rating END) as rated\
                    FROM meal\
                    WHERE calories<:calories_left AND ((time <= CURRENT_DATE - 2 AND customer_id = :customer_id) OR customer_id != :customer_id)\
                    ORDER BY rated DESC\
                    LIMIT 3"
        meals = connection.execute(sqlalchemy.text(newsql),
                                        [{"customer_id": customer_id, "calories_left": calories_left}]).fetchall()
        if not meals:
            raise HTTPException(status_code=404, detail="No prior meals in the database to recommend from")
        
        mealrecs = []
        for meal in meals:
            mealrecs.append({
                "meal_name" : meal.name,
                "calories" : meal.calories,
            })
    return mealrecs