"""
Лабораторная работа №4
Демонстрация шаблонов проектирования
"""

from patterns import (
    NotificationFactory,
    EmailNotification,
    SMSNotification,
    PushNotification,
    LegacyBankSystem,
    BankSystemAdapter,
    BankTransaction,
    TransactionLogger,
    FraudDetector,
    NotificationService
)

def print_separator(title: str):
    """Печатает разделитель с заголовком"""
    print("\n" + "=" * 60)
    print(f" {title} ")
    print("=" * 60)

def demonstrate_factory_pattern():
    """Демонстрация фабричного метода"""
    print_separator("ФАБРИЧНЫЙ МЕТОД")

    factory = NotificationFactory()

    # Создаем разные типы уведомлений через фабрику
    notifications = [
        factory.create_notification("email"),
        factory.create_notification("sms"),
        factory.create_notification("push")
    ]

    # Отправляем уведомления
    messages = [
        "Ваш платеж на 1000 руб. выполнен успешно",
        "Код подтверждения: 123456",
        "У вас новое сообщение в приложении"
    ]

    for i, notification in enumerate(notifications):
        result = notification.send(messages[i])
        print(f"{i+1}. {result}")

    # Показываем типы объектов
    print("\nТипы созданных объектов:")
    for notification in notifications:
        print(f"  - {type(notification).__name__}")

def demonstrate_adapter_pattern():
    """Демонстрация адаптера"""
    print_separator("АДАПТЕР")

    # Создаем старую систему
    legacy_system = LegacyBankSystem()
    print("Создана старая банковская система")

    # Создаем адаптер
    adapter = BankSystemAdapter(legacy_system)
    print("Создан адаптер для интеграции с новой системой")

    # Тестируем адаптер с разными сообщениями
    test_messages = [
        "Оплата услуг ЖКХ",
        "Перевод между счетами",
        "Ошибка авторизации",
        "Блокировка карты",
        "Информационное сообщение"
    ]

    print("\nТестирование адаптера:")
    for i, message in enumerate(test_messages):
        result = adapter.send(message)
        print(f"{i+1}. Сообщение: '{message}'")
        print(f"   Результат: {result}")

def demonstrate_observer_pattern():
    """Демонстрация наблюдателя"""
    print_separator("НАБЛЮДАТЕЛЬ")

    # Создаем фабрику для сервиса уведомлений
    factory = NotificationFactory()

    # Создаем наблюдателей
    logger = TransactionLogger()
    fraud_detector = FraudDetector(threshold=50000)  # Порог 50,000 руб.
    notification_service = NotificationService(factory)

    print("Созданы наблюдатели:")
    print("  1. TransactionLogger - логирует все транзакции")
    print("  2. FraudDetector - обнаруживает подозрительные операции")
    print("  3. NotificationService - отправляет уведомления клиентам")

    # Сценарий 1: Нормальная транзакция
    print("\n[СЦЕНАРИЙ 1] Нормальная транзакция")
    print("-" * 40)

    transaction1 = BankTransaction("TRX-001", "Иванов И.И.")
    transaction1.attach(logger)
    transaction1.attach(fraud_detector)
    transaction1.attach(notification_service)

    print("Создана транзакция TRX-001 от Иванова И.И.")
    print("Прикреплены все наблюдатели")

    transaction_data = transaction1.process_transaction(25000, "Петров П.П.")
    print(f"\nТранзакция выполнена: {transaction_data['amount']} руб. -> {transaction_data['recipient']}")

    # Получаем результаты от наблюдателей
    log_result = logger.update(transaction_data)
    fraud_result = fraud_detector.update(transaction_data)
    notification_result = notification_service.update(transaction_data)

    print("\nРеакция наблюдателей:")
    print(f"1. {log_result}")
    print(f"2. {fraud_result if fraud_result else '[БЕЗОПАСНО] Сумма в пределах нормы'}")
    print(f"3. {notification_result}")

    # Сценарий 2: Подозрительная транзакция
    print("\n[СЦЕНАРИЙ 2] Подозрительная транзакция")
    print("-" * 40)

    transaction2 = BankTransaction("TRX-002", "Сидоров С.С.")
    transaction2.attach(logger)
    transaction2.attach(fraud_detector)
    transaction2.attach(notification_service)

    print("Создана транзакция TRX-002 от Сидорова С.С.")

    transaction_data2 = transaction2.process_transaction(150000, "Неизвестный получатель")
    print(f"\nТранзакция выполнена: {transaction_data2['amount']} руб. -> {transaction_data2['recipient']}")

    # Получаем результаты от наблюдателей
    log_result2 = logger.update(transaction_data2)
    fraud_result2 = fraud_detector.update(transaction_data2)
    notification_result2 = notification_service.update(transaction_data2)

    print("\nРеакция наблюдателей:")
    print(f"1. {log_result2}")
    print(f"2. {fraud_result2}")
    print(f"3. {notification_result2}")

    # Сценарий 3: Отмена транзакции
    print("\n[СЦЕНАРИЙ 3] Отмена транзакции")
    print("-" * 40)

    transaction3 = BankTransaction("TRX-003", "Кузнецов К.К.")
    transaction3.attach(logger)
    transaction3.attach(notification_service)  # Не прикрепляем детектор мошенничества

    print("Создана транзакция TRX-003 от Кузнецова К.К.")
    print("Прикреплены только логгер и сервис уведомлений")

    # Сначала обрабатываем, потом отменяем
    transaction3.process_transaction(30000, "Смирнов С.С.")
    cancel_data = transaction3.cancel_transaction()

    print("\nТранзакция отменена")

    log_result3 = logger.update(cancel_data)
    notification_result3 = notification_service.update(cancel_data)

    print("\nРеакция наблюдателей:")
    print(f"1. {log_result3}")
    print(f"2. {notification_result3}")

