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
|QUERY PLAN   
| Limit  (cost=32829.67..32829.68 rows=3 width=55) (actual time=538.826..538.927 rows=3 loops=1) <br>
|   ->  Sort  (cost=32829.67..33162.74 rows=133229 width=55) (actual time=538.825..538.925 rows=3 loops=1)  <br>
|   Sort Key: (CASE WHEN (meal.user_id = 199993) THEN (meal.rating * 2) ELSE meal.rating END) DESC  <br>
|  Sort Method: top-N heapsort  Memory: 25kB   <br>
| ->  Nested Loop  (cost=8597.60..31107.71 rows=133229 width=55) (actual time=26.063..471.054 rows=399687 loops=1)   <br>
|    Join Filter: ((meal.calories)::numeric < ((goals.daily_calories)::numeric - (COALESCE(sum(meal_1.calories), '0'::numeric))))<br>  
|    ->  Nested Loop  (cost=8597.60..8605.65 rows=1 width=40) (actual time=26.035..26.137 rows=1 loops=1)      <br>
|   ->  Index Scan using goals_customer_id_key on goals  (cost=0.42..8.44 rows=1 width=8) (actual time=0.027..0.030 rows=1 loops=1)  <br>
|    Index Cond: (user_id = 199993)   <br>
|     ->  Aggregate  (cost=8597.18..8597.19 rows=1 width=32) (actual time=26.005..26.103 rows=1 loops=1)    <br>
|     ->  Gather  (cost=1000.00..8597.17 rows=1 width=8) (actual time=25.966..26.082 rows=2 loops=1)        <br>
|      Workers Planned: 2                                                                                                    |<br>
|      Workers Launched: 2                                                                                                   |<br>
|     ->  Parallel Seq Scan on meal meal_1  (cost=0.00..7597.07 rows=1 width=8) (actual time=20.128..20.132 rows=1 loops=3) |<br>
|    Filter: ((user_id = 199993) AND (EXTRACT(day FROM age(now(), "time")) = '0'::numeric))                          |<br>
|     Rows Removed by Filter: 133229                                                                                  |<br>
|    ->  Seq Scan on meal  (cost=0.00..13842.20 rows=399686 width=63) (actual time=0.015..230.076 rows=399687 loops=1)                       |<br>
|      Filter: (((EXTRACT(day FROM age(now(), "time")) > '2'::numeric) AND (user_id = 199993)) OR (user_id <> 199993))                   |<br>
|      Rows Removed by Filter: 2                                                                                                         |<br>
| Planning Time: 2.616 ms                                                                                     |<br>
| Execution Time: 539.081 ms    <br>

### 2. /workout/recommend/{user_id}/{type}
GroupAggregate  (cost=30140.66..30161.95 rows=200 width=96) (actual time=205.838..217.240 rows=3 loops=1) <br>
Group Key: e.name<br>
->  Sort  (cost=30140.66..30144.98 rows=1729 width=40) (actual time=200.398..207.320 rows=72369 loops=1)<br>
Sort Key: e.name<br>
Sort Method: external merge  Disk: 2416kB<br>
->  Hash Join  (cost=13422.72..30047.68 rows=1729 width=40) (actual time=33.567..182.741 rows=72369 loops=1)    <br>      
Hash Cond: (c.exercise_id = e.id)<br>
->  Seq Scan on user_workouts c  (cost=13378.96..28674.78 rows=350073 width=16) (actual time=33.510..137.209 rows=676098 loops=1)   <br> 
Filter: (NOT (hashed SubPlan 1))<br>
Rows Removed by Filter: 24049 <br>
SubPlan 1<br>
->  Gather  (cost=1000.00..13378.95 rows=4 width=8) (actual time=33.494..33.557 rows=1 loops=1)  <br>
Workers Planned: 2<br>
Workers Launched: 2      <br>
->  Parallel Seq Scan on user_workouts  (cost=0.00..12378.55 rows=2 width=8) (actual time=21.144..31.059 rows=0 loops=3)<br>
Filter: ((user_id = 12413) AND ("time" >= (CURRENT_DATE - 3)))<br>
Rows Removed by Filter: 233382       <br>                      
->  Hash  (cost=43.69..43.69 rows=5 width=40) (actual time=0.043..0.045 rows=4 loops=1)<br>
Buckets: 1024  Batches: 1  Memory Usage: 9kB    <br>     
->  Hash Join  (cost=20.18..43.69 rows=5 width=40) (actual time=0.038..0.043 rows=4 loops=1)<br>
Hash Cond: (e.muscle_group_id = m.muscle_group_id)<br>
->  Seq Scan on exercises e  (cost=0.00..20.70 rows=1070 width=48) (actual time=0.003..0.004 rows=29 loops=1)<br>
->  Hash  (cost=20.12..20.12 rows=4 width=8) (actual time=0.009..0.010 rows=4 loops=1)<br>
Buckets: 1024  Batches: 1  Memory Usage: 9kB<br>
->  Seq Scan on muscle_groups m  (cost=0.00..20.12 rows=4 width=8) (actual time=0.005..0.007 rows=4 loops=1)<br>
Filter: ((type)::text = 'back'::text)   <br>                   
Rows Removed by Filter: 10<br>
Planning Time: 0.555 ms<br>
Execution Time: 217.905 ms <br>                              


### 3. /daily_calories/{user_id}
