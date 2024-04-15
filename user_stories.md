# User Stories
As someone who cooks food a lot, I want to see the nutritional contents of certain types of food so that I can know what amounts of protein, sugars, fats, etc. are in the food I make.
As an athlete, I want to know how many calories are in the food I eat so that I can make sure I am getting enough calories each day.
As someone who is trying to lose weight, I want to know how many calories and fats are in the food I eat so I can make sure I am not eating too much food.
As someone who likes to try new foods, I want to be able to sort through different foods based on certain criteria so that I can discover new things to try.
As someone who likes to bake, I want to be able to see the nutritional content of the ingredients I use so that I know what is in the baked goods.
As someone interested in nutrition, I want to be able to explore a database of foods with nutrition facts so that I can learn more about what kinds of foods have certain nutritional contents.
As someone who is lactose intolerant, I want to find lactose free foods that are also high in protein so that I can still reach my daily nutritional goals.
As someone who is allergic to nuts, I want to find healthy snack alternatives that have fats and proteins that I am lacking so that I can meet my nutritional goals.
As someone who has celiac’s disease, I want to find calorie dense foods that do not contain gluten so that I can still get enough calories in a day without bread or wheat products.
As someone with diabetes, I want to be aware of how much sugar is in my food so that I can maintain my blood sugar levels.
As someone who has a fast metabolism and struggles to eat a lot, I want to find calorie dense foods so that I can meet my calorie intake goals.
As someone looking to build a lot of muscle, I want to find protein dense foods so that I can build as much muscle as possible

# Exceptions
Exception: Food item not found.
Handling: Display a message stating "Food item not found. Please check the spelling or try a different item."
Exception: Nutritional information is incomplete or unavailable.
Handling: Notify the user with "Nutritional information is currently unavailable for this item."
Exception: Incomplete nutritional data due to a database error.
Handling: Show an error message "There was an error retrieving the data. Please try again later."
Exception: Filtering criteria return no results.
Handling: Display message "No foods match your criteria. Please adjust the filters."
Exception: The nutritional content is unavailable or not entered in the database.
Handling: The app prompts the user with a query to fill the content themselves
Exception: User is not able to view the database
Display Message “Database cannot be found, please retry later”
Exception: Food is unobtainable (expensive)
Handling: A lot of foods that meet the criteria of lactose free and protein rich are often expensive, if out of budget the foods will be prompted with a warning
Exception: App recommends nuts despite allergy
Handling: Option for user to say don’t recommend item/category again
Exception: App doesn’t know whether or not food has gluten
Handling: If the app doesn’t know if food has gluten in it, won’t recommend it.
Exception: Specific brands of food contain differing sugar levels.
Handling: App provides a warning to check the brand of the food the user is consuming
Exception: Not able to eat enough food to satisfy caloric goals
Handling: App would recommend meals at a greater frequency to support those that require more food
Exception: Can’t recommend specific protein foods
Handling: Has generic healthy food recommendations to give
