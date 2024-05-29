## INITIAL EDITS, NEED TO DO MORE

Code Review Edits
https://github.com/spruhaN/nutrition_pal/issues/7 - Sam Todd
Changed return from fetchone() to scalar_one()
Refactored code to have prefix, standardizing inconsistencies
Inconsequential to combine, left as is
Removed unnecessary variable for sql executions where we do not care about return val
All Basemodels moved to top of file during refactoring
Combining sql statements inconsequential, did not do so in daily_calories GET
Did not add further descriptive comments to endpoints, initial func def is enough and code is simple enough
Deleted duplicate schema.sql
Did not place files containing workflows, diagrams, etc in specific folder as they already exists separate from actual code
Ditto
Added exception handling when incorrect data is inputted and/or no return
We removed the ingredient_id component of meals, not relevant

https://github.com/spruhaN/nutrition_pal/issues/19 - Kyle Reeves
Placed endpoints in distinct files
(MUST REFACTOR ALL REFERENCE TO CUSTOMER TO USER)
(ERROR HANDLING FOR DAILY CAL IS NO GOAL ADDED)
If the user does not want to post an actual workout and wants to input something useless, that is of no concern for us, they may also have unique names for workouts, difficult to check
Added error handling for negative daily_caloric goal
Added error handling if negative values for workouts given
Ditto for height and weight
Ditto for calories
Changed te name of duplicate endpoint
(MUST CHANGE TO EITHER ADD TYPE FOR MEAL POST OR REMOVE RETURN)
Made it so user can only input one goal, thus invalid
Combining sql statements irrelevant, did not combine

https://github.com/spruhaN/nutrition_pal/issues/18 - Dale Parcley
(ADD MORE MUSCLES AND WOKROUTS)
No negative caloric values allowed, user can guesstimate and then update entry later
Irrelevant, meal type is whatever is beneficial to the user
Don’t want to be too specific for muscles, not everyone is a kinesiology majors
Refactored to be more organized, distinct endpoints files
Added units of measurements in API spec
Yes we don’t have reminders, beyond scope of project
Fixed, nothing to do with design anyways
Refactored main.py into separates endpoint files
Is no expected progress, just goals and user input, not relevant to product
Put primary muscle involved
Deleted 2nd schem.sql file

https://github.com/spruhaN/nutrition_pal/issues/13 - Asa
Refactored endpoints into different files
Uses scalar_one() instead of fetchone() for simpler code
Added units for height and weight in API SPEC
Added rating for meals, we don’t believe any more attributes adds relevant value
Made it so user can only have one goal, and they can update, thus, issue with daily_calories is obsolete
Changed name of one function that had exact name of other, thus, differentiating endpoint
No longer causes internal server error

https://github.com/spruhaN/nutrition_pal/issues/3 - James Irwin
We refactored main.py into individual endpoint files
Ditto
Added additional exercises to offer more options
Not adding ‘heart’, no one says I’m training heart today
Added recommendation endpoints for users to follow our mission statement
Alls functions have comments describing purpose now
Added exception handling and error catching
Defined units of measurement in API spec for height and weight
No relevant, do not need to add missing muscle ids, doesn’t effect code
Rows not being in chronological order by ids is not relevant
Removed unused variables that are results of sql transactions where we do not care about return values
Package.json was unnecessary, we removed it from the codebase

https://github.com/spruhaN/nutrition_pal/issues/2 - Rhoyalinn Cereno
Refactored project so endpoints have individual files
Did not place informative files into unique folder as they essentially are already, they are not intermixed with any code
Added comments to functions to increase readability
Changed name of one of the duplicate functions
(MAKE getWorkoutsByDay and getWorkoutsByGroup MORE UNDERSTANDABLE)
Deleted instances where variables are not used
Inconsequential change, leave as SELECT … AS id
Capitalized all keywords in sql statements for better readability
Removed statement in API spec that was irrelevant to endpoint
 Added error checking for negative values where appropriate in codebase
Not going to allow unique units for height, weight, calories, lets assume this is only in the US
Not changing variable name, it is overwritten