def demonstrate_integration():
    """Демонстрация интеграции всех паттернов"""
    print_separator("ИНТЕГРАЦИЯ ВСЕХ ПАТТЕРНОВ")

    print("Создаем комплексную систему банковских уведомлений...\n")

    # 1. Используем фабрику для создания уведомлений
    factory = NotificationFactory()

    # 2. Используем адаптер для интеграции со старой системой
    legacy_system = LegacyBankSystem()
    adapter = BankSystemAdapter(legacy_system)

    # 3. Создаем наблюдателей
    logger = TransactionLogger()
    fraud_detector = FraudDetector(threshold=75000)
    notification_service = NotificationService(factory)

    # 4. Создаем транзакцию и прикрепляем наблюдателей
    transaction = BankTransaction("TRX-INT-001", "Банк Москвы")
    transaction.attach(logger)
    transaction.attach(fraud_detector)
    transaction.attach(notification_service)

    print("[OK] Система инициализирована")
    print("   - Фабрика уведомлений: создает email/sms/push")
    print("   - Адаптер: интегрирует со старой банковской системой")
    print("   - Наблюдатели: 3 компонента следят за транзакциями")

    # Выполняем транзакцию
    print("\n[ВЫПОЛНЕНИЕ] Выполняем транзакцию...")
    transaction_data = transaction.process_transaction(
        120000,
        "ООО 'ТехноПрофи'"
    )

    print(f"\n[РЕЗУЛЬТАТЫ] Транзакции:")
    print(f"   ID: {transaction_data['id']}")
    print(f"   Сумма: {transaction_data['amount']} руб.")
    print(f"   Получатель: {transaction_data['recipient']}")
    print(f"   Статус: {transaction_data['status']}")

    # Демонстрируем работу адаптера
    print("\n[АДАПТЕР] Отправляем уведомление через адаптер старой системы...")
    alert_result = adapter.send(f"Крупный перевод: {transaction_data['amount']} руб.")
    print(f"   Результат: {alert_result}")

    print("\n[УСПЕХ] Все паттерны успешно интегрированы и работают вместе!")

def main():
    """Главная функция"""
    print("\n" + "=" * 60)
    print("ЛАБОРАТОРНАЯ РАБОТА №4")
    print("ШАБЛОНЫ ПРОЕКТИРОВАНИЯ В PYTHON")
    print("=" * 60)
    print("Реализованные паттерны:")
    print("  1. Фабричный метод (порождающий)")
    print("  2. Адаптер (структурный)")
    print("  3. Наблюдатель (поведенческий)")
    print("=" * 60)

    # Демонстрация каждого паттерна отдельно
    demonstrate_factory_pattern()
    demonstrate_adapter_pattern()
    demonstrate_observer_pattern()

    # Демонстрация интеграции
    demonstrate_integration()

    print("\n" + "=" * 60)
    print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)

if __name__ == "__main__":
    main()
