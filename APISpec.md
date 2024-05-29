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

### 1.1. POST meal - `/meal/` (POST)

POSTS a meal to the db, with primary ingredient and calories

**Request**:

```json
    {
        "type": "string", /*Mexican, Asian, Indian, whatever type*/
        "calories": "integer",
    }
```

**Response**

```json
{
    "success": "boolean"
}
```

### 1.2. Goals - `/goal/` (POST)

Writes a goal to the db so the person can see what they committed to

**Request**:

```json
[
  {
    "goal": "string",
    "type": "string", /* either diet or workout*/
    "daily_calories" : "integer"
  }
]
```
**Response**:

```json
{
    "success": "boolean"
}
```


### 1.3. Daily Calories Needed - `/daily_calories/{customer_id}/` (GET)

Get's how many calories you need to meet your daily goal

**Request**:

```json
{
  "customer_id": "integer"
}
```

**Response**:

```json
{
  "calories_left": "integer"
}
```

### 1.4. Average Daily Calories - `/daily_calories/{customer_id}/average` (GET)

Gets how many average calories a user has consumed over the last x days along with their biggest meal

**Request**:

```json
{
  "customer_id": "integer",
  "over_days": "integer"
}
```

**Response**:

```json
{
  "biggest_meal": "string",
  "average_calories": "integer"
}
```



### 1.5. Post Workout - `/workout/` (POST)

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

```json
{
    "success": "boolean"
}
```

### 1.6. Get meals eaten - `/meal/day` (GET)

Get all meals eaten

**Response**:

```json
[
    {
        "id": "integer",
        "type": "string", 
        "calories": "integer",
        "date": "timeday"
    }
]
```

### 1.7. Get all workouts - `/workout/day` (GET)

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

### 1.8. See what muscle group a workout hits - `/workout/{id}/muscle_groups` (GET)
Sees what muscle group a workout hits, supplies the id

**Response**:

```json
    {
      "type": "string",
      "group": "string
    }
```

### 1.9. Search workouts by muscle groups - `/workout/muscle_groups/{type}` (GET)
See workout for a specific muscle group, this is from a db of generic wrokouts separate from personal workouts

**Response**:

```json
[
    {
      "name" : "string"
    }
]
```


### 1.10. See workout you've done for that type - `/workout/personal/muscle_groups/{type}` (GET)
Returns a list of workouts you have done that correpsond to the type you set
**Response**:

```json
[
    {
        "name": "string", /* May have restricted workout where the only options are like pushup, pull-up, cardio atm*/
        "sets": "integer",
        "reps": "integer",
        "length": "integer", /* minutes */
        "date" : "timeday"
    }
]
```

### 1.11. See workout you've done for that type - `/meal/{customer_id}/recommend` (GET)
Returns at most 3 meals for a customer given their caloric needs for the day
**Response**:

```json
[
    {
        "meal_name": "string", 
        "calories": "integer",
    }
]
```

### 1.12. See workout you've done for that type - `/workout/recommend/{customer_id}/{type}` (GET)
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
