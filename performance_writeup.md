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
12ms

### /workout/{user_id}/day
28ms

### /workout/muscle_groups/{type}
2.1ms

### /workout/{workout_id}/muscle_groups
0.8ms

### /workout/recommend/{user_id}/{type}
350ms

### (POST)/goal/{customer_id}
0.5ms

### (UPDATE)/goal/{customer_id}
0.75ms

### /user/
1.8ms

### /daily_calories/{user_id}
24ms

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

This explain tells me that most of the time is coming from scanning through the meals table looking for meals with the right calorie range. This leads me to believe that adding an index on calories in the meal table will speed this query up significantly. there is also a block of time coming from filtering by the date range, so I will add an index on that as well.

CREATE INDEX idx_goals_user_id ON goals(user_id);

CREATE INDEX idx_meal_user_id ON meal(user_id);

CREATE INDEX idx_meal_time ON meal(time);

CREATE INDEX idx_meal_user_time ON meal(user_id, time);

CREATE INDEX idx_meal_calories ON meal(calories);

CREATE INDEX idx_meal_user_calories ON meal(user_id, calories);

CREATE INDEX idx_meal_calories_time ON meal(calories, time);

| QUERY PLAN                                                                                                                                                 |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Limit  (cost=24241.02..24241.03 rows=3 width=55) (actual time=453.986..453.988 rows=3 loops=1)                                                             |
|   ->  Sort  (cost=24241.02..24574.09 rows=133229 width=55) (actual time=453.984..453.986 rows=3 loops=1)                                                   |
|         Sort Key: (CASE WHEN (meal.user_id = 199993) THEN (meal.rating * 2) ELSE meal.rating END) DESC                                                     |
|         Sort Method: top-N heapsort  Memory: 25kB                                                                                                          |
|         ->  Nested Loop  (cost=8.90..22519.06 rows=133229 width=55) (actual time=0.079..394.394 rows=399687 loops=1)                                       |
|               Join Filter: ((meal.calories)::numeric < ((goals.daily_calories)::numeric - (COALESCE(sum(meal_1.calories), '0'::numeric))))                 |
|               ->  Nested Loop  (cost=8.90..16.95 rows=1 width=40) (actual time=0.061..0.066 rows=1 loops=1)                                                |
|                     ->  Index Scan using idx_goals_user_id on goals  (cost=0.42..8.44 rows=1 width=8) (actual time=0.027..0.030 rows=1 loops=1)            |
|                           Index Cond: (user_id = 199993)                                                                                                   |
|                     ->  Aggregate  (cost=8.48..8.49 rows=1 width=32) (actual time=0.031..0.032 rows=1 loops=1)                                             |
|                           ->  Index Scan using idx_meal_user_id on meal meal_1  (cost=0.42..8.48 rows=1 width=8) (actual time=0.025..0.027 rows=2 loops=1) |
|                                 Index Cond: (user_id = 199993)                                                                                             |
|                                 Filter: (EXTRACT(day FROM age(now(), "time")) = '0'::numeric)                                                              |
|               ->  Seq Scan on meal  (cost=0.00..13842.23 rows=399687 width=63) (actual time=0.016..205.009 rows=399687 loops=1)                            |
|                     Filter: (((EXTRACT(day FROM age(now(), "time")) > '2'::numeric) AND (user_id = 199993)) OR (user_id <> 199993))                        |
|                     Rows Removed by Filter: 2                                                                                                              |
| Planning Time: 1.109 ms                                                                                                                                    |
| Execution Time: 454.144 ms           

I attempted to add a lot of indexes but none of them seemed to significantly increase the efficiency of this endpoint. The sequential scan on meal for the time and user_id seems to take a bulk of the time of this endpoint but I can't figure out how to properly index it so that it makes the query faster.

