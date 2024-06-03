# Fake Data Modeling
#### Python File: https://github.com/spruhaN/fake_post_data/blob/master/populate_posts.py
#### Write-up: 
To get to a million rows of data we needed to add a million rows to our user database, one for each user. Our script randomizes the number of exercises it adds per user and ranges from one to seven, meaning that the user_workout database contains one million to seven million rows. The same logic applied to meals except we capped each user at five meals, implying that our meals database can range from one to five million rows. As for the the workouts and muscle_groups, all of the rows within them are predefined so they are 29 and 14 rows, in that order.
As for our justification we believe that our databases would source this way since we are assuming that per day a user is working out 1-7 times and eating 1-5 meals, if we were to expand on this application we would be deleting previous workouts and meals as they are non-consequential to our current endpoints.

# Performance results of hitting endpoints

For each endpoint, list how many ms it took to execute. State which three endpoints were the slowest.
### /meal/{user_id}
| QUERY PLAN                                                                                 |
| ------------------------------------------------------------------------------------------ |
| Insert on meal  (cost=0.00..0.01 rows=0 width=0) (actual time=0.298..0.299 rows=0 loops=1) |
|   ->  Result  (cost=0.00..0.01 rows=1 width=104) (actual time=0.086..0.087 rows=1 loops=1) |
| Planning Time: 0.094 ms                                                                    |
| Trigger for constraint meal_customer_id_fkey: time=0.719 calls=1                           |
| Execution Time: 1.125 ms                                                                   |
### /meal/{user_id}/{meal_id}
| QUERY PLAN                                                                                                            |
| --------------------------------------------------------------------------------------------------------------------- |
| Update on meal  (cost=0.42..8.44 rows=0 width=0) (actual time=1.437..1.438 rows=0 loops=1)                            |
|   ->  Index Scan using meal_pkey on meal  (cost=0.42..8.44 rows=1 width=78) (actual time=0.325..0.329 rows=1 loops=1) |
|         Index Cond: (meal_id = 399689)                                                                                |
|         Filter: (user_id = 19)                                                                                        |
| Planning Time: 0.694 ms                                                                                               |
| Execution Time: 3.881 ms                                                                                              |
### /meal/{user_id}/day
| QUERY PLAN                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------- |
| Gather  (cost=1000.00..6931.91 rows=2 width=71) (actual time=23.729..27.996 rows=3 loops=1)                       |
|   Workers Planned: 2                                                                                              |
|   Workers Launched: 2                                                                                             |
|   ->  Parallel Seq Scan on meal  (cost=0.00..5931.71 rows=1 width=71) (actual time=19.425..19.426 rows=1 loops=3) |
|         Filter: (user_id = 199996)                                                                                |
|         Rows Removed by Filter: 133229                                                                            |
| Planning Time: 0.367 ms                                                                                           |
| Execution Time: 28.125 ms                                                                                         |
### /meal/{user_id}/recommend
| QUERY PLAN                                                                                                                                            |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Limit  (cost=32829.67..32829.68 rows=3 width=55) (actual time=538.826..538.927 rows=3 loops=1)                                                        |
|   ->  Sort  (cost=32829.67..33162.74 rows=133229 width=55) (actual time=538.825..538.925 rows=3 loops=1)                                              |
|         Sort Key: (CASE WHEN (meal.user_id = 199993) THEN (meal.rating * 2) ELSE meal.rating END) DESC                                                |
|         Sort Method: top-N heapsort  Memory: 25kB                                                                                                     |
|         ->  Nested Loop  (cost=8597.60..31107.71 rows=133229 width=55) (actual time=26.063..471.054 rows=399687 loops=1)                              |
|               Join Filter: ((meal.calories)::numeric < ((goals.daily_calories)::numeric - (COALESCE(sum(meal_1.calories), '0'::numeric))))            |
|               ->  Nested Loop  (cost=8597.60..8605.65 rows=1 width=40) (actual time=26.035..26.137 rows=1 loops=1)                                    |
|                     ->  Index Scan using goals_customer_id_key on goals  (cost=0.42..8.44 rows=1 width=8) (actual time=0.027..0.030 rows=1 loops=1)   |
|                           Index Cond: (user_id = 199993)                                                                                              |
|                     ->  Aggregate  (cost=8597.18..8597.19 rows=1 width=32) (actual time=26.005..26.103 rows=1 loops=1)                                |
|                           ->  Gather  (cost=1000.00..8597.17 rows=1 width=8) (actual time=25.966..26.082 rows=2 loops=1)                              |
|                                 Workers Planned: 2                                                                                                    |
|                                 Workers Launched: 2                                                                                                   |
|                                 ->  Parallel Seq Scan on meal meal_1  (cost=0.00..7597.07 rows=1 width=8) (actual time=20.128..20.132 rows=1 loops=3) |
|                                       Filter: ((user_id = 199993) AND (EXTRACT(day FROM age(now(), "time")) = '0'::numeric))                          |
|                                       Rows Removed by Filter: 133229                                                                                  |
|               ->  Seq Scan on meal  (cost=0.00..13842.20 rows=399686 width=63) (actual time=0.015..230.076 rows=399687 loops=1)                       |
|                     Filter: (((EXTRACT(day FROM age(now(), "time")) > '2'::numeric) AND (user_id = 199993)) OR (user_id <> 199993))                   |
|                     Rows Removed by Filter: 2                                                                                                         |
| Planning Time: 2.616 ms                                                                                                                               |
| Execution Time: 539.081 ms                                                                                                                            |


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
