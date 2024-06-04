# API Specification for Nutrient Tracker

`/meal/`
`/goal/`
`/daily_calories/`
`/workout/`
`/meal/day`
`/workout/day`
`/workout/{id}/muscle_group`
`/workout/muscle_groups/{type}`
`/workout/{id}/muscle_groups/{type}`

#### USER
### 1.1. POST user - `/user/` (POST)

POSTS a user to the DB
**Request**:

```json
    {
        "name": "string", /*Mexican, Asian, Indian, whatever type*/
        "weight": "integer", /* pounds */
        "height" : "integer" /* inches
    }
```

**Response**

```json
{
    "id": "integer"
}
```


#### MEALS
### 2.1. POST meal - `/meal/{user_id}` (POST)

POSTS a meal to the db, with primary ingredient and calories

**Request**:

```json
    {
        "type": "string", /*Mexican, Asian, Indian, whatever type*/
        "calories": "integer",
        "rating" : "integer",
        "name" : "string"
    }
```

**Response**

"OK"


### 2.2. PUT meal - `/meal/{user_id}/{meal_id}` (PUT)

POSTS a meal to the db, with primary ingredient and calories

**Request**:

```json
    {
        "type": "string", /*Mexican, Asian, Indian, whatever type*/
        "calories": "integer",
        "rating" : "integer",
        "name" : "string"
    }
```

**Response**
``` json
  {
      "status" : "OK", 
      "message": "Meal updated successfully"
  }
```

### 2.3. See workout you've done for that type - `/meal/{customer_id}/recommend` (GET)
Returns at most 3 meals for a customer given their caloric needs for the day

**Response**:

```json
[
    {
        "meal_name": "string", 
        "calories": "integer",
        "type" : "string"
    }
]
```

### 2.4. Get meals eaten - `/meal/{user_id}/day` (GET)

Get all meals eaten

**Response**:

```json
[
    {
        "id": "integer",
        "type": "string", 
        "calories": "integer",
        "date": "timeday",
        "rating" : "integer"
    }
]
```

#### GOALS
### 3.1. Goals - `/goal/{user_id}` (POST)

Writes a goal to the db so the person can see what they committed to

**Request**:

```json
  {
    "goal": "string",
    "type": "string", 
    "daily_calories" : "integer"
  }
```
**Response**:

"OK"

### 3.2. Goals - `/goal/{user_id}` (PUT)

Writes a goal to the db so the person can see what they committed to

**Request**:

```json
  {
    "goal": "string",
    "type": "string", 
    "daily_calories" : "integer"
  }
```
**Response**:

```json
{
  "status": "OK",
   "message" : "Successful update"
}
```


#### DAILY CALORIES
### 4.1. Daily Calories Needed - `/daily_calories/{user_id}/` (GET)

Get's how many calories you need to meet your daily goal

**Response**:

```json
{
  "calories_left": "integer"
}
```

### 4.2. Average Daily Calories - `/daily_calories/{user_id}/average` (GET)

Gets how many average calories a user has consumed over the last x days along with their biggest meal

**Request**:

```json
{
  "user_id": "integer",
  "over_days": "integer"
}
```



#### WORKOUT
### 5.1. Post Workout - `/workout/{user_id}` (POST)

Posts a workout to the db, ID of muscle groups can be assigned by the db

**Request**:

```json
{
  "name": "string", /* May have restricted workout where the only options are like pushup, pull-up, cardio atm*/
  "sets": "integer",
  "reps": "integer",
  "length": "integer" /* minutes */
}
```

**Response**:

"OK"



### 5.2. Get all workouts - `/workout/{user_id}/day` (GET)

Get all meals eaten

**Response**:

```json
[
    {
      "id": "integer",
      "name": "string", /* May have restricted workout where the only options are like pushup, pull-up, cardio atm*/
      "sets": "integer",
      "reps": "integer",
      "length": "interger",
      "date": "timeday"
    }
]
```

### 5.3. See what muscle group a workout hits - `/workout/{workout_id}/muscle_groups` (GET)
Gets workouts for very specific aspect of body (triceps, biceps...)

**Response**:

```json
[
    {
      "name" : "string",
      "type" : "string",
      "group" : "string"
    }
]
```

### 5.4. Search workouts by general body parts (chest, back...) - `/workout/muscle_groups/{type}` (GET)
See workout for a specific muscle group, this is from a db of generic wrokouts separate from personal workouts

**Response**:

```json
[
    {
      "name" : "string",
      "type" : "string",
      "group" : "string"
    }
]
```


### 5.5. See workout you've done for that type - `/workout/recommend/{user_id}/{type}` (GET)
Returns a list of workouts for a given type you haven't done in the past three days
**Response**:

```json
[
    {
        "name": "string", 
        "sets": "integer",
        "reps": "integer"
    }
]
```


### 5.5. See workout you've done for that type - `/workout/all_workouts` (GET)
Returns a list of workouts for a given type you haven't done in the past three days
**Response**:

```json
[
    {
        "name": "string", 
        "type": "integer",
        "group": "integer"
    }
]
```