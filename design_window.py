import PySimpleGUI as sg
from printtry import process_input_products

# тема окошечка из библиотеки
sg.theme('LightGreen3')

# устанавливаем элементы в интерфейсе
layout = [ [sg.Text("Добро пожаловать в кулинарную книгу \"Здоровое питание\"!")],
           [sg.Text("Введите продукты: "), sg.InputText(key='text')],
           [sg.Button("Найти рецепт"), sg.Button("Назад")],
           [sg.Output(size=(60, 10))] ]
# окошечко программы
window = sg.Window('Cookbook', layout, size=(500,300))

# для того, чтобы вывести подходящие рецепты, мы проходимся по всем значениям словаря
# и находим множество, в котором совпадают большинство стеммингов; выводим на экран ключи
# если
while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, "Назад"):
        break

    if event == "Найти рецепт":
        input = values['text']
        process_input_products(input)

window.close()