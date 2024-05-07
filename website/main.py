from fastapi import FastAPI
app = FastAPI()
from pydantic import BaseModel
import database as db
import sqlalchemy


# uvicorn main:app --reload

@app.get('/')
async def root():
    return {"hello" : "team"}

class User(BaseModel):
    name: str
    weight: int
    height: int


@app.post("/user")
async def postUser(user: User):
    with db.engine.begin() as connection:
        sql = "INSERT INTO customer (name, weight, height)\
            VALUES (:name, :weight, :height) RETURNING customer_id"
        
        result = connection.execute(sqlalchemy.text(sql), 
                                    [{"name": user.name, "weight": user.weight,
                                      "height": user.height}]).fetchone()
    return {"id": result.customer_id}

class Goal(BaseModel):
    goal: str
    type: str
    daily_calories: int

@app.post("/goals/{customer_id}")
async def postGoals(goal: Goal, customer_id: int):
    with db.engine.begin() as connection:
        sql = "INSERT INTO goals (type, goal, customer_id, daily_calories)\
            VALUES (:type, :goal, :customer_id, :daily_calories)"
        
        result = connection.execute(sqlalchemy.text(sql), 
                                    [{"type": goal.type, "goal": goal.goal, 
                                      "customer_id": customer_id, "daily_calories" : goal.daily_calories}])
    return "OK"


class Meal(BaseModel):
    name: str
    calories: int

@app.post("/meal/{customer_id}")
async def postMeal(meal: Meal, customer_id: int):
    with db.engine.begin() as connection:
        sql = "INSERT INTO meal (name, calories, customer_id, ingredient_id)\
            VALUES (:name, :calories, :customer_id, :ingredient_id)"
        
        result = connection.execute(sqlalchemy.text(sql), 
                                    [{"name": meal.name, "calories": meal.calories, 
                                      "customer_id": customer_id, "ingredient_id": 1}])
    return "OK"


@app.get('/daily_calories/{customer_id}')
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

@app.get("/meal/{customer_id}/day")
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