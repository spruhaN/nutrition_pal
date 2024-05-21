from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from src.api import meal, workout, goal, daily_calories, user
import json
import logging

description = """
Nutrition Pal allows you to track meals and workout, setting daily caloric goals
"""

app = FastAPI(
    title="Nutrition Pal",
    description=description
)

app.include_router(meal.router)
app.include_router(workout.router)
app.include_router(goal.router)
app.include_router(user.router)
app.include_router(daily_calories.router)

@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)

@app.get("/")
async def root():
    return {"message": "Welcome to NutritionPal."}
