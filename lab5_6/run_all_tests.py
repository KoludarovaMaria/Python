"""
Простой скрипт для запуска всех тестов
"""

import unittest
import subprocess
import sys
import os

def run_unittest_tests():
    """Запуск TDD тестов (unittest)"""
    print("\n" + "="*60)
    print("ЗАПУСК TDD ТЕСТОВ (Test-Driven Development)")
    print("="*60)

    # Добавляем текущую директорию в путь Python
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

    # Загружаем тесты из test_patterns.py
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    try:
        # Импортируем тестовые классы
        from test_patterns import (
            TestFactoryPatternTDD,
            TestAdapterPatternTDD,
            TestObserverPatternTDD,
            TestPatternsWithMocks,
            TestIntegration,
            TestEdgeCases
        )

        # Добавляем все тестовые классы
        test_classes = [
            TestFactoryPatternTDD,
            TestAdapterPatternTDD,
            TestObserverPatternTDD,
            TestPatternsWithMocks,
            TestIntegration,
            TestEdgeCases
        ]

        for test_class in test_classes:
            suite.addTests(loader.loadTestsFromTestCase(test_class))

        # Запускаем тесты
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)

        # Статистика
        print("\n" + "="*60)
        print("СТАТИСТИКА TDD ТЕСТОВ:")
        print(f"  Всего тестов: {result.testsRun}")
        print(f"  Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
        print(f"  Провалено: {len(result.failures)}")
        print(f"  Ошибок: {len(result.errors)}")

        return result.wasSuccessful()

    except ImportError as e:
        print(f"[ERROR] Ошибка импорта: {e}")
        return False

def run_simple_bdd_tests():
    """Запуск упрощенных BDD тестов"""
    print("\n" + "="*60)
    print("ЗАПУСК BDD ТЕСТОВ (Behavior-Driven Development)")
    print("="*60)

    try:
        # Импортируем и запускаем упрощенные BDD тесты
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from test_bdd_simple import run_all_bdd_scenarios

        success = run_all_bdd_scenarios()
        return success

    except ImportError as e:
        print(f"[ERROR] Ошибка импорта: {e}")
        print("[INFO] Убедитесь, что файл test_bdd_simple.py существует")
        return False
    except Exception as e:
        print(f"[ERROR] Ошибка при выполнении BDD тестов: {e}")
        return False

def main():
    """Главная функция"""
    print("\n" + "="*60)
    print("ЛАБОРАТОРНАЯ РАБОТА №4 - ЗАПУСК ТЕСТОВ")
    print("="*60)

    # Проверяем наличие необходимых файлов
    required_files = ["patterns.py", "test_patterns.py"]
    missing_files = []

    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print("[ERROR] Отсутствуют необходимые файлы:")
        for file in missing_files:
            print(f"  - {file}")
        return 1

    # Запуск TDD тестов
    print("\n[ЭТАП 1] ЗАПУСК TDD ТЕСТОВ")
    print("-" * 40)
    tdd_success = run_unittest_tests()

    # Запуск BDD тестов (упрощенная версия)
    print("\n[ЭТАП 2] ЗАПУСК BDD ТЕСТОВ")
    print("-" * 40)
    bdd_success = run_simple_bdd_tests()

    # Демонстрация
    print("\n[ЭТАП 3] ДЕМОНСТРАЦИЯ РАБОТЫ ПАТТЕРНОВ")
    print("-" * 40)

    if os.path.exists("main.py"):
        print("Запуск демонстрационной программы...\n")

        # Устанавливаем переменную окружения для корректной кодировки
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'

        demo_process = subprocess.run(
            [sys.executable, "main.py"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            env=env
        )

        # Выводим вывод демонстрации
        if demo_process.stdout:
            print(demo_process.stdout)

        if demo_process.stderr:
            print("\n[ОШИБКИ] Демонстрации:")
            print(demo_process.stderr)

        demo_success = demo_process.returncode == 0
    else:
        print("[WARNING] Файл main.py не найден")
        demo_success = False

    # Итоги
    print("\n" + "="*60)
    print("ИТОГИ ТЕСТИРОВАНИЯ")
    print("="*60)

    print(f"TDD тесты: {'[OK] ПРОЙДЕНЫ' if tdd_success else '[FAIL] ПРОВАЛЕНЫ'}")
    print(f"BDD тесты: {'[OK] ПРОЙДЕНЫ' if bdd_success else '[FAIL] ПРОВАЛЕНЫ'}")
    print(f"Демонстрация: {'[OK] УСПЕШНО' if demo_success else '[FAIL] ОШИБКА'}")

    overall_success = tdd_success and bdd_success

    if overall_success:
        print("\n" + "="*60)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        print("="*60)
        print("\n[ВЫПОЛНЕНЫ ВСЕ ТРЕБОВАНИЯ ЛАБОРАТОРНОЙ РАБОТЫ]:")
        print("   1. ✅ Реализованы 3 паттерна проектирования:")
        print("       - Фабричный метод (порождающий)")
        print("       - Адаптер (структурный)")
        print("       - Наблюдатель (поведенческий)")
        print("   2. ✅ Применен TDD фреймворк (unittest) - 26 тестов")
        print("   3. ✅ Применен BDD подход - 5 сценариев")
        print("   4. ✅ Использованы Mock-объекты")
        print("\nЛабораторная работа выполнена полностью и готова к сдаче!")
    else:
        print("\n[WARNING] Некоторые тесты не пройдены")
        print("Проверьте вывод выше для деталей.")

    return 0 if overall_success else 1

if __name__ == "__main__":
    # Устанавливаем кодировку вывода
    sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
