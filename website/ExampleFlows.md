# Flow 1. Tracking daily calories and inputting workouts
Stephanie has some goals and wants to start tracking her calories and meals. <br />
First she does a POST /user name ,weight height, "Stephanie", 100, 100, gets her id as a return
Then she POST /goals{id} passing “lose weight”, “diet” and 2000<br />
Next she eats food and does a POST /meal{id} passing “Mexican” and 800.<br />
She wants to see how many calories she has left GET /daily_calories{id} returning 1200.<br />
She then eats a pizza, POSTS /meal{id} passing “Italian” 1200. <br />
Checks calories with GET /daily_calories{id}, returns 0. <br />
Next day GET /meal{id}/day returning a list of meals with an id, type, calorie, and time stamp<br />


# Flow 2. Adding and looking up workout
Marc wants to build muscle<br />
Marc enters his goals by calling POST /goals passing “get big”, “workout”, 2800.<br />
He then begins adding workouts with with POST /workout passing “deadlift”, 3, 10, 0.<br />
He does this with multiple workouts at varying lengths, set, reps.<br />
His friends asks him what workouts he’s done, so he GET /workouts/days and returns a list of workout with “id”, “name”, “sets”, “reps”, “length”, "type", "group"<br />
His friend asks what to do for back, GET /workout/muscle_group/{type} passing “back” as type and returns a list of workouts "name", "type", and "group" for the back<br />

# Flow 3. Finding workout muscle_groups
Andrew M. is jealous of his roommate’s incredible physique. <br />
Andrew starts with a POST /goals passing “get huge, “workout”, 2800.<br />
He posts a workout POST /workout “squat”, 20, 20, 0.<br />
He wants to see what his workouts hit so he starts with GET /workout/day and gets a list of “id”, “name”, “sets”, “reps”, “length”, "type", and "group"<br />
He wants to see what his squat hits so he does a GET /workout/{id}/muscle_groups passing an id in that was in the prior return.<br />
This returns what muscles he's targeting<br />

We would have a separate db of a generic set of workout and their muscle groups, so people can search for workouts outside their db


