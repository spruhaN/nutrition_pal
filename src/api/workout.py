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

# finds workout under excercises(exercise_id, name, muscle_group_id) and attaches id and info to customer workout with reps
@router.post("/{customer_id}")
async def postWorkout(workout: Workout, customer_id: int):
    
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
                    INSERT INTO customer_workouts (exercise_id, sets, reps, length, customer_id)
                    VALUES (:e_id, :sets, :reps, :length, :customer_id)
                    """
        result = connection.execute(sqlalchemy.text(insert_sql),workout.dict() | {"e_id": res.id, "customer_id": customer_id})
    return "OK"

@router.get("/{customer_id}/day")
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
@router.get("/muscle_groups/{type}")
async def getMuscleGroups(type: str):
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
@router.get("/{workout_id}/muscle_groups")
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
