# Flow 1.
Stephanie has some goals and wants to start tracking her calories. She inputs her desired daily calories for the foreseeable future through POST /goals once she gets the app. Now when she eats some food, a chimichanga lets say, she does POST /meal, adding her meal to the db. Then, later in the day she wants to see how many calories she needs to fulfill her goal so she does GET /daily_calories and it returns how much she needs based on previous meals. She then eats a pizza, POSTS /meals. Checks how many more calories with GET /daily_calories. She’s good, but wakes up feeling gross the next day. “What did I eat?” she thinks, so she may GET /meal/day and look at everything she ate. “I think it was the pizza…”. She probably won’t eat the pizza anymore.

# Flow 2. 
Marc comes to our service looking to start working out to build muscle and feel better about himself. First, Marc enters his goals by calling POST /goals. He is then interested in finding a workout regime, so he calls GET /workouts/plan to find a pre-made workout regime fit for his goals. Marc then remembers that he should be working many muscle groups each workout, so he may GET /workouts/id/muscle_groups to see which muscle groups he’ll be working for his assigned workout. Marc then realizes that his gym does not have the equipment for one of the suggested exercises, so he searches for an alternative with GET /workouts/muscle_groups/search. Now, Marc is confident about his plan for his next workout and leaves feeling good about himself.

# Flow 3.
Andrew M. is jealous of his roommate’s incredible physique. He asks his roommate how he is so jacked. His roommate does a GET /meal/day  and GET /workouts/day request for ever day in the past week. He shows Andrew what he ate and worked out. Andrew still doesn’t get it so his roommate does a GET /meal/meal_id/ingredients on a meal he’s pulled up to show him what part of the meal is good for you. Andrew gets inspired and creates an account, POST /goals some goals and then is ready to try and be as great as his roommate


# Endpoint

| Endpoint | Read or Write |
|-----------------|-----------------|
| /meal      | write      |
| /meal/day     | read      |
| /meal/create      | write      |
| /meal/meal_id/ingredients      | read      |
| /workout      | write      |
| /workout/plan     | read      |
| /workout/day      | read     |
| /workout/id/muscle_group      | read     |
| /workout/muscle_group      | read     |
| /goal    | write    |
| /daily_calories     | read     |






