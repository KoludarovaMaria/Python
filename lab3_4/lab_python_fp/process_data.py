import json
import os
import sys

# Добавляем текущую директорию в путь для импортов
sys.path.append(os.path.dirname(__file__))

from field import field
from gen_random import gen_random
from unique import Unique
from print_result import print_result
from cm_timer import cm_timer_1

# Путь к файлу данных внутри папки lab_python_fp
current_dir = os.path.dirname(__file__)
path = os.path.join(current_dir, 'data_light.json')

print(f"Ищем файл по пути: {path}")

# Загружаем данные
try:
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    print(f"Успешно загружено {len(data)} записей из data_light.json")
except FileNotFoundError:
    print(f"Ошибка: Файл {path} не найден!")
    print("Создайте файл data_light.json в папке lab_python_fp со следующим содержимым:")
    print("""
[
    {"job-name": "Программист Python", "salary": 150000},
    {"job-name": "Программист Java", "salary": 140000},
    {"job-name": "Аналитик данных", "salary": 120000},
    {"job-name": "Программист C++", "salary": 160000},
    {"job-name": "Дизайнер", "salary": 80000},
    {"job-name": "программист JavaScript", "salary": 130000},
    {"job-name": "Менеджер проекта", "salary": 110000},
    {"job-name": "Программист Python", "salary": 155000}
]
""")
    # Используем тестовые данные для демонстрации
    data = [
        {"job-name": "Программист Python", "salary": 150000},
        {"job-name": "Программист Java", "salary": 140000},
        {"job-name": "Аналитик данных", "salary": 120000},
        {"job-name": "Программист C++", "salary": 160000},
        {"job-name": "Дизайнер", "salary": 80000},
        {"job-name": "программист JavaScript", "salary": 130000},
        {"job-name": "Менеджер проекта", "salary": 110000},
        {"job-name": "Программист Python", "salary": 155000}
    ]
    print("Используются тестовые данные из кода.")

@print_result
def f1(arg):
    return sorted(list(Unique(field(arg, 'job-name'), ignore_case=True)), key=lambda x: x.lower())

@print_result
def f2(arg):
    return list(filter(lambda x: x.lower().startswith('программист'), arg))

@print_result
def f3(arg):
    return list(map(lambda x: f"{x} с опытом Python", arg))

@print_result
def f4(arg):
    salaries = list(gen_random(len(arg), 100000, 200000))
    return [f"{prof}, зарплата {salary} руб." for prof, salary in zip(arg, salaries)]


if __name__ == '__main__':
    print("\nЗапуск цепочки функций...")
    with cm_timer_1():
        result = f4(f3(f2(f1(data))))
    print("\nОбработка завершена!")
