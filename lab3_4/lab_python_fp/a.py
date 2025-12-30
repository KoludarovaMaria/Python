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

# Путь к файлу данных
current_dir = os.path.dirname(__file__)
path = os.path.join(current_dir, 'data_light.json')

print(f"Ищем файл по пути: {path}")

# Проверяем и создаем файл если нужно
if not os.path.exists(path) or os.path.getsize(path) == 0:
    print("Файл не найден или пустой. Создаем новый...")

    # Данные для записи
    default_data = [
        {"job-name": "Инженер", "salary": 80000, "city": "Москва"},
        {"job-name": "Программист Java", "salary": 120000, "city": "Санкт-Петербург"},
        {"job-name": "Аналитик данных", "salary": 90000, "city": "Новосибирск"},
        {"job-name": "Программист Python", "salary": 150000, "city": "Москва"},
        {"job-name": "Веб-разработчик", "salary": 110000, "city": "Казань"},
        {"job-name": "Программист C++", "salary": 140000, "city": "Екатеринбург"},
        {"job-name": "Дизайнер", "salary": 70000, "city": "Москва"},
        {"job-name": "Системный администратор", "salary": 85000, "city": "Санкт-Петербург"},
        {"job-name": "программист JavaScript", "salary": 130000, "city": "Новосибирск"},
        {"job-name": "Менеджер проекта", "salary": 95000, "city": "Москва"}
    ]

    # Записываем данные в файл
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(default_data, f, ensure_ascii=False, indent=2)

    print(f"Создан файл с {len(default_data)} записями")
    data = default_data
else:
    # Загружаем данные из файла
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        print(f"Успешно загружено {len(data)} записей из data_light.json")
    except json.JSONDecodeError as e:
        print(f"Ошибка в формате JSON: {e}")
        print("Создаем новые данные...")
        data = [
            {"job-name": "Программист Python", "salary": 150000, "city": "Москва"},
            {"job-name": "Программист Java", "salary": 140000, "city": "Санкт-Петербург"},
            {"job-name": "Аналитик данных", "salary": 120000, "city": "Новосибирск"},
            {"job-name": "Дизайнер", "salary": 80000, "city": "Москва"},
            {"job-name": "программист JavaScript", "salary": 130000, "city": "Новосибирск"}
        ]

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
    print("\nРезультат:")
    for item in result:
        print(item)
