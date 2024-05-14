from fastapi import FastAPI
from pydantic import BaseModel
import database as db
import sqlalchemy

app = FastAPI()

# uvicorn main:app --reload

# root
@app.get('/')
async def root():
    return {"hello": "team"}

class User(BaseModel):
    name: str
    weight: int
    height: int

# add user to user db and return user id
@app.post("/user")
async def postUser(user: User):
    with db.engine.begin() as connection:
        sql = """
        INSERT INTO customer (name, weight, height)
        VALUES (:name, :weight, :height) RETURNING customer_id
        """
        result = connection.execute(sqlalchemy.text(sql), user.dict()).fetchone()
    return {"id": result.customer_id}

class Goal(BaseModel):
    goal: str
    type: str
    daily_calories: int

# set goals to goal db with attached user id
@app.post("/goals/{customer_id}")
async def postGoals(goal: Goal, customer_id: int):
    with db.engine.begin() as connection:
        sql = """
        INSERT INTO goals (type, goal, customer_id, daily_calories)
        VALUES (:type, :goal, :customer_id, :daily_calories)
        """
        connection.execute(sqlalchemy.text(sql), goal.dict() | {"customer_id": customer_id})
    return "OK"

class Workout(BaseModel):
    name: str
    sets: int
    reps: int
    length: int  # Duration of the workout in minutes

# finds workout under excercises(exercise_id, name, muscle_group_id) and attaches id and info to customer workout with reps
@app.post("/workout/{customer_id}")
async def postWorkout(workout: Workout, customer_id: int):
    with db.engine.begin() as connection:
        find_qry = """
                    SELECT id as id
                    FROM exercises
                    WHERE name = :w_name;
                    """
        res = connection.execute(sqlalchemy.text(find_qry), {"w_name": workout.name}).first()

        print(res.id)
        
        insert_sql = """
                    INSERT INTO customer_workouts (exercise_id, sets, reps, length, customer_id)
                    VALUES (:e_id, :sets, :reps, :length, :customer_id)
                    """
        result = connection.execute(sqlalchemy.text(insert_sql),workout.dict() | {"e_id": res.id, "customer_id": customer_id})
    return "OK"

@app.get("/workouts/{customer_id}/day")
async def getWorkoutsByDay(customer_id: int):
    with db.engine.begin() as connection:
        sql = """
                select
                    e.id,
                    e.name,
                    mg.type,
                    mg.group,
                    cw.sets,
                    cw.reps,
                    cw.length
                from customer_workouts as cw
                join exercises as e on cw.exercise_id = e.id
                join muscle_groups as mg on e.muscle_group_id = mg.muscle_group_id
                where cw.customer_id = :cid and DATE(time) = DATE('now')
                """
        result = connection.execute(sqlalchemy.text(sql), {"cid": customer_id}).mappings().all()

    return result

# returns a list of workouts that target the given type
@app.get("/workouts/muscle_groups/{type}")
async def getWorkoutsByDay(type: str):
    with db.engine.begin() as connection:
        sql = """
                select
                    e.name,
                    mg.type,
                    mg.group
                from exercises as e
                join muscle_groups as mg on mg.muscle_group_id = e.muscle_group_id
                where mg.type = :m_type
                """
        result = connection.execute(sqlalchemy.text(sql), {"m_type": type}).mappings().all()
    return result

# returns a description of the given workout provided
@app.get("/workout/{workout_id}/muscle_groups")
async def getWorkoutMuscleGroups(workout_id: int):
    with db.engine.begin() as connection:
        sql = """
                select
                e.name,
                mg.type,
                mg.group
                from exercises as e
                join muscle_groups as mg on mg.muscle_group_id = e.muscle_group_id
                where e.id = :w_id
                """
        muscle_groups = connection.execute(sqlalchemy.text(sql), {"w_id": workout_id}).mappings().all()
    return muscle_groups

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
