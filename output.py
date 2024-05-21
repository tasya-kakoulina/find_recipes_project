import book2 
import re
from nltk.stem.snowball import SnowballStemmer


# функция возвращает список из пар элементов (имя рецепта, количество ингредиентов, которых не хватает) -> list[(str, int)
def find_recipes_by_user_products(user_products):
    recipes_matches: list[(str, int)] = [] # создаем список, в котором будет храниться имена рецептов;
    # но имена конкретно тех рецептов, у которых все ингредиенты совпали, и также тех, у которых нужно докупить несколько продуктов
    # именно поэтому я ввожу еще int, в котором будет содержаться количество не совпадающих ингредиентов (потом мне будет удобнее выводить на экран)

    for title, ingridients in book2.culinary_book.items(): #прохожусь по кулинарной книге
        exists_products = set() # создаю set, в котором будут храниться те ингредиенты, которые совпали с рецептом
        ingridients_str = " ".join(ingridients) # сделала set ингредиентов одной строкой, чтобы через re.findall()) работать удобнее было

        for product in user_products:
            exists_products = exists_products.union(set(re.findall(product, ingridients_str)))
            # прохожусь по всем продуктам юзера и с помощью регулярки оставляю те значения юзера,
            # которые совпали со значениями рецепта в словаре

        if len(user_products) == len(exists_products): # если количество продуктов юзера равно совпадениям, то они реально существуют ТО ЕСТЬ ОН НАШЕЛ ВСЕ ПРОДУКТЫ ВВЕДЕННЫЕ
            missing_ingredients = len(ingridients) - len(exists_products) # количество отсутствующих продуктов
            recipes_matches.append((title, missing_ingredients)) # добавляем в списочек

    return recipes_matches


# функция, которая выводит на экран каждый рецепт, в котором совпали все ингредиенты; рецепт, в котором совпали
# ингредиенты частично, и мы ограничиваемся 3 продуктами, которых может не хватать
def print_it_on_the_screen(user_products: list[str]):
    recipes_matches: list[(str, int)] = find_recipes_by_user_products(user_products)

    if not recipes_matches: #может такое быть, что не все продукты совпали; печатаем сразу отбой!
        print(f"К сожалению, мы не смогли подобрать для вас рецепты. Попробуйте ввести иную комбинацию.")
    else:
        recipes_matches.sort(key=lambda x: x[1])
        # сортируем по возрастанию отсутствия ингредиентов, то есть если все ингредиенты есть, то рецепт в самом начале

        max_count_of_missing_products = 3

        for title, missing_products_count in recipes_matches:
            count_for_values = len(book2.culinary_book[title])
            if missing_products_count == 0: # 0 отсутствующих, значит мои поздравления, мы выводим на экран
                print(f"Поздравляем, у вас есть все продукты для рецепта \"{title}\", всего ингредиентов: {count_for_values}")
            elif 0 < missing_products_count < max_count_of_missing_products:
                print(f"В рецепте \"{title}\" вам понадобится к введенным продуктам дополнительно {missing_products_count} ингредиента(ов).")
                continue
            elif missing_products_count >= count_for_values or missing_products_count >= max_count_of_missing_products:
                print(f"Для некоторых рецептов вам потребуется ещё большее количество продуктов. Можете попробовать ввести другую комбинацию!")
                break


def process_input_products(input_products):
    input_products = input_products.lower().split(', ')
    processed_products = []
    stemmer = SnowballStemmer("russian")
    for i in input_products:
        if ' ' in i:
            i = i.split(' ')
            i = [stemmer.stem(j) for j in i]
            i = ' '.join(i)
        processed_products.append(i)
    user_products = [stemmer.stem(i) for i in processed_products]
    print_it_on_the_screen(user_products)
