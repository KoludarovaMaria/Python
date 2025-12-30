from operator import itemgetter


class Street:
    """Улица"""

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __repr__(self):
        return f"Street(id={self.id}, name='{self.name}')"


class House:
    """Дом"""

    def __init__(self, id, address, residents_count, street_id):
        self.id = id
        self.address = address
        self.residents_count = residents_count
        self.street_id = street_id

    def __repr__(self):
        return f"House(id={self.id}, address='{self.address}', residents={self.residents_count}, street_id={self.street_id})"


class StreetHouse:
    """Связь многие-ко-многим между домами и улицами"""

    def __init__(self, street_id, house_id):
        self.street_id = street_id
        self.house_id = house_id

    def __repr__(self):
        return f"StreetHouse(street_id={self.street_id}, house_id={self.house_id})"


# Данные для тестирования (можно заменить на загрузку из БД или файла)
def create_test_data():
    """Создание тестовых данных"""

    # Улицы
    streets = [
        Street(1, 'Арбат'),
        Street(2, 'Бауманская'),
        Street(3, 'Авиамоторная'),
        Street(4, 'Волгоградский проспект'),
        Street(5, 'Академическая'),
    ]

    # Дома
    houses = [
        House(1, 'Арбат, 1', 150, 1),
        House(2, 'Арбат, 15', 200, 1),
        House(3, 'Бауманская, 10', 180, 2),
        House(4, 'Авиамоторная, 25', 220, 3),
        House(5, 'Волгоградский пр-т, 100', 300, 4),
        House(6, 'Академическая, 5', 170, 5),
        House(7, 'Академическая, 7', 190, 5),
        House(8, 'Авиамоторная, 30', 210, 3),
    ]

    # Связи многие-ко-многим
    streets_houses = [
        StreetHouse(1, 1),
        StreetHouse(1, 2),
        StreetHouse(2, 3),
        StreetHouse(3, 4),
        StreetHouse(4, 4),  # Угловой дом на двух улицах
        StreetHouse(4, 5),
        StreetHouse(5, 6),
        StreetHouse(5, 7),
        StreetHouse(3, 8),
        StreetHouse(5, 8),  # Угловой дом на двух улицах
    ]

    return streets, houses, streets_houses


def create_one_to_many(streets, houses):
    """Создание соединения один-ко-многим"""
    one_to_many = [(h.address, h.residents_count, s.name)
                   for s in streets
                   for h in houses
                   if h.street_id == s.id]
    return one_to_many


def create_many_to_many(streets, houses, streets_houses):
    """Создание соединения многие-ко-многим"""
    many_to_many_temp = [(s.name, sh.street_id, sh.house_id)
                         for s in streets
                         for sh in streets_houses
                         if s.id == sh.street_id]

    many_to_many = [(h.address, h.residents_count, street_name)
                    for street_name, street_id, house_id in many_to_many_temp
                    for h in houses if h.id == house_id]
    return many_to_many


def task1(one_to_many):
    """Задание Д1: дома с адресом, оканчивающимся на '15'"""
    result = list(filter(lambda i: i[0].endswith('15'), one_to_many))
    return result


def task2(one_to_many, streets):
    """Задание Д2: улицы со средним количеством жителей"""
    result_unsorted = []
    for s in streets:
        # Список домов на улице
        s_houses = list(filter(lambda i: i[2] == s.name, one_to_many))
        if len(s_houses) > 0:
            # Количество жителей в домах
            s_residents = [residents for _, residents, _ in s_houses]
            # Среднее количество жителей
            avg_residents = sum(s_residents) / len(s_residents)
            result_unsorted.append((s.name, round(avg_residents, 1)))

    result = sorted(result_unsorted, key=itemgetter(1))
    return result


def task3(many_to_many, streets):
    """Задание Д3: улицы на 'А' и дома на них"""
    result = {}
    for s in streets:
        if s.name.startswith('А'):
            # Список домов на улице (многие-ко-многим)
            s_houses = list(filter(lambda i: i[2] == s.name, many_to_many))
            # Адреса домов (убираем дубликаты)
            s_addresses = list(set([address for address, _, _ in s_houses]))
            result[s.name] = s_addresses
    return result


def print_results(result1, result2, result3):
    """Вывод результатов в консоль"""
    print('Задание Д1')
    print("Список домов с адресом, оканчивающимся на '15', и их улицы:")
    for item in result1:
        print(f"  {item[0]} -> {item[2]}")

    print('\nЗадание Д2')
    print("Список улиц со средним количеством жителей в домах, отсортированный по среднему количеству:")
    for item in result2:
        print(f"  {item[0]}: {item[1]} жителей")

    print('\nЗадание Д3')
    print("Улицы, название которых начинается с 'А', и дома на них:")
    for street_name, houses_list in result3.items():
        print(f"  {street_name}:")
        for address in houses_list:
            print(f"    - {address}")


def main():
    """Основная функция для запуска программы"""
    streets, houses, streets_houses = create_test_data()
    one_to_many = create_one_to_many(streets, houses)
    many_to_many = create_many_to_many(streets, houses, streets_houses)

    result1 = task1(one_to_many)
    result2 = task2(one_to_many, streets)
    result3 = task3(many_to_many, streets)

    print_results(result1, result2, result3)


if __name__ == '__main__':
    main()
