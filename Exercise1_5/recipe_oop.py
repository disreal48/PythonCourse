class Recipe(object):
  def __init__(self, name):
    self.name = name
    self.ingredients = []
    self.cooking_time = 0
    self.difficulty = None
    self.ingredient_len = len(self.ingredients)

  all_ingredients = []  

  def calculate_difficulty(self):
    if self.cooking_time < 10 and self.ingredient_len < 4:
        return "Easy"
    elif self.cooking_time < 10 and self.ingredient_len >= 4:
        return "Medium"
    elif self.cooking_time >= 10 and self.ingredient_len < 4:
        return "Intermediate"
    else:
        return "Hard"
    
  def get_name(self):
    return self.name  

  def get_cooking_time(self):
    return self.cooking_time
  
  def set_name(self, name):
    self.name = name

  def set_cooking_time(self, cooking_time):
    self.cooking_time = cooking_time

  def add_ingredient(self, *ingredients):
    self.ingredients.extend(ingredients)
    self.ingredient_len += len(ingredients)
    self.difficulty = self.calculate_difficulty()
    self.update_all_ingredients()

  def get_ingredients(self):
    return self.ingredients

  def get_difficulty(self):
    if self.difficulty is None:
        self.difficulty = self.calculate_difficulty()
    return self.difficulty

  def search_ingredient(self, ingredient):
    return ingredient in self.ingredients

  def update_all_ingredients(self):
    for ingredient in self.ingredients:
      if ingredient not in Recipe.all_ingredients:
        Recipe.all_ingredients.append(ingredient)

  def __str__(self):
    return f"""Name: {self.name}
Cooking Time: {self.cooking_time} minutes
Ingredients: {', '.join(self.ingredients)}
Difficulty: {self.get_difficulty()}"""
  
def recipe_search(data, search_term):
  for recipe in data:
    if recipe.search_ingredient(search_term):
      print(recipe)

tea = Recipe("Tea")
tea.add_ingredient("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)

print(tea)

coffee = Recipe("Coffee")
coffee.add_ingredient("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)
cake = Recipe("Cake")
cake.add_ingredient("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)
banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredient("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)

recipes_list = [tea, coffee, cake, banana_smoothie]

for ingredient in ["Water", "Sugar", "Bananas"]:
    recipe_search(recipes_list, ingredient)