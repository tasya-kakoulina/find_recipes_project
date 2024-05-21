from bs4 import BeautifulSoup
import requests  # library to access sites


def set_recipe_urls(catalog_url):  # parses recipe catalogs for paths of recipes, returns set of paths
    page = requests.get(catalog_url)
    soup = BeautifulSoup(page.text, "html.parser")
    hrefs_set = set()
    for link in soup.find_all('a'):
        href = link.get('href')
        if href[:19] == "/recipes/selection/" and href[19:20] in "abcdefghijklmnopqrstuvwxyz" and href not in hrefs_set:
            hrefs_set.add(href)
    return hrefs_set


def write_recipe_urls(catalog_url):  # writes paths into paths.txt
    hrefs = list(set_recipe_urls(catalog_url))
    with open('paths.txt', 'a', encoding="utf-8") as hrefs_file:
        for href in hrefs:
            hrefs_file.write(f'{href}\n')


def get_recipe_urls(catalog_url):  # two previous functions combo
    set_recipe_urls(catalog_url)
    write_recipe_urls(catalog_url)


def get_ingredients(recipe_url):  # parses the site, adds the name and ingredients with dividers into ingredients.txt
    page = requests.get(recipe_url)
    soup = BeautifulSoup(page.text, "html.parser")
    ingredients = soup.find_all('span', class_="g-ingredient__name text-l")
    recipe_name = soup.find_all('h1', class_="h2 mb-4 mb-md-32")
    with open('ingredients.txt', 'a', encoding="utf-8") as ingr_file:
        for r_n in recipe_name:
            ingr_file.write(f'{r_n.text}\n')
        ingr_file.write('---\n')  # recipe name divider
        for ingredient in ingredients:
            ingr_file.write(f'{ingredient.text}\n')
        ingr_file.write('///\n')  # different recipes divider


page_count = -1
for i in range(100, 90, -1):  # looking for the amount of recipe catalog pages
    a = set_recipe_urls("https://здоровое-питание.рф/recipes-book/?PAGEN_1=" + str(i))
    b = set_recipe_urls("https://здоровое-питание.рф/recipes-book/?PAGEN_1=" + str(i - 1))
    if a.intersection(b) == set():
        print(i, "pages")
        page_count = i
        break

# get_recipe_urls("https://здоровое-питание.рф/recipes-book/")
for i in range(page_count, 0, -1):  # getting ALL recipe links
    get_recipe_urls("https://здоровое-питание.рф/recipes-book/?PAGEN_1=" + str(i))
with open('paths.txt', 'r', encoding="utf-8") as paths_file:
    paths = paths_file.read().split('\n')  # reading the file
    for path in paths:
        get_ingredients("https://здоровое-питание.рф" + path)  # creating a url to parse, parsing
