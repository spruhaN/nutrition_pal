# Example workflow
# Flow 1. Tracking daily calories and inputting workouts
Stephanie has some goals and wants to start tracking her calories and meals. <br />
First she does a POST /user name ,weight height, "Stephanie", 100, 100, gets her id as a return
Then she POST /goals/{id} passing “lose weight”, “diet”,  and 2000<br />
Next she eats food and does a POST /meal/{id} passing “Mexican” and 800.<br />
She wants to see how many calories she has left GET /daily_calories/{id} returning 1200.<br />
She then eats a pizza, POSTS /meal/{id} passing “Italian” 1200. <br />
Checks calories with GET /daily_calories{id}, returns 0. <br />
Next day GET /meal/{id}/day returning a list of meals with an id, type, calorie, and time stamp<br />

# Testing results
<Repeated for each step of the workflow>
1. 
curl -X 'POST' \
  'https://fast-api-practice.onrender.com/user' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Stephanie",
    "weight": 100,
    "height": 100
  }'
2. 
{
  "id" : 3
}


1. 
curl -X 'POST' \
  'https://fast-api-practice.onrender.com/goals/3' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "diet",
    "goal": "I want to lose 20 pounds",
    "daily_calories": 2000
  }'
2. 
  "OK"


1. 
curl -X 'POST' \
  'https://fast-api-practice.onrender.com/meal/3' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Chimichange",
    "type": "Mexican",
    "calories": 800
  }'
2. 
  "OK"


1. 
curl -X 'GET' \
  'https://fast-api-practice.onrender.com/daily_calories/3' \
  -H 'accept: application/json' \
2. 
  {"calories_left" : 1200}


1. 
curl -X 'POST' \
  'https://fast-api-practice.onrender.com/meal/3' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Pepperoni Piiza",
    "type": "Italian",
    "calories": 1200
  }'
2. 
  "OK"


1. 
curl -X 'GET' \
  'https://fast-api-practice.onrender.com/daily_calories/3' \
  -H 'accept: application/json' \
2. 
  {"calories_left" : 0}

1. 
curl -X 'GET' \
  'https://fast-api-practice.onrender.com/meal/3/day' \
  -H 'accept: application/json' \
2. 
  [{
    "name": "Chimichange",
    "calories": 800,
    "time": "2024-05-07T04:34:43.301995+00:00",
    "type": null
}, {
    "name": "Pepperoni Piiza",
    "calories": 1200,
    "time": "2024-05-07T04:38:49.285678+00:00",
    "type": null
}]