from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql://cf-python:password@localhost/task_database")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return "<Recipe ID: " + str(self.id) + "-" + self.name + ">"
    
    def __str__(self):
        return f"""Name: {self.name}
Cooking Time: {self.cooking_time} minutes
Ingredients: {self.ingredients}
Difficulty: {self.difficulty}"""
    
    def return_ingredients_as_list(self):
        return self.ingredients.split(', ') if self.ingredients else []
    
    def calculate_difficulty(self):
      ingredients_len = len(self.return_ingredients_as_list())
      if self.cooking_time < 10 and ingredients_len < 4:
        self.difficulty =  "Easy"
      elif self.cooking_time < 10 and ingredients_len >= 4:
        self.difficulty =  "Medium"
      elif self.cooking_time >= 10 and ingredients_len < 4:
        self.difficulty =  "Intermediate"
      else:
        self.difficulty =  "Hard"
      

Base.metadata.create_all(engine)

def standardize_ingredients(ingredients):  
    return ", ".join(ingredients)

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
def create_recipe():
  while True:
    name = input("Enter recipe name: ")
    if session.query(Recipe).filter(Recipe.name == name).first():
        print("Recipe with this name already exists. Please enter a different name.")
    elif not 0 < len(name) <= 50:
        print("Recipe name must be between 1 and 50 characters.")
    else:
        break
    
  while True:
      igrendients_count = check_input_for_digit("Enter number of ingredients: ")
      if 0 < igrendients_count <= 10:
          break          
      else:
          print("Enter a number between 1 and 10.")

  ingredients = []

  for i in range(1, igrendients_count+1):
      while True:
          ingredient = input(f"Enter ingredient {i}: ")
          if 0 < len(ingredient) <= 50 and ingredient.isalpha():
                ingredients.append(ingredient)
                break
          else:
              print("Enter a valid ingredient name between 0 and 50 characters.")
                

  while True:
      cooking_time = check_input_for_digit("Enter cooking time (in minutes): ")
      if 0 < cooking_time <= 180:
          break
      else:
          print("Enter a number between 1 and 180.")

  ingredients_str = standardize_ingredients(ingredients)

  new_recipe = Recipe(name=name, ingredients=ingredients_str, cooking_time=cooking_time)
  new_recipe.calculate_difficulty()

  session.add(new_recipe)
  session.commit()
  print("Recipe was added successfully")

#View Recipes
def view_all_recipes():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("No recipes available.")
        return
    else:
        for recipe in recipes:
            print(recipe)

#Search Recipe by ingredient
def search_by_ingredients():    
    results = session.query(Recipe.ingredients).all()
    if not results:
        print("No recipes available.")
        return

    all_ingredients = set()

    for result in results:
        ingredients = result[0].split(", ")
        for ingredient in ingredients:
            all_ingredients.add(ingredient.strip())

    print("\nAll available ingredients:")
    for count, ingredient in enumerate(sorted(all_ingredients), start=1):
        print(f"{count}. {ingredient}")

    while True:
      choices = input("Type the numbers of ingredients separated by commas: ")
      if all(choice.isdigit() for choice in choices.split(",")):
          break
      else:
          print("Enter valid numbers separated by commas.")
    
    choices_list = choices.split(",")
    choices_list = [choice.strip() for choice in choices_list]
    search_ingredients = []

    for choice in choices_list:
        search_ingredients.append(sorted(all_ingredients)[int(choice)-1])
    
    conditions = []
    for ingredient in search_ingredients:
        conditions.append(Recipe.ingredients.like(f"%{ingredient}%"))

    results = session.query(Recipe).filter(*conditions).all()

    if results:
      for result in results:
        print(result)
    else:
      print("Ingredient(s) not found in any recipe.")

#Update Recipe
def update_recipe():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("No recipes available.")
        return
    
    results = session.query(Recipe.name, Recipe.ingredients, Recipe.cooking_time).all()

    print("\nAvailable Recipes:")
    for label, result in enumerate(results, 1):
        print(label, result.name)

    while True:
        recipe_id = check_input_for_digit("Which Recipe do you want to update?: ")
        if recipe_id in range(1, len(results)+1):
            break
        else:
            print("Recipe not found. Enter a valid recipe ID.")

    recipe_to_edit = session.query(Recipe).filter(Recipe.name == results[recipe_id-1].name).first()
    print("Which Attribute do you want to update?")
    print(f"1. Name (Currently {recipe_to_edit.name})")
    print(f"2. Ingredients (Currently {recipe_to_edit.ingredients})")
    print(f"3. Cooking Time (Currently {recipe_to_edit.cooking_time})")

    column_to_update = 0

    while True:
        column_to_update = check_input_for_digit("Enter the number of the attribute you want to update: ")
        if 0 < column_to_update <= 3:
            break
        else:
            print("Enter a valid number.")


    updated_column = None
    update_completed = False
    while not update_completed:
      if column_to_update == 1:
          while True:
              updated_column = input("Enter a new name: ")
              if 0 < len(updated_column) <= 50:
                  recipe_to_edit.name = updated_column
                  update_completed = True
                  break
              else:
                  print("Enter a name between 1 and 50 characters.")
      elif column_to_update == 2:
          while True:
              updated_column = input("Enter new ingredients (comma-separated): ")
              if 0 < len(updated_column) <= 255:
                  standardize_ingredients(updated_column)
                  recipe_to_edit.ingredients = updated_column
                  recipe_to_edit.calculate_difficulty()
                  update_completed = True
                  break
              else:
                  print("Enter ingredients between 1 and 255 characters.")
      elif column_to_update == 3:
          while True:
              updated_column = check_input_for_digit("Enter new cooking time (in minutes): ")
              if 0 < updated_column <= 180:
                  recipe_to_edit.cooking_time = updated_column
                  recipe_to_edit.calculate_difficulty()
                  update_completed = True
                  break
              else:
                  print("Enter a number between 1 and 180.")
      else:
          print("\nEnter a number between 1 and 3")
          return

    session.commit()
    print("Recipe updated successfully!")

#Delete Recipe
def delete_recipe():
    if session.query(Recipe).count() == 0:
        print("No recipes available.")
        return
    
    recipes = session.query(Recipe.id, Recipe.name).all()
    print("\nAvailable Recipes:")
    for recipe in recipes:
        print(recipe)

    while True:
      recipe_id = check_input_for_digit("Which Recipe do you want to delete?: ")
      if session.query(Recipe).filter(Recipe.id == recipe_id).first():
          break
      else:
          print("Recipe not found. Enter a valid recipe ID.")

    delete_query = session.query(Recipe).filter(Recipe.id == recipe_id).first()

    while True:
        confirm = input(f"Are you sure you want to delete {delete_query.name}? (y/n): ")
        if confirm.lower() in ['y', 'n']:
            break
        else:
            print("Enter 'y' or 'n'.")

    if confirm.lower() == 'y':
        session.delete(delete_query)
        session.commit()
        print("Recipe was deleted successfully!")
    else:
        print("Deletion cancelled.")


#Main Menu
choice = 0
while(choice != 9):
  print("1. Create a new recipe")
  print("2. View all recipes")
  print("3. Search for recipes by ingredients")
  print("4. Edit a recipe")
  print("5. Delete a recipe")
  print("9. Quit the application")

  choice = check_input_for_digit("Enter your choice: ")
  
  if choice == 1:
    create_recipe()
  elif choice == 2:
    view_all_recipes()
  elif choice == 3:
    search_by_ingredients()
  elif choice == 4:
    update_recipe()
  elif choice == 5:
    delete_recipe()
  elif choice == 9:
    print("Exiting...")
    session.close()
    engine.dispose()
    break
  else:
    print("Invalid choice")