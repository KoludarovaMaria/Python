

import unittest
from houses_streets import (
    Street, House, StreetHouse,
    create_test_data, create_one_to_many, create_many_to_many,
    task1, task2, task3
)


class TestHousesStreets(unittest.TestCase):
    """Класс для тестирования функций работы с домами и улицами"""

    def setUp(self):
        """Подготовка тестовых данных перед каждым тестом"""
        self.streets, self.houses, self.streets_houses = create_test_data()
        self.one_to_many = create_one_to_many(self.streets, self.houses)
        self.many_to_many = create_many_to_many(
            self.streets, self.houses, self.streets_houses
        )

    # Тест 1: Проверка создания тестовых данных
    def test_create_test_data(self):
        """Тест создания тестовых данных"""
        # Проверяем количество созданных объектов
        self.assertEqual(len(self.streets), 5)
        self.assertEqual(len(self.houses), 8)
        self.assertEqual(len(self.streets_houses), 10)

        # Проверяем корректность данных улиц
        street_names = [s.name for s in self.streets]
        self.assertIn('Арбат', street_names)
        self.assertIn('Авиамоторная', street_names)

        # Проверяем корректность данных домов
        house_addresses = [h.address for h in self.houses]
        self.assertIn('Арбат, 1', house_addresses)
        self.assertIn('Арбат, 15', house_addresses)

    # Тест 2: Проверка задания Д1 (дома с адресом на '15')
    def test_task1_houses_ending_with_15(self):
        """Тест поиска домов с адресом, оканчивающимся на '15'"""
        result = task1(self.one_to_many)

        # Проверяем, что найден только один дом
        self.assertEqual(len(result), 1)

        # Проверяем корректность найденного дома
        address, residents, street = result[0]
        self.assertEqual(address, 'Арбат, 15')
        self.assertEqual(residents, 200)
        self.assertEqual(street, 'Арбат')

        # Проверяем, что другие дома не попали в результат
        addresses = [item[0] for item in result]
        self.assertNotIn('Арбат, 1', addresses)
        self.assertNotIn('Бауманская, 10', addresses)

    # Тест 3: Проверка задания Д2 (среднее количество жителей по улицам)
    def test_task2_average_residents(self):
        """Тест вычисления среднего количества жителей по улицам"""
        result = task2(self.one_to_many, self.streets)

        # Проверяем количество улиц в результате
        self.assertEqual(len(result), 5)

        # Проверяем сортировку по возрастанию
        for i in range(len(result) - 1):
            self.assertLessEqual(result[i][1], result[i + 1][1])

        # Проверяем конкретные значения
        result_dict = dict(result)

        # Проверяем улицу Арбат: (150 + 200) / 2 = 175
        self.assertEqual(result_dict['Арбат'], 175.0)

        # Проверяем улицу Бауманская: 180 / 1 = 180
        self.assertEqual(result_dict['Бауманская'], 180.0)

        # Проверяем улицу Авиамоторная: (220 + 210) / 2 = 215
        self.assertEqual(result_dict['Авиамоторная'], 215.0)

    # Тест 4: Проверка задания Д3 (улицы на 'А' и их дома)
    def test_task3_streets_starting_with_A(self):
        """Тест поиска улиц, начинающихся с 'А', и их домов"""
        result = task3(self.many_to_many, self.streets)

        # Проверяем количество улиц на 'А'
        self.assertEqual(len(result), 3)

        # Проверяем наличие всех улиц на 'А'
        self.assertIn('Арбат', result)
        self.assertIn('Авиамоторная', result)
        self.assertIn('Академическая', result)

        # Проверяем отсутствие улиц не на 'А'
        self.assertNotIn('Бауманская', result)
        self.assertNotIn('Волгоградский проспект', result)

        # Проверяем дома на улице Арбат
        arbat_houses = result['Арбат']
        self.assertEqual(len(arbat_houses), 2)
        self.assertIn('Арбат, 1', arbat_houses)
        self.assertIn('Арбат, 15', arbat_houses)

        # Проверяем, что угловой дом Авиамоторная, 30 есть на двух улицах
        self.assertIn('Авиамоторная, 30', result['Авиамоторная'])
        self.assertIn('Авиамоторная, 30', result['Академическая'])

    # Тест 5: Проверка создания соединения один-ко-многим
    def test_create_one_to_many(self):
        """Тест создания связи один-ко-многим"""
        one_to_many = self.one_to_many

        # Проверяем количество связей
        self.assertEqual(len(one_to_many), 8)  # 8 домов

        # Проверяем структуру данных
        for address, residents, street in one_to_many:
            self.assertIsInstance(address, str)
            self.assertIsInstance(residents, int)
            self.assertIsInstance(street, str)

            # Проверяем, что количество жителей положительное
            self.assertGreater(residents, 0)

    # Тест 6: Проверка создания соединения многие-ко-многим
    def test_create_many_to_many(self):
        """Тест создания связи многие-ко-многим"""
        many_to_many = self.many_to_many

        # Проверяем количество связей (больше чем домов из-за угловых домов)
        self.assertEqual(len(many_to_many), 10)  # 10 связей

        # Проверяем структуру данных
        for address, residents, street in many_to_many:
            self.assertIsInstance(address, str)
            self.assertIsInstance(residents, int)
            self.assertIsInstance(street, str)

            # Проверяем, что количество жителей положительное
            self.assertGreater(residents, 0)

        # Проверяем, что угловой дом встречается несколько раз
        addresses = [item[0] for item in many_to_many]
        self.assertEqual(addresses.count('Авиамоторная, 25'), 2)  # На двух улицах
        self.assertEqual(addresses.count('Авиамоторная, 30'), 2)  # На двух улицах


if __name__ == '__main__':

    unittest.main(verbosity=2)
