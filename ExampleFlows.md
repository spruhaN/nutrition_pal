# Flow 1. Tracking daily calories and inputting workouts
Stephanie has some goals and wants to start tracking her calories and meals. 
First she POST /goals passing “lose weight”, “diet” and 2000
Next she eats food and does a POST /meal passing “Mexican” and 800.
She wants to see how many calories she has left GET /daily_calories returning 1200.
She then eats a pizza, POSTS /meal passing “Italian” 1200. 
Checks calories with GET /daily_calories, returns 0. 
Next day GET /meal/day returning a list of meals with an id, type, calorie, and time stamp


# Flow 2. Adding and looking up workout
Marc wants to build muscle
Marc enters his goals by calling POST /goals passing “get big”, “workout”, 2800.
He then begins adding workouts with with POST /workout passing “push-up”, 3, 10, 14.
He does this with multiple workouts at varying lengths, set, reps.
His friends asks him what workouts he’s done, so he GET /workouts/days and returns a list of workout with “id”, “name”, “sets”, “reps”, “length”, and “time”
His friend asks to do for back, GET /workout/muscle_group/{type} passing “back” as type and returns a list of workouts “id”, “name”, “sets”, “reps”, “length”, and “time”, for the back

# Flow 3. Finding workout muscle_groups
Andrew M. is jealous of his roommate’s incredible physique. 
Andrew starts with a POST /goals passing “get big”, “workout”, 2800.
He posts a workout POST /workout “pull-up”, 3, 4, 10.
He does this for a variety of workouts. 
He wants to see what his workouts hit so he starts with GET /workout/day and gets a list of “id”, “name”, “sets”, “reps”, “length”, and “time”
He wants to see what his chest-press hits so he does a GET /workout/{id}/muscle_groups passing an id in that was in the prior return.
This returns a list of strings [“chest”, “triceps”, “shoulders”]

We would have a separate db of a generic set of workout and their muscle groups, so people can search for workouts outside their db


