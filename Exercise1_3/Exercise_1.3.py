recipes_list = []
ingredients_list = []

def take_recipe():
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time: "))
    ingredients = input("Enter the ingredients separated by commas: ")

    return {"name": name, "cooking_time": cooking_time, "ingredients": ingredients.split(",")}

n = int(input("How many recipes would you like to enter?"))

for i in range(n):
  recipe = take_recipe()
  for ingredient in recipe["ingredients"]:
    if ingredient not in ingredients_list:
      ingredients_list.append(ingredient)
  recipes_list.append(recipe)

for recipe in recipes_list:
  ingredient_len = len(recipe["ingredients"]) 
  cooking_time = recipe["cooking_time"]

  if cooking_time < 10 and ingredient_len < 4:
    recipe["difficulty"] = "Easy"
  elif cooking_time < 10 and ingredient_len >= 4:
    recipe["difficulty"] = "Medium"
  elif cooking_time >= 10 and ingredient_len < 4:
    recipe["difficulty"] = "Intermediate"
  else:
    recipe["difficulty"] = "Hard"

for recipe in recipes_list:
  print("Recipe: " + recipe["name"])
  print("Cooking time (min): " + str(recipe["cooking_time"]))
  print("Ingredients:")
  for ingredient in recipe["ingredients"]:
    print(ingredient.strip())
  print("Difficulty level: " + recipe["difficulty"])

print("-----------------------------------------")
print("Ingredients Available Across All Recipes:")
print("-----------------------------------------")
for ingredient in ingredients_list:
  print(ingredient.strip())
