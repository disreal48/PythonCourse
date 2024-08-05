import pickle

def display_recipe(recipe):
    print(f"Name: {recipe['name']}")
    print(f"Cooking Time: {recipe['cooking_time']}")
    print("Ingredients:")
    for ingredient in recipe["ingredients"]:
        print(ingredient)
    print(f"Difficulty: {recipe['difficulty']}")

def search_ingredient(data):
    for count, ingredient in enumerate(data["all_ingredients"], 1):
      print(count, ingredient.strip())

    try:
        ingredient_index = int(input("Enter the number of the ingredient you would like to search for: "))
        ingredient_searched = data["all_ingredients"][ingredient_index - 1]
    except ValueError:
        print("The input was not a number")
    except IndexError:
        print("The number was out of range")
    except:
        print("Something horribly happened. Please contact the support.")
    else:
        for recipe in data["recipes_list"]:
            if ingredient_searched in recipe["ingredients"]:
                display_recipe(recipe)

def main():
    file_name = input("Enter the file name: ")

    try:
        data = pickle.load(open(file_name, "rb"))
    except FileNotFoundError:
        print("The File has not been found")
    except:
        print("Something went south")
    else:
        search_ingredient(data)

main()