import pickle

def calc_difficulty(cooking_time, ingredient_len):
    if cooking_time < 10 and ingredient_len < 4:
        return "Easy"
    elif cooking_time < 10 and ingredient_len >= 4:
        return "Medium"
    elif cooking_time >= 10 and ingredient_len < 4:
        return "Intermediate"
    else:
        return "Hard"

def take_recipe():
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter the cooking time: "))
    ingredients = input("Enter the ingredients separated by commas: ")
    ingredients = [ingredient.strip() for ingredient in ingredients.split(",")]
    ingredient_len = len(ingredients)
    difficulty = calc_difficulty(cooking_time, ingredient_len)

    return {"name": name, "cooking_time": cooking_time, "ingredients": ingredients, "difficulty": difficulty}

def main():
    file_name = input("Enter the file name: ")
    try:
        file = open(file_name, "rb")
        data = pickle.load(file)
        recipes_list = data["recipes_list"]
        all_ingredients = data["all_ingredients"]
    except FileNotFoundError:
        print("The File has not been found")
        data = {"recipes_list": [], "all_ingredients": []}
    except:
        data = {"recipes_list": [], "all_ingredients": []}
    else:
        data.close()
    finally:
        recipes_list = data["recipes_list"]
        all_ingredients = data["all_ingredients"]

    recipe_count = int(input("How many recipes would you like to enter? "))

    for i in range(recipe_count):
      recipe = take_recipe()
      for ingredient in recipe["ingredients"]:
        if ingredient not in all_ingredients:
          all_ingredients.append(ingredient)
      recipes_list.append(recipe)

    data = {"recipes_list": recipes_list, "all_ingredients": all_ingredients}
    pickle.dump(data, open(file_name, "wb"))

main()
