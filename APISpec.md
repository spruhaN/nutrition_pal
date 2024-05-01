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


### 1.3. Daily Calories Needed - `/daily_calories/` (GET)

Get's how many calories you need to meet your daily goal

**Respone**:

```json
{
  "calories_left": "integer"
}
```



### 1.4. Post Workout - `/workout/` (POST)

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

### 1.5. Get meals eaten - `/meal/day` (GET)

Get all meals eaten

**Response**:

```json
[
    {
        "id": "integer",
        "type": "string", 
        "calories": "integer",
        "date": "timeday
    }
]
```

### 1.6. Get all workouts - `/workout/day` (GET)

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

### 1.7. See what muscle group a workout hits - `/workout/{id}/muscle_groups` (GET)
Sees what muscle group a workout hits, supplies the id

**Response**:

```json
    {
      "type": "string",
      "group": "string
    }
```

### 1.8. Search workout muscle groups - `/workout/muscle_groups/{type}` (GET)
See workout for a specific muscle group

**Response**:

```json
[
    {
      "name" : "string"
    }
]
```


### 1.9. Search workout muscle groups for workouts youve done - `/workout/{id}/muscle_groups/{type}` (GET)
See workout for a specific muscle group that you have done before

**Response**:

```json
[
    {
      "name" : "string"
    }
]
```