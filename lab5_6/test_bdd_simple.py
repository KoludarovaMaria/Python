"""
Упрощенные BDD тесты без сложных зависимостей
"""

import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from patterns import (
    NotificationFactory,
    EmailNotification,
    SMSNotification,
    BankSystemAdapter,
    LegacyBankSystem,
    BankTransaction,
    TransactionLogger,
    FraudDetector
)

def test_scenario_1():
    """Сценарий 1: Создание email уведомления через фабрику"""
    print("\n📋 Сценарий 1: Создание email уведомления")
    print("-" * 40)

    # Given: У меня есть фабрика уведомлений
    factory = NotificationFactory()
    print("✅ Given: У меня есть фабрика уведомлений")

    # When: Я создаю уведомление типа "email"
    notification = factory.create_notification("email")
    print("✅ When: Я создаю уведомление типа 'email'")

    # Then: Я должен получить уведомление типа EmailNotification
    assert isinstance(notification, EmailNotification)
    print("✅ Then: Я получил уведомление типа EmailNotification")

    # And: Я могу отправить сообщение
    result = notification.send("Тестовое сообщение")
    print(f"✅ And: Я отправил сообщение, результат: '{result[:30]}...'")

    assert "Отправка email" in result
    print("✅ And: Результат содержит 'Отправка email'")

    return True

def test_scenario_2():
    """Сценарий 2: Создание SMS уведомления"""
    print("\n📋 Сценарий 2: Создание SMS уведомления")
    print("-" * 40)

    # Given
    factory = NotificationFactory()
    print("✅ Given: У меня есть фабрика уведомлений")

    # When
    notification = factory.create_notification("sms")
    print("✅ When: Я создаю уведомление типа 'sms'")

    # Then
    assert isinstance(notification, SMSNotification)
    print("✅ Then: Я получил уведомление типа SMSNotification")

    result = notification.send("Код: 1234")
    print(f"✅ And: Результат: '{result}'")

    assert "Отправка SMS" in result
    return True

def test_scenario_3():
    """Сценарий 3: Адаптер для старой системы"""
    print("\n📋 Сценарий 3: Использование адаптера")
    print("-" * 40)

    # Given: У меня есть старая банковская система
    legacy_system = LegacyBankSystem()
    print("✅ Given: У меня есть старая банковская система")

    # And: Я создаю адаптер
    adapter = BankSystemAdapter(legacy_system)
    print("✅ And: Я создаю адаптер для старой системы")

    # When: Я отправляю сообщение через адаптер
    result = adapter.send("оплата услуг")
    print(f"✅ When: Я отправляю 'оплата услуг', результат: '{result}'")

    # Then: Я должен получить результат в формате старой системы
    assert result.startswith("[Код")
    print("✅ Then: Результат в формате старой системы")

    # And: Результат должен содержать код 100
    assert "[Код 100]" in result
    print("✅ And: Результат содержит код 100")

    return True

def test_scenario_4():
    """Сценарий 4: Наблюдатель за транзакциями"""
    print("\n📋 Сценарий 4: Транзакция с наблюдателями")
    print("-" * 40)

    # Given: Я создаю банковскую транзакцию
    transaction = BankTransaction("TRX-BDD-001", "Иванов И.И.")
    print("✅ Given: Я создал транзакцию TRX-BDD-001")

    # And: К транзакции прикреплены наблюдатели
    logger = TransactionLogger()
    detector = FraudDetector(threshold=50000)

    transaction.attach(logger)
    transaction.attach(detector)
    print("✅ And: К транзакции прикреплены логгер и детектор мошенничества")

    # When: Я обрабатываю транзакцию
    transaction_data = transaction.process_transaction(30000, "Петров П.П.")
    print("✅ When: Я обрабатываю транзакцию на 30000 руб.")

    # Then: Транзакция должна быть completed
    assert transaction.status == "completed"
    print("✅ Then: Транзакция completed")

    # And: Логгер должен записать информацию
    log_result = logger.update(transaction_data)
    assert "ЛОГ: Транзакция" in log_result
    print(f"✅ And: Логгер записал: '{log_result[:40]}...'")

    # And: Не должно быть предупреждения о мошенничестве
    fraud_result = detector.update(transaction_data)
    assert fraud_result == ""
    print("✅ And: Предупреждения о мошенничестве нет")

    return True

def test_scenario_5():
    """Сценарий 5: Обнаружение мошенничества"""
    print("\n📋 Сценарий 5: Подозрительная транзакция")
    print("-" * 40)

    # Given
    transaction = BankTransaction("TRX-BDD-002", "Сидоров С.С.")
    logger = TransactionLogger()
    detector = FraudDetector(threshold=50000)

    transaction.attach(logger)
    transaction.attach(detector)
    print("✅ Given: Создана транзакция с порогом 50000")

    # When
    transaction_data = transaction.process_transaction(150000, "Неизвестный")
    print("✅ When: Обрабатываю транзакцию на 150000 руб.")

    # Then
    fraud_result = detector.update(transaction_data)
    assert "ВНИМАНИЕ" in fraud_result
    print(f"✅ Then: Обнаружено мошенничество: '{fraud_result[:50]}...'")

    return True

def run_all_bdd_scenarios():
    """Запуск всех BDD сценариев"""
    print("\n" + "="*60)
    print("BDD ТЕСТИРОВАНИЕ (упрощенная версия)")
    print("="*60)

    scenarios = [
        ("Создание email уведомления", test_scenario_1),
        ("Создание SMS уведомления", test_scenario_2),
        ("Использование адаптера", test_scenario_3),
        ("Транзакция с наблюдателями", test_scenario_4),
        ("Обнаружение мошенничества", test_scenario_5)
    ]

    passed = 0
    failed = 0

    for name, test_func in scenarios:
        try:
            print(f"\n🔍 Запуск: {name}")
            if test_func():
                print(f"✅ {name} - ПРОЙДЕН")
                passed += 1
            else:
                print(f"❌ {name} - ПРОВАЛЕН")
                failed += 1
        except AssertionError as e:
            print(f"❌ {name} - ПРОВАЛЕН: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {name} - ОШИБКА: {e}")
            failed += 1

    print("\n" + "="*60)
    print("ИТОГИ BDD ТЕСТИРОВАНИЯ:")
    print(f"  Всего сценариев: {passed + failed}")
    print(f"  Пройдено: {passed}")
    print(f"  Провалено: {failed}")
    print("="*60)

    return failed == 0

if __name__ == "__main__":
    success = run_all_bdd_scenarios()
    sys.exit(0 if success else 1)
