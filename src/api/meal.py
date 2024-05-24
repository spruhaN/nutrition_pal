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

# Customer uploades meal onto db
@router.post("/meal/{customer_id}")
async def postMeal(meal: Meal, customer_id: int):

    if meal.calories < 1:
        raise HTTPException(status_code=422, detail="Cannot input 0 or negative calories")
    
    with db.engine.begin() as connection:
        sql = "INSERT INTO meal (name, calories, customer_id, ingredient_id)\
            VALUES (:name, :calories, :customer_id, :ingredient_id)"
        
        result = connection.execute(sqlalchemy.text(sql), 
                                    [{"name": meal.name, "calories": meal.calories, 
                                      "customer_id": customer_id, "ingredient_id": 1}])
    return "OK"


# Customer gets all meals eaten
@router.get("/meal/{customer_id}/day")
async def getAllMeals(customer_id: int):
    with db.engine.begin() as connection:
        sql = "SELECT name, calories, time, type, ingredient_id FROM meal WHERE customer_id = :customer_id"
        meals = connection.execute(sqlalchemy.text(sql), [{"customer_id": customer_id}]).fetchall()

        meal_list = []
        for meal in meals:
            meal_list.append(
                {"name": meal.name,
                 "calories": meal.calories,
                 "time": meal.time,
                 "type": meal.type
                 }
            )
    return meal_list
