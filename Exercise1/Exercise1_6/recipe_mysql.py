import mysql.connector

#Connect to the MySQL server
conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password')

#Create a database and a table
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS task_database;")
cursor.execute("USE task_database;")

cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
    id                  INT AUTO_INCREMENT PRIMARY KEY,
    name                VARCHAR(50),
    ingredients         VARCHAR(255),
    cooking_time        INT,
    difficulty          VARCHAR(20)
);''')

#Calculate Difficulty
def calculate_difficulty(cooking_time, ingredients):
  ingredients = ingredients.split(",")
  ingredients_len = len(ingredients)
  if cooking_time < 10 and ingredients_len < 4:
    return "Easy"
  elif cooking_time < 10 and ingredients_len >= 4:
    return "Medium"
  elif cooking_time >= 10 and ingredients_len < 4:
    return "Intermediate"
  else:
    return "Hard"
  
def standardize_ingredients(ingredients):
  ingredients = ingredients.split(",")
  ingredients = [ingredient.strip().capitalize() for ingredient in ingredients]
  return ",".join(ingredients)

def check_input_for_digit(string):
  while True:
    try:
      var = int(input(string))
      return var
    except ValueError:
      print("Please enter a valid number")

def display_recipe(row):
    print("Recipe ID." + str(row[0]))
    print("   Recipe Name: " + row[1])
    print("   Ingredients: " + row[2])
    print("   Cooking Time: " + str(row[3]))
    print("   Difficulty: " + row[4] + "\n")


#Create Recipe
def create_recipe(conn, cursor):
  name = input("Enter recipe name: ")
  ingredients = input("Enter ingredients (comma separated): ")
  cooking_time = check_input_for_digit("Enter cooking time (in minutes): ")
  difficulty = calculate_difficulty(cooking_time, ingredients)
  standardize_ingredients(ingredients)

  query = """
    INSERT INTO Recipes (name, ingredients, cooking_time, difficulty)
    VALUES (%s, %s, %s, %s);
    """
  cursor.execute(query, (name, ingredients, cooking_time, difficulty))
  conn.commit()
  print("Recipe was added successfully")

#Search Recipe
def search_recipe(cursor):
    cursor.execute("SELECT DISTINCT ingredients FROM Recipes;")
    results = cursor.fetchall()

    all_ingredients = set()

    for row in results:
        ingredients = row[0]
        all_ingredients.update(ingredients.split(', '))

    print("\nAll available ingredients:")
    for count, ingredient in enumerate(sorted(all_ingredients), start=1):
        print(f"{count}. {ingredient}")

    choice = check_input_for_digit("Type the number of an ingrdient: ") - 1
    search_ingredient = sorted(all_ingredients)[choice]

    search_query = "SELECT * FROM Recipes WHERE ingredients LIKE %s;"
    cursor.execute(search_query, ('%' + search_ingredient + '%',))
    
    results = cursor.fetchall()
    if results:
        for row in results:
            display_recipe(row)
    else:
        print("This ingredient is found in no recipe.")

#Update Recipe
def update_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()
    
    print("\nAvailable Recipes:")
    for row in recipes:
        print(f"ID: {row[0]}, Name: {row[1]}")

    recipe_id = check_input_for_digit("Which Recipe do you want to update?: ")
    column_to_update = input("What do you want to update? (name, ingredients, cooking_time): ")

    updated_column = None
    if column_to_update == 'name':
        updated_column = input("Enter a new name: ")
        query = "UPDATE Recipes SET name = %s WHERE id = %s;"
        cursor.execute(query, (updated_column, recipe_id))
    elif column_to_update == 'ingredients':
        updated_column = input("Enter new ingredients (comma-separated): ")
        standardize_ingredients(updated_column)
        query = "UPDATE Recipes SET ingredients = %s WHERE id = %s;"
        cursor.execute(query, (updated_column, recipe_id))
    elif column_to_update == 'cooking_time':
        updated_column = check_input_for_digit("Enter a new cooking time (in minutes): ")
        query = "UPDATE Recipes SET cooking_time = %s WHERE id = %s;"
        cursor.execute(query, (updated_column, recipe_id))
    else:
        print("\nNo valid parameter.")
        return

    if column_to_update in ['ingredients', 'cooking_time']:
        cursor.execute("SELECT cooking_time, ingredients FROM Recipes WHERE id = %s;", (recipe_id,))
        row = cursor.fetchone()
        difficulty = calculate_difficulty(row[0], row[1])
        query = "UPDATE Recipes SET difficulty = %s WHERE id = %s;"
        cursor.execute(query, (difficulty, recipe_id))

    conn.commit()
    print("Recipe updated successfully!")

#Delete Recipe
def delete_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    recipes = cursor.fetchall()
    
    print("\nAvailable Recipes:")
    for row in recipes:
        print(f"ID: {row[0]}, Name: {row[1]}")

    recipe_id = check_input_for_digit("Enter the number of the recipe you want to delete: ")

    delete_query = "DELETE FROM Recipes WHERE id = %s"
    cursor.execute(delete_query, (recipe_id,))
    conn.commit()
    print("Recipe was deleted successfully!")


#Main Menu
choice = 0
while(choice != 9):
  print("1. Create Recipe")
  print("2. Search Recipe")
  print("3. Update Recipe")
  print("4. Delete Recipe")
  print("9. Exit")
  choice = check_input_for_digit("Enter your choice: ")

  if choice == 1:
    create_recipe(conn, cursor)
  elif choice == 2:
    search_recipe(cursor)
  elif choice == 3:
    update_recipe(conn, cursor)
  elif choice == 4:
    delete_recipe(conn, cursor)
  elif choice == 9:
    print("Exiting...")
    break
  else:
    print("Invalid choice")