### 2. /workout/recommend/{user_id}/{type}
| QUERY PLAN                                                                                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| GroupAggregate  (cost=30140.70..30161.99 rows=200 width=96) (actual time=176.181..184.986 rows=3 loops=1)                                            |
|   Group Key: e.name                                                                                                                                  |
|   ->  Sort  (cost=30140.70..30145.03 rows=1729 width=40) (actual time=170.676..176.536 rows=72369 loops=1)                                           |
|         Sort Key: e.name                                                                                                                             |
|         Sort Method: external merge  Disk: 2416kB                                                                                                    |
|         ->  Hash Join  (cost=13422.73..30047.72 rows=1729 width=40) (actual time=29.217..154.342 rows=72369 loops=1)                                 |
|               Hash Cond: (c.exercise_id = e.id)                                                                                                      |
|               ->  Seq Scan on user_workouts c  (cost=13378.98..28674.83 rows=350074 width=16) (actual time=29.167..116.055 rows=676099 loops=1)      |
|                     Filter: (NOT (hashed SubPlan 1))                                                                                                 |
|                     Rows Removed by Filter: 24049                                                                                                    |
|                     SubPlan 1                                                                                                                        |
|                       ->  Gather  (cost=1000.00..13378.97 rows=4 width=8) (actual time=4.801..29.194 rows=1 loops=1)                                 |
|                             Workers Planned: 2                                                                                                       |
|                             Workers Launched: 2                                                                                                      |
|                             ->  Parallel Seq Scan on user_workouts  (cost=0.00..12378.57 rows=2 width=8) (actual time=17.955..26.035 rows=0 loops=3) |
|                                   Filter: ((user_id = 12413) AND ("time" >= (CURRENT_DATE - 3)))                                                     |
|                                   Rows Removed by Filter: 233382                                                                                     |
|               ->  Hash  (cost=43.69..43.69 rows=5 width=40) (actual time=0.036..0.038 rows=4 loops=1)                                                |
|                     Buckets: 1024  Batches: 1  Memory Usage: 9kB                                                                                     |
|                     ->  Hash Join  (cost=20.18..43.69 rows=5 width=40) (actual time=0.032..0.037 rows=4 loops=1)                                     |
|                           Hash Cond: (e.muscle_group_id = m.muscle_group_id)                                                                         |
|                           ->  Seq Scan on exercises e  (cost=0.00..20.70 rows=1070 width=48) (actual time=0.013..0.015 rows=29 loops=1)              |
|                           ->  Hash  (cost=20.12..20.12 rows=4 width=8) (actual time=0.006..0.007 rows=4 loops=1)                                     |
|                                 Buckets: 1024  Batches: 1  Memory Usage: 9kB                                                                         |
|                                 ->  Seq Scan on muscle_groups m  (cost=0.00..20.12 rows=4 width=8) (actual time=0.003..0.005 rows=4 loops=1)         |
|                                       Filter: ((type)::text = 'back'::text)                                                                          |
|                                       Rows Removed by Filter: 10                                                                                     |
| Planning Time: 0.561 ms                                                                                                                              |
| Execution Time: 185.546 ms                                                                                                                           |                            

First joins the user_workouts with exercises and muscle_groups <br>
Filters out rows not for specific type <br>
Then gets exercises user has done in past three days and filters those out <br>
Return! <br>

Adding Index onto user_id in user_workouts table led to time of 89ms.<br>

| QUERY PLAN                                                                                                                                                     |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Finalize GroupAggregate  (cost=11830.90..11893.27 rows=200 width=96) (actual time=59.244..60.601 rows=3 loops=1)                                               |
|   Group Key: e.name                                                                                                                                            |
|   ->  Gather Merge  (cost=11830.90..11886.27 rows=400 width=96) (actual time=57.751..60.589 rows=9 loops=1)                                                    |
|         Workers Planned: 2                                                                                                                                     |
|         Workers Launched: 2                                                                                                                                    |
|         ->  Partial GroupAggregate  (cost=10830.88..10840.08 rows=200 width=96) (actual time=51.839..54.453 rows=3 loops=3)                                    |
|               Group Key: e.name                                                                                                                                |
|               ->  Sort  (cost=10830.88..10832.68 rows=720 width=40) (actual time=50.126..51.436 rows=24123 loops=3)                                            |
|                     Sort Key: e.name                                                                                                                           |
|                     Sort Method: quicksort  Memory: 2392kB                                                                                                     |
|                     Worker 0:  Sort Method: quicksort  Memory: 2165kB                                                                                          |
|                     Worker 1:  Sort Method: quicksort  Memory: 2271kB                                                                                          |
|                     ->  Hash Join  (cost=52.29..10796.71 rows=720 width=40) (actual time=0.084..45.558 rows=24123 loops=3)                                     |
|                           Hash Cond: (c.exercise_id = e.id)                                                                                                    |
|                           ->  Parallel Seq Scan on user_workouts c  (cost=8.54..10199.14 rows=145864 width=16) (actual time=0.051..31.557 rows=225366 loops=3) |
|                                 Filter: (NOT (hashed SubPlan 1))                                                                                               |
|                                 Rows Removed by Filter: 8016                                                                                                   |
|                                 SubPlan 1                                                                                                                      |
|                                   ->  Index Scan using c_index on user_workouts  (cost=0.42..8.53 rows=4 width=8) (actual time=0.027..0.027 rows=1 loops=3)    |
|                                         Index Cond: (user_id = 12413)                                                                                          |
|                                         Filter: ("time" >= (CURRENT_DATE - 3))                                                                                 |
|                           ->  Hash  (cost=43.69..43.69 rows=5 width=40) (actual time=0.024..0.025 rows=4 loops=3)                                              |
|                                 Buckets: 1024  Batches: 1  Memory Usage: 9kB                                                                                   |
|                                 ->  Hash Join  (cost=20.18..43.69 rows=5 width=40) (actual time=0.018..0.023 rows=4 loops=3)                                   |
|                                       Hash Cond: (e.muscle_group_id = m.muscle_group_id)                                                                       |
|                                       ->  Seq Scan on exercises e  (cost=0.00..20.70 rows=1070 width=48) (actual time=0.004..0.006 rows=29 loops=3)            |
|                                       ->  Hash  (cost=20.12..20.12 rows=4 width=8) (actual time=0.007..0.008 rows=4 loops=3)                                   |
|                                             Buckets: 1024  Batches: 1  Memory Usage: 9kB                                                                       |
|                                             ->  Seq Scan on muscle_groups m  (cost=0.00..20.12 rows=4 width=8) (actual time=0.003..0.004 rows=4 loops=3)       |
|                                                   Filter: ((type)::text = 'back'::text)                                                                        |
|                                                   Rows Removed by Filter: 10                                                                                   |
| Planning Time: 0.867 ms                                                                                                                                        |
| Execution Time: 60.892 ms                                                                                                                                      |

### 3. /daily_calories/{user_id}
| QUERY PLAN                                                                                                                                   |
| -------------------------------------------------------------------------------------------------------------------------------------------- |
| Aggregate  (cost=8601.64..8601.65 rows=1 width=32) (actual time=23.446..27.458 rows=1 loops=1)                                               |
|   ->  Nested Loop  (cost=1000.42..8601.63 rows=1 width=8) (actual time=23.364..27.449 rows=2 loops=1)                                        |
|         ->  Gather  (cost=1000.00..8597.18 rows=1 width=8) (actual time=23.256..27.335 rows=2 loops=1)                                       |
|               Workers Planned: 2                                                                                                             |
|               Workers Launched: 2                                                                                                            |
|               ->  Parallel Seq Scan on meal  (cost=0.00..7597.08 rows=1 width=8) (actual time=19.152..19.154 rows=1 loops=3)                 |
|                     Filter: ((user_id = 199993) AND (EXTRACT(day FROM age(now(), "time")) = '0'::numeric))                                   |
|                     Rows Removed by Filter: 133229                                                                                           |
|         ->  Index Only Scan using goals_customer_id_key on goals  (cost=0.42..4.44 rows=1 width=0) (actual time=0.053..0.053 rows=1 loops=2) |
|               Index Cond: (user_id = 199993)                                                                                                 |
|               Heap Fetches: 0                                                                                                                |
| Planning Time: 1.199 ms                                                                                                                      |
| Execution Time: 27.638 ms                                                                                                                    |

From looking at the explain analyze, I can tell that there is a parallel seq scan that takes up most of the time. The filter that it is doing
is over the entire table and deals with the user_id and the time column of the meal table to filter the rows out that arent from the right
user and aren't today. Then the analysis shows that it uses the default index of customer_id on the goals table to quickly find the user's goal.

From this I am going to create an index on meals user_id and time

create index idx_user_id_time on meal (user_id, time)


| QUERY PLAN                                                                                                                                   |
| -------------------------------------------------------------------------------------------------------------------------------------------- |
| Aggregate  (cost=14.68..14.69 rows=1 width=32) (actual time=0.150..0.151 rows=1 loops=1)                                                     |
|   ->  Nested Loop  (cost=0.84..14.67 rows=1 width=8) (actual time=0.136..0.145 rows=2 loops=1)                                               |
|         ->  Index Scan using idx_user_id_time on meal  (cost=0.42..10.23 rows=1 width=8) (actual time=0.090..0.093 rows=2 loops=1)           |
|               Index Cond: (user_id = 199993)                                                                                                 |
|               Filter: (EXTRACT(day FROM age(now(), "time")) = '0'::numeric)                                                                  |
|         ->  Index Only Scan using goals_customer_id_key on goals  (cost=0.42..4.44 rows=1 width=0) (actual time=0.023..0.023 rows=1 loops=2) |
|               Index Cond: (user_id = 199993)                                                                                                 |
|               Heap Fetches: 0                                                                                                                |
| Planning Time: 1.111 ms                                                                                                                      |
| Execution Time: 0.284 ms                                                                                                                     |

This clearly drastically increased performance exactly how I wanted it to.
