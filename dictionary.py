import re

with open('ingredients.txt', 'r', encoding='utf-8') as file:
    culinary_book_text = file.read()

recipes_list = culinary_book_text.split('///')   # список всех рецептов (названия и ингредиенты вместе)
names_list = []    # список названий всех рецептов
ingredients_list = []     # список ингредиентов-строк всех рецептов (с повторениями)

for recipe in recipes_list:
    name_n_ingredients = recipe.split('---')   # отделяем названия рецептов от ингредиентов
    recipe_name = name_n_ingredients[0].replace('\n', '').strip()   # выделяем названия отдельно, очищаем их
    names_list.append(recipe_name)
    ingredients = recipe[recipe.find('---') + 3:].strip().lower()   # выделяем ингредиенты отдельно, очищаем их
    ingredients_list.append(ingredients)

ingredients_list_list = []    # список, в котором будут находиться списки ингредиентов каждого рецепта

for ingredients in ingredients_list:
    ingredients = re.sub(r'\([^()]*\)', '', ingredients)
    mini_list = re.split('\n|,| и ', ingredients)   # список ингредиентов отдельно взятого рецепта
    ingredients_list_list.append(mini_list)  # список списков ингредиентов различных рецептов (с повторениями)

# словарь, в котором ключи - названия рецептов, а значения - списки их ингредиентов
culinary_book = {key: value for key, value in zip(names_list, ingredients_list_list)}
