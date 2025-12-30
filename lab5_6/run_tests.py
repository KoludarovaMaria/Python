"""
Скрипт для запуска всех тестов лабораторной работы
"""

import subprocess
import sys
import os
import time

def print_header(text):
    """Печать заголовка"""
    print("\n" + "="*80)
    print(f" {text} ")
    print("="*80)

def run_command(command, description):
    """Выполнение команды с выводом результата"""
    print(f"\n🚀 {description}...")
    print(f"   Команда: {command}")

    start_time = time.time()

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )

        elapsed_time = time.time() - start_time

        if result.returncode == 0:
            print(f"✅ Успешно завершено за {elapsed_time:.2f} сек")
            if result.stdout:
                print("\nВывод:")
                print(result.stdout[:500])  # Первые 500 символов вывода
        else:
            print(f"❌ Завершено с ошибкой за {elapsed_time:.2f} сек")
            print(f"Код возврата: {result.returncode}")
            if result.stderr:
                print("\nОшибки:")
                print(result.stderr)

        return result.returncode

    except Exception as e:
        print(f"❌ Ошибка при выполнении: {e}")
        return 1

def main():
    """Главная функция"""
    print_header("ЛАБОРАТОРНАЯ РАБОТА №4 - ЗАПУСК ТЕСТОВ")

    # Проверяем, что мы в правильной директории
    if not os.path.exists("patterns.py"):
        print("❌ Ошибка: Файл patterns.py не найден!")
        print("   Запустите скрипт из директории с файлами лабораторной работы")
        return 1

    # Устанавливаем зависимости
    print_header("УСТАНОВКА ЗАВИСИМОСТЕЙ")

    install_result = run_command(
        "pip install -r requirements.txt",
        "Установка зависимостей из requirements.txt"
    )

    if install_result != 0:
        print("⚠️  Предупреждение: Возможны проблемы с зависимостями")

    # Запуск TDD тестов
    print_header("TDD ТЕСТИРОВАНИЕ")

    tdd_result = run_command(
        "python -m pytest test_patterns.py -v",
        "Запуск TDD тестов"
    )

    # Запуск BDD тестов
    print_header("BDD ТЕСТИРОВАНИЕ")

    bdd_result = run_command(
        "python -m pytest test_bdd.py -v",
        "Запуск BDD тестов"
    )

    # Запуск тестов с генерацией HTML отчета
    print_header("ГЕНЕРАЦИЯ ОТЧЕТА")

    report_result = run_command(
        "python -m pytest test_patterns.py test_bdd.py --html=test_report.html --self-contained-html",
        "Генерация HTML отчета"
    )

    # Запуск демонстрации
    print_header("ДЕМОНСТРАЦИЯ РАБОТЫ ПАТТЕРНОВ")

    demo_result = run_command(
        "python main.py",
        "Запуск демонстрационной программы"
    )

    # Итоги
    print_header("ИТОГИ ТЕСТИРОВАНИЯ")

    results = {
        "TDD тесты": "✅ ПРОЙДЕНЫ" if tdd_result == 0 else "❌ ПРОВАЛЕНЫ",
        "BDD тесты": "✅ ПРОЙДЕНЫ" if bdd_result == 0 else "❌ ПРОВАЛЕНЫ",
        "Демонстрация": "✅ УСПЕШНО" if demo_result == 0 else "❌ ОШИБКА"
    }

    for test_type, status in results.items():
        print(f"  {test_type}: {status}")

    # Проверяем покрытие кода (если установлен pytest-cov)
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            if "pytest-cov" in f.read():
                print_header("АНАЛИЗ ПОКРЫТИЯ КОДА")

                coverage_result = run_command(
                    "python -m pytest --cov=patterns --cov-report=html --cov-report=term",
                    "Анализ покрытия кода"
                )

                if coverage_result == 0:
                    print("\n📊 Отчет о покрытии сохранен в директории htmlcov/")

    print_header("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")

    # Возвращаем общий результат
    overall_result = 0 if all(r == 0 for r in [tdd_result, bdd_result]) else 1

    if overall_result == 0:
        print("🎉 Все тесты пройдены успешно!")
        print("📄 Отчет сохранен в test_report.html")
    else:
        print("⚠️  Некоторые тесты не пройдены")
        print("   Проверьте вывод выше для деталей")

    return overall_result

if __name__ == "__main__":
    sys.exit(main())
