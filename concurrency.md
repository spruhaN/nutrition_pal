# Concurrency
We will outline three cases where our service would encounter phenomenon if it had no concurrency control protection in place.

---
### 1. Non-Repeatable Read 
**Phenomenon**: A transaction reads the same row twice and gets a different value each time.
File: `meal.py` 
**Scenario**: A user requests a meal recommendation with `/meal/{customer_id}/recommend` at the same time their daily caloric goal is lowered with `/{customer_id}`, putting the recommended meal over the daily calorie goal.
```mermaid
sequenceDiagram
    participant S1 as Session 1
    participant DB as Database
    participant S2 as Session 2

    Note over S1, S2: Session 1 reads meal recommendations while Session 2 updates daily caloric goal.
    S1->>DB: SELECT daily_calories FROM goals WHERE customer_id = {customer_id}
    DB-->>S1: Returns daily_calories
    S2->>DB: UPDATE goals SET daily_calories = {new_value} WHERE customer_id = {customer_id}
    DB-->>S2: Confirm update
    S1->>DB: SELECT name, calories FROM meal WHERE calories < daily_calories ORDER BY rating DESC LIMIT 3
    DB-->>S1: Returns meals based on old daily_calories
    Note over S1: Session 1 may get incorrect meal recommendations due to changed daily caloric goal.
```
**Solution**: Implement a locking mechanism that does not allow READs and UPDATEs to happen at the same time.

---
### 2. Non-Repeatable Read *part 2, electric boogaloo* 
**Phenomenon**: A transaction reads the same row twice and gets a different value each time.
File: `meal.py` *again* 
**Scenario**: A user requests a meal recommendation with `/meal/{customer_id}/recommend` at the same time a meal is updated with `/{customer_id}/{meal_id}` such that their daily calories are changed, putting the recommended meal over the daily calorie goal.
```mermaid
 sequenceDiagram
    participant S1 as Session 1
    participant DB as Database
    participant S2 as Session 2

    Note over S1, S2: Session 1 reads meal recommendations while Session 2 updates a meal.
    S1->>DB: SELECT name, calories FROM meal WHERE calories < daily_calories ORDER BY rating DESC LIMIT 3
    DB-->>S1: Returns initial meal recommendations
    S2->>DB: UPDATE meal SET calories = {new_calories} WHERE customer_id = {customer_id} AND meal_id = {meal_id}
    DB-->>S2: Confirm update
    S1->>DB: SELECT name, calories FROM meal WHERE calories < daily_calories ORDER BY rating DESC LIMIT 3
    DB-->>S1: Returns updated meal recommendations
    Note over S1: Meal recommendations in Session 1 change after update.
```
**Solution**: Again, implement a locking mechanism that does not allow READs and UPDATEs to happen at the same time.

---
### 3. Lost update
**Phenomenon**: Two identical queries are executed, but the rows retrieved by the two are different.
File: `goal.py` 
**Scenario**: A user updates their calorie goal with `/{customer_id}` in 2 sessions at the same time, losing one of the updates.
```mermaid
sequenceDiagram
    participant S1 as Session 1
    participant DB as Database
    participant S2 as Session 2

    Note over S1, S2: Both sessions update the same calorie goal simultaneously.
    S1->>DB: UPDATE goals SET daily_calories = {new_calories} WHERE customer_id = {customer_id}
    S2->>DB: UPDATE goals SET daily_calories = {other_new_calories} WHERE customer_id = {customer_id}
    DB-->>S1: Confirm update
    DB-->>S2: Confirm update
    Note over S1, S2: Possible lost update scenario where one update may overwrite the other.

```
**Solution**: Raise transaction isolation level to REPEATABLE READ (default).

