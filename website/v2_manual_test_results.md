# Example workflow
# Flow 2. Adding and looking up workout
Marc wants to build muscle<br />
Marc enters his goals by calling POST /goals passing “get big”, “workout”, 2800.<br />
He then begins adding workouts with with POST /workout passing “deadlift”, 3, 10, 0.<br />
He does this with multiple workouts at varying lengths, set, reps.<br />
His friends asks him what workouts he’s done, so he GET /workouts/days and returns a list of workout with “id”, “name”, “sets”, “reps”, “length”, "type", "group"<br />
His friend asks what to do for back, GET /workout/muscle_group/{type} passing “back” as type and returns a list of workouts "name", "type", and "group" for the back<br />

# Testing results
<Repeated for each step of the workflow>


### Marco enters in his information
1. 
    curl -X 'POST' \
    'https://nutrition-pal.onrender.com/user' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "name": "Marc",
    "weight": 150,
    "height": 189
    }'
2. 
    {
    "id" : 11
    }
or some integer(can vary due to testing) BUT USE THIS VALUE FOR LATER CUSTOMER ID PARAMS


### Marco enters his goals
1. 
    curl -X 'POST' \
    'https://nutrition-pal.onrender.com/goals/11' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "goal": "get big",
    "type": "workout",
    "daily_calories": 2800
    }'
2. 
    "OK"


### Marco enters a few workouts
1. 
    curl -X 'POST' \
    'https://nutrition-pal.onrender.com/workout/11' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "name": "deadlift",
    "sets": 3,
    "reps": 10,
    "length": 0
    }'
2. 
    "OK"

1.
    curl -X 'POST' \
    'https://nutrition-pal.onrender.com/workout/11' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "name": "pull_up",
    "sets": 5,
    "reps": 5,
    "length": 0
    }'
2. 
    "OK"

1.
    curl -X 'POST' \
    'https://nutrition-pal.onrender.com/workout/11' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "name": "leg_press",
    "sets": 1,
    "reps": 9,
    "length": 0
    }'
2. 
    "OK"


### Marco wants to check how many workouts he's done that day
1. 
    curl -X 'GET' \
    'https://nutrition-pal.onrender.com/workouts/11/day' \
    -H 'accept: application/json'
2. 
    [
    {
        "id": 15,
        "name": "deadlift",
        "type": "legs",
        "group": "glutes",
        "sets": 3,
        "reps": 10,
        "length": 0
    },
    {
        "id": 9,
        "name": "pull_up",
        "type": "back",
        "group": "lats",
        "sets": 5,
        "reps": 5,
        "length": 0
    },
    {
        "id": 22,
        "name": "leg_press",
        "type": "legs",
        "group": "quads",
        "sets": 1,
        "reps": 9,
        "length": 0
    }
    ]


### Marco wants to see what workouts he can do for back
1. 
    curl -X 'GET' \
    'https://nutrition-pal.onrender.com/workouts/muscle_groups/back' \
    -H 'accept: application/json'
2. 
    [
    {
        "name": "lat_pulldown",
        "type": "back",
        "group": "lats"
    },
    {
        "name": "cable_row",
        "type": "back",
        "group": "traps"
    },
    {
        "name": "pull_up",
        "type": "back",
        "group": "lats"
    },
    {
        "name": "bent_over_dumbell_row",
        "type": "back",
        "group": "lats"
    }
    ]

# Flow 3. Finding workout muscle_groups
Andrew M. is jealous of his roommate’s incredible physique. <br />
Andrew starts with a POST /goals passing “get huge, “workout”, 2800.<br />
He posts a workout POST /workout “squat”, 20, 20, 0.<br />
He wants to see what his workouts hit so he starts with GET /workout/day and gets a list of “id”, “name”, “sets”, “reps”, “length”, "type", and "group"<br />
He wants to see what his squat hits so he does a GET /workout/{id}/muscle_groups passing an id in that was in the prior return.<br />
This returns what muscles he's targeting<br />


### Andrew creates a user account
1.
    curl -X 'POST' \
    'https://nutrition-pal.onrender.com/user' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "name": "Andrew M.",
    "weight": 90,
    "height": 189
    }'
2.
    {
    "id": 12
    }


### Andrew inputs his goal
1.
    curl -X 'POST' \
    'https://nutrition-pal.onrender.com/goals/12' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "goal": "get huge",
    "type": "workout",
    "daily_calories": 5000
    }'
2.
    "OK"


### Andrew puts in his workout
1.
    curl -X 'POST' \
    'https://nutrition-pal.onrender.com/workout/12' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "name": "squat",
    "sets": 20,
    "reps": 20,
    "length": 0
    }'
2.
    "OK"


### Andrew forgot what he did and wants to check
1.
    curl -X 'GET' \
    'https://nutrition-pal.onrender.com/workouts/12/day' \
    -H 'accept: application/json'
2.
    [
    {
        "id": 20,
        "name": "squat",
        "type": "legs",
        "group": "quads",
        "sets": 20,
        "reps": 20,
        "length": 0
    }
    ]


### Andrew is extremely forgetful and wants to see what squat hits
1.
    curl -X 'GET' \
    'https://nutrition-pal.onrender.com/workout/20/muscle_groups' \
    -H 'accept: application/json'
2.
    [
    {
        "name": "squat",
        "type": "legs",
        "group": "quads"
    }
    ]