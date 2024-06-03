# Fake Data Modeling
#### Python File: https://github.com/spruhaN/fake_post_data/blob/master/populate_posts.py
#### Write-up: 
To get to a million rows of data we needed to add a million rows to our user database, one for each user. Our script randomizes the number of exercises it adds per user and ranges from one to seven, meaning that the user_workout database contains one million to seven million rows. The same logic applied to meals except we capped each user at five meals, implying that our meals database can range from one to five million rows. As for the the workouts and muscle_groups, all of the rows within them are predefined so they are 29 and 14 rows, in that order.
As for our justification we believe that our databases would source this way since we are assuming that per day a user is working out 1-7 times and eating 1-5 meals, if we were to expand on this application we would be deleting previous workouts and meals as they are non-consequential to our current endpoints.

# Performance results of hitting endpoints

For each endpoint, list how many ms it took to execute. State which three endpoints were the slowest.
### /meal/{user_id}
### /meal/{user_id}/{meal_id}
### /meal/{user_id}/day
### /meal/{user_id}/recommend

### /workout/{user_id}
### /workout/{user_id}/day
### /workout/muscle_groups/{type}
### /workout/{workout_id}/muscle_groups
### /workout/recommend/{user_id}/{type}

### (POST)/goal/{customer_id}
### (UPDATE)/goal/{customer_id}

### /user/

### /daily_calories/{user_id}
### /daily_calories{user_id}/average

# Performance tuning
For each of the three slowest endpoints, run explain on the queries and copy the results of running explain into the markdown file. Then describe what the explain means to you and what index you will add to speed up the query. Then copy the command for adding that index into the markdown and rerun explain. Then copy the results of that explain into the markdown and say if it had the performance improvement you expected. Continue this process until the three slowest endpoints are now acceptably fast (think about what this means for your service).

### 1.
### 2.
### 3. 
