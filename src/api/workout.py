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
    with db.engine.begin() as connection:
        sql = "SELECT name FROM users WHERE user_id = :user_id"
        res = connection.execute(sqlalchemy.text(sql), [{"user_id" : user_id}]).fetchone()
        if not res:
            raise HTTPException(status_code=422, detail="User does not exist, create an account with /user/")
    
    
        if (workout.sets < 1) or (workout.reps < 1) or (workout.length < 1):
                raise HTTPException(status_code=422, detail="Cannot input sets, reps, or length values < 1")
    
        find_qry = """
                    SELECT id as id
                    FROM exercises
                    WHERE name = :w_name;
                    """
        res = connection.execute(sqlalchemy.text(find_qry), {"w_name": workout.name}).first()

        if res is None:
            workout_sql = """ SELECT name FROM exercises """
            workouts = connection.execute(sqlalchemy.text(workout_sql)).mappings().all()
            print(workouts)
            return [{"Acceptable inputs" : str(workouts)}]

        insert_sql = """
                    INSERT INTO user_workouts (exercise_id, sets, reps, length, user_id)
                    VALUES (:e_id, :sets, :reps, :length, :user_id) RETURNING exercise_id
                    """
        res = connection.execute(sqlalchemy.text(insert_sql), workout.dict() | {"e_id": res.id, "user_id": user_id}).first()
        return {"id": res.exercise_id}


@router.get("/{user_id}/day")
async def getWorkoutsByDay(user_id: int):

    with db.engine.begin() as connection:
        sql = "SELECT name FROM users WHERE user_id = :user_id"
        res = connection.execute(sqlalchemy.text(sql), [{"user_id" : user_id}]).fetchone()
        if not res:
            raise HTTPException(status_code=422, detail="User does not exist, create an account with /user/")
    
        sql = """
                SELECT
                    e.id,
                    e.name,
                    mg.type,
                    mg.group_name,
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
                    mg.group_name
                FROM exercises AS e
                JOIN muscle_groups AS mg ON mg.muscle_group_id = e.muscle_group_id
                WHERE mg.type = :m_type
                """
        result = connection.execute(sqlalchemy.text(sql), {"m_type": type}).mappings().all()

        if result is None or len(result) == 0:
            sql = """ SELECT DISTINCT type FROM muscle_groups """
            types = connection.execute(sqlalchemy.text(sql)).mappings.all()
            print(types)
            return [{"Acceptable inputs" : str(types)}]

    return result


# returns a description of the given workout provided
@router.get("/{workout_id}/muscle_groups")
async def getWorkoutMuscleGroups(workout_id: int):
    with db.engine.begin() as connection:
        sql = """
                SELECT
                e.name,
                mg.type,
                mg.group_name
                FROM exercises AS e
                JOIN muscle_groups AS mg ON mg.muscle_group_id = e.muscle_group_id
                WHERE e.id = :w_id
                """
        muscle_groups = connection.execute(sqlalchemy.text(sql), {"w_id": workout_id}).mappings().all()

        if muscle_groups is None or len(muscle_groups) == 0:
            sql = """ SELECT muscle_group_id, group_name FROM muscle_groups"""
            pairings = connection.execute(sqlalchemy.text(sql)).mappings().all()
            print(pairings)
            return [{"Acceptable inputs" : str(pairings)}]

    return muscle_groups


# Recommends a workout for the user and the given type
@router.get("/recommend/{user_id}/{type}")
async def recWorkout(user_id: int, type: str):
    with db.engine.begin() as connection:
        sql = "SELECT name FROM users WHERE user_id = :user_id"
        res = connection.execute(sqlalchemy.text(sql), [{"user_id" : user_id}]).fetchone()
        if not res:
            raise HTTPException(status_code=404, detail="User does not exist, create an account with /user/")
    
        sql = """WITH recent AS (
                    SELECT
                        exercise_id
                    FROM user_workouts
                    WHERE 
                        user_id = :user_id AND
                        time >= CURRENT_DATE - 3)
                SELECT
                    e.name AS name,
                    ROUND(AVG(c.sets)) AS sets,
                    ROUND(AVG(c.reps)) AS reps
                FROM exercises AS e
                JOIN
                    user_workouts AS c ON c.exercise_id = e.id
                JOIN 
                    muscle_groups AS m ON m.muscle_group_id = e.muscle_group_id
                WHERE
                    m.type = :type AND
                    c.exercise_id NOT IN (SELECT exercise_id FROM recent)
                GROUP BY e.name"""
        
        workout_list = connection.execute(sqlalchemy.text(sql), 
                                      [{"user_id" : user_id,
                                        "type" : type}]).fetchall()
        if len(workout_list) == 0:
            return {"message": "No workout available for given type, make sure type is [legs, front, back, or arms]"}

        workouts = []
        for workout in workout_list:
            workouts.append({
                "name" : workout.name,
                "sets" : workout.sets,
                "reps" : workout.reps
            })

    return workouts


@router.get("/all_workouts")
async def getAllWorkouts():
    with db.engine.begin() as connection:
        sql = """SELECT exercises.name, exercises.id, muscle_groups.group_name, muscle_groups.muscle_group_id
                FROM exercises
                JOIN muscle_groups ON exercises.muscle_group_id = muscle_groups.muscle_group_id;
                """
        
        workout_list = connection.execute(sqlalchemy.text(sql)).mappings().all()
        if len(workout_list) == 0:
            return {"message": "No workouts listed"}
    return workout_list
