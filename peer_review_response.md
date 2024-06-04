## INITIAL EDITS, NEED TO DO MORE

Code Review Edits


## https://github.com/spruhaN/nutrition_pal/issues/7 - Sam Todd



1. Changed return from fetchone() to scalar_one()
2.  Refactored code to have prefix, standardizing inconsistencies
3.  Inconsequential to combine, left as is
4.  Removed unnecessary variable for sql executions where we do not care about return val
5.  All Basemodels moved to top of file during refactoring
6.  Combining sql statements inconsequential, did not do so in daily_calories GET
7.  Did not add further descriptive comments to endpoints, initial func def is enough and code is simple enough
8.  Deleted duplicate schema.sql
9.  Did not place files containing workflows, diagrams, etc in specific folder as they already exists separate from actual code
10. ^
11. Added exception handling when incorrect data is inputted and/or no return
12. We removed the ingredient_id component of meals, not relevant

## https://github.com/spruhaN/nutrition_pal/issues/19 - Kyle Reeves

1. Placed endpoints in distinct files
2. (MUST REFACTOR ALL REFERENCE TO CUSTOMER TO USER)
3. (ERROR HANDLING FOR DAILY CAL IS NO GOAL ADDED)
4. If the user does not want to post an actual workout and wants to input something useless, that is of no concern for us, they may also have unique names for workouts, difficult to check
5. Added error handling for negative daily_caloric goal
6. Added error handling if negative values for workouts given
7. Ditto for height and weight
8. Ditto for calories
9. Changed te name of duplicate endpoint
10. (MUST CHANGE TO EITHER ADD TYPE FOR MEAL POST OR REMOVE RETURN)
11. Made it so user can only input one goal, thus invalid
12. Combining sql statements irrelevant, did not combine

## https://github.com/spruhaN/nutrition_pal/issues/18 - Dale Parcley


1. (ADD MORE MUSCLES AND WOKROUTS)
2. No negative caloric values allowed, user can guesstimate and then update entry later
3. Irrelevant, meal type is whatever is beneficial to the user
4. Don’t want to be too specific for muscles, not everyone is a kinesiology majors
5. Refactored to be more organized, distinct endpoints files
6. Added units of measurements in API spec
7. Yes we don’t have reminders, beyond scope of project
8. Fixed, nothing to do with design anyways
9. Refactored main.py into separates endpoint files
10. Is no expected progress, just goals and user input, not relevant to product
11. Put primary muscle involved
12. Deleted 2nd schema.sql file


## https://github.com/spruhaN/nutrition_pal/issues/13 - Asa


1. Refactored endpoints into different files
2. Uses scalar_one() instead of fetchone() for simpler code
3. Added units for height and weight in API SPEC
4. Added rating for meals, we don’t believe any more attributes adds relevant value
5. Made it so user can only have one goal, and they can update, thus, issue with daily_calories is obsolete
6. Changed name of one function that had exact name of other, thus, differentiating endpoint
7. No longer causes internal server error


## https://github.com/spruhaN/nutrition_pal/issues/3 - James Irwin


1. We refactored main.py into individual endpoint files
2. Ditto
3. Added additional exercises to offer more options
4. Not adding ‘heart’, no one says I’m training heart today
5. Added recommendation endpoints for users to follow our mission statement
6. Alls functions have comments describing purpose now
7. Added exception handling and error catching
8. Defined units of measurement in API spec for height and weight
9. Not relevant, do not need to add missing muscle ids, doesn’t effect code
10. Rows not being in chronological order by ids is not relevant
11. Removed unused variables that are results of sql transactions where we do not care about return values
12. Package.json was unnecessary, we removed it from the codebase


## https://github.com/spruhaN/nutrition_pal/issues/2 - Rhoyalinn Cereno


1. Refactored project so endpoints have individual files
2. Did not place informative files into unique folder as they essentially are already, they are not intermixed with any code
3. Added comments to functions to increase readability
4. Changed name of one of the duplicate functions
5. (MAKE getWorkoutsByDay and getWorkoutsByGroup MORE UNDERSTANDABLE)
6. Deleted instances where variables are not used
7. Inconsequential change, leave as SELECT … AS id
8. Capitalized all keywords in sql statements for better readability
9. Removed statement in API spec that was irrelevant to endpoint
10. Added error checking for negative values where appropriate in codebase
11. Not going to allow unique units for height, weight, calories, lets assume this is only in the US
12. Not changing variable name, it is overwritten

