# Fake Data Modeling
#### Python File: https://github.com/spruhaN/fake_post_data/blob/master/populate_posts.py
#### Write-up: 
To get to a million rows of data we needed to add a million rows to our user database, one for each user. Our script randomizes the number of exercises it adds per user and ranges from one to seven, meaning that the user_workout database contains one million to seven million rows. The same logic applied to meals except we capped each user at five meals, implying that our meals database can range from one to five million rows. As for the the workouts and muscle_groups, all of the rows within them are predefined so they are 29 and 14 rows, in that order.
As for our justification we believe that our databases would source this way since we are assuming that per day a user is working out 1-7 times and eating 1-5 meals, if we were to expand on this application we would be deleting previous workouts and meals as they are non-consequential to our current endpoints.

# Performance results of hitting endpoints

For each endpoint, list how many ms it took to execute. State which three endpoints were the slowest.
### /meal/{user_id}
1.125 ms

### /meal/{user_id}/{meal_id}
3.881 ms

### /meal/{user_id}/day
28.125 ms

### /meal/{user_id}/recommend
539.081 ms

### /workout/{user_id}
41ms

### /workout/{user_id}/day
39ms

### /workout/muscle_groups/{type}
2.1ms

### /workout/{workout_id}/muscle_groups
0.8ms

### /workout/recommend/{user_id}/{type}
350ms

### (POST)/goal/{customer_id}
41.6ms

### (UPDATE)/goal/{customer_id}
0.75ms

### /user/
1.8ms

### /daily_calories/{user_id}
77ms

### /daily_calories{user_id}/average
38.400ms

# Performance tuning
For each of the three slowest endpoints, run explain on the queries and copy the results of running explain into the markdown file. Then describe what the explain means to you and what index you will add to speed up the query. Then copy the command for adding that index into the markdown and rerun explain. Then copy the results of that explain into the markdown and say if it had the performance improvement you expected. Continue this process until the three slowest endpoints are now acceptably fast (think about what this means for your service).

### 1. /meal/{user_id}/recommend
QUERY PLAN                                                                                                                                            |
----------------------------------------------------------------------------------------------------------------------------------------------------- |
Limit  (cost=32829.67..32829.68 rows=3 width=55) (actual time=538.826..538.927 rows=3 loops=1)                                                        |
  ->  Sort  (cost=32829.67..33162.74 rows=133229 width=55) (actual time=538.825..538.925 rows=3 loops=1)                                              |
        Sort Key: (CASE WHEN (meal.user_id = 199993) THEN (meal.rating * 2) ELSE meal.rating END) DESC                                                |
        Sort Method: top-N heapsort  Memory: 25kB                                                                                                     |
        ->  Nested Loop  (cost=8597.60..31107.71 rows=133229 width=55) (actual time=26.063..471.054 rows=399687 loops=1)                              |
              Join Filter: ((meal.calories)::numeric < ((goals.daily_calories)::numeric - (COALESCE(sum(meal_1.calories), '0'::numeric))))            |
              ->  Nested Loop  (cost=8597.60..8605.65 rows=1 width=40) (actual time=26.035..26.137 rows=1 loops=1)                                    |
                    ->  Index Scan using goals_customer_id_key on goals  (cost=0.42..8.44 rows=1 width=8) (actual time=0.027..0.030 rows=1 loops=1)   |
                          Index Cond: (user_id = 199993)                                                                                              |
                    ->  Aggregate  (cost=8597.18..8597.19 rows=1 width=32) (actual time=26.005..26.103 rows=1 loops=1)                                |
                          ->  Gather  (cost=1000.00..8597.17 rows=1 width=8) (actual time=25.966..26.082 rows=2 loops=1)                              |
                                Workers Planned: 2                                                                                                    |
                                Workers Launched: 2                                                                                                   |
                                ->  Parallel Seq Scan on meal meal_1  (cost=0.00..7597.07 rows=1 width=8) (actual time=20.128..20.132 rows=1 loops=3) |
                                      Filter: ((user_id = 199993) AND (EXTRACT(day FROM age(now(), "time")) = '0'::numeric))                          |
                                      Rows Removed by Filter: 133229                                                                                  |
              ->  Seq Scan on meal  (cost=0.00..13842.20 rows=399686 width=63) (actual time=0.015..230.076 rows=399687 loops=1)                       |
                    Filter: (((EXTRACT(day FROM age(now(), "time")) > '2'::numeric) AND (user_id = 199993)) OR (user_id <> 199993))                   |
                    Rows Removed by Filter: 2                                                                                                         |
Planning Time: 2.616 ms                                                                                                                               |
Execution Time: 539.081 ms                                                                                                                            |


### 2. /workout/recommend/{user_id}/{type}
### 3. /daily_calories/{user_id}
