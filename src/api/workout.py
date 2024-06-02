from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy

router = APIRouter(
    prefix="/workout",
    tags=["workout"],
    dependencies=[Depends(auth.get_api_key)],
)


class Workout(BaseModel):
    name: str
    sets: int
    reps: int
    length: int  # Duration of the workout in minutes

# finds workout under excercises(exercise_id, name, muscle_group_id) and attaches id and info to user workout with reps
@router.post("/{user_id}")
async def postWorkout(workout: Workout, user_id: int):
    
    if (workout.sets < 1) or (workout.reps < 1) or (workout.length < 1):
            raise HTTPException(status_code=422, detail="Cannot input sets, reps, or length values <0")
    
    with db.engine.begin() as connection:
        find_qry = """
                    SELECT id as id
                    FROM exercises
                    WHERE name = :w_name;
                    """
        res = connection.execute(sqlalchemy.text(find_qry), {"w_name": workout.name}).first()

        print(res.id)
        
        insert_sql = """
                    INSERT INTO user_workouts (exercise_id, sets, reps, length, user_id)
                    VALUES (:e_id, :sets, :reps, :length, :user_id)
                    """
        connection.execute(sqlalchemy.text(insert_sql),workout.dict() | {"e_id": res.id, "user_id": user_id})
    return "OK"

@router.get("/{user_id}/day")
async def getWorkoutsByDay(user_id: int):
    with db.engine.begin() as connection:
        sql = """
                SELECT
                    e.id,
                    e.name,
                    mg.type,
                    mg.group,
                    cw.sets,
                    cw.reps,
                    cw.length
                FROM user_workouts AS cw
                JOIN exercises AS e ON cw.exercise_id = e.id
                JOIN muscle_groups AS mg ON e.muscle_group_id = mg.muscle_group_id
                WHERE cw.user_id = :cid and DATE(time) = DATE('now')
                """
        result = connection.execute(sqlalchemy.text(sql), {"cid": user_id}).mappings().all()

    return result

# returns a list of workouts that target the given type
@router.get("/muscle_groups/{type}")
async def getMuscleGroups(type: str):
    with db.engine.begin() as connection:
        sql = """
                SELECT
                    e.name,
                    mg.type,
                    mg.group
                FROM exercises AS e
                JOIN muscle_groups AS mg ON mg.muscle_group_id = e.muscle_group_id
                WHERE mg.type = :m_type
                """
        result = connection.execute(sqlalchemy.text(sql), {"m_type": type}).mappings().all()
    return result


# returns a description of the given workout provided
@router.get("/{workout_id}/muscle_groups")
async def getWorkoutMuscleGroups(workout_id: int):
    with db.engine.begin() as connection:
        sql = """
                SELECT
                e.name,
                mg.type,
                mg.group
                FROM exercises AS e
                JOIN muscle_groups AS mg ON mg.muscle_group_id = e.muscle_group_id
                WHERE e.id = :w_id
                """
        muscle_groups = connection.execute(sqlalchemy.text(sql), {"w_id": workout_id}).mappings().all()
    return muscle_groups


# Recommends a workout for the user and the given type
@router.get("/recommend/{user_id}/{type}")
async def recWorkout(user_id: int, type: str):
    with db.engine.begin() as connection:
        sql = "WITH recent AS (\
                    SELECT\
                        exercise_id\
                    FROM user_workouts\
                    WHERE \
                        user_id = :user_id AND\
                        time >= CURRENT_DATE - 3\)\
                SELECT\
                    e.name AS name,\
                    ROUND(AVG(c.sets)) AS sets,\
                    ROUND(AVG(c.reps)) AS reps\
                FROM exercises AS e\
                JOIN\
                    user_workouts AS c ON c.exercise_id = e.id\
                JOIN \
                    muscle_groups AS m ON m.muscle_group_id = e.muscle_group_id\
                WHERE\
                    m.type = :type AND\
                    c.exercise_id NOT IN (SELECT exercise_id FROM recent)\
                GROUP BY e.name"
        
        workout_list = connection.execute(sqlalchemy.text(sql), 
                                      [{"user_id" : user_id,
                                        "type" : type}]).fetchall()
        if len(workout_list) == 0:
            return {"message": "No workout available for given type"}

        workouts = []
        for workout in workout_list:
            workouts.append({
                "name" : workout.name,
                "sets" : workout.sets,
                "reps" : workout.reps
            })

    return workouts


 