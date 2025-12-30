"""
Лабораторная работа №4
Тестирование шаблонов проектирования
TDD, Mock-объекты и интеграционные тесты
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from patterns import (
    NotificationFactory,
    EmailNotification,
    SMSNotification,
    LegacyBankSystem,
    BankSystemAdapter,
    BankTransaction,
    TransactionLogger,
    FraudDetector,
    NotificationService
)

# ==================== TDD ТЕСТЫ ====================
class TestFactoryPatternTDD(unittest.TestCase):
    """TDD тесты для фабричного метода"""

    def setUp(self):
        """Подготовка перед каждым тестом"""
        self.factory = NotificationFactory()

    def test_create_email_notification(self):
        """Тест создания email уведомления"""
        notification = self.factory.create_notification("email")
        self.assertIsInstance(notification, EmailNotification)

    def test_create_sms_notification(self):
        """Тест создания SMS уведомления"""
        notification = self.factory.create_notification("sms")
        self.assertIsInstance(notification, SMSNotification)

    def test_email_notification_send(self):
        """Тест отправки email"""
        notification = self.factory.create_notification("email")
        result = notification.send("Тестовое сообщение")
        expected = "📧 Отправка email: Тестовое сообщение"
        self.assertEqual(result, expected)

    def test_sms_notification_send(self):
        """Тест отправки SMS"""
        notification = self.factory.create_notification("sms")
        result = notification.send("Код: 1234")
        expected = "📱 Отправка SMS: Код: 1234"
        self.assertEqual(result, expected)

    def test_invalid_notification_type(self):
        """Тест на неверный тип уведомления"""
        with self.assertRaises(ValueError):
            self.factory.create_notification("telegram")

    def test_factory_returns_different_instances(self):
        """Тест, что фабрика возвращает разные экземпляры"""
        notification1 = self.factory.create_notification("email")
        notification2 = self.factory.create_notification("email")
        self.assertNotEqual(id(notification1), id(notification2))

class TestAdapterPatternTDD(unittest.TestCase):
    """TDD тесты для адаптера"""

    def setUp(self):
        self.legacy_system = LegacyBankSystem()
        self.adapter = BankSystemAdapter(self.legacy_system)

    def test_adapter_creation(self):
        """Тест создания адаптера"""
        self.assertIsInstance(self.adapter, BankSystemAdapter)

    def test_adapter_send_payment(self):
        """Тест отправки оплаты"""
        result = self.adapter.send("Оплата интернета")
        self.assertEqual(result, "[Код 100] Оплата интернета")

    def test_adapter_send_transfer(self):
        """Тест отправки перевода"""
        result = self.adapter.send("Перевод денег другу")
        self.assertEqual(result, "[Код 200] Перевод денег другу")

    def test_adapter_send_error(self):
        """Тест отправки ошибки"""
        result = self.adapter.send("Ошибка в системе")
        self.assertEqual(result, "[Код 300] Ошибка в системе")

    def test_adapter_send_unknown(self):
        """Тест отправки неизвестного типа"""
        result = self.adapter.send("Информация о счете")
        self.assertEqual(result, "[Код 0] Информация о счете")

    def test_adapter_implements_notification_interface(self):
        """Тест, что адаптер реализует интерфейс Notification"""
        self.assertTrue(hasattr(self.adapter, 'send'))
        self.assertTrue(callable(self.adapter.send))

class TestObserverPatternTDD(unittest.TestCase):
    """TDD тесты для паттерна Наблюдатель"""

    def test_transaction_creation(self):
        """Тест создания транзакции"""
        transaction = BankTransaction("TEST-001", "Тестовый отправитель")
        self.assertEqual(transaction.transaction_id, "TEST-001")
        self.assertEqual(transaction.sender, "Тестовый отправитель")
        self.assertEqual(transaction.status, "pending")

    def test_process_transaction(self):
        """Тест обработки транзакции"""
        transaction = BankTransaction("TEST-002", "Отправитель")
        transaction_data = transaction.process_transaction(1000, "Получатель")

        self.assertEqual(transaction.status, "completed")
        self.assertEqual(transaction.amount, 1000)
        self.assertEqual(transaction.recipient, "Получатель")
        self.assertEqual(transaction_data['id'], "TEST-002")
        self.assertEqual(transaction_data['amount'], 1000)
        self.assertEqual(transaction_data['status'], "completed")

    def test_cancel_transaction(self):
        """Тест отмены транзакции"""
        transaction = BankTransaction("TEST-003", "Отправитель")
        transaction.process_transaction(2000, "Получатель")
        cancel_data = transaction.cancel_transaction()

        self.assertEqual(transaction.status, "cancelled")
        self.assertEqual(cancel_data['status'], "cancelled")

    def test_observer_attaching(self):
        """Тест прикрепления наблюдателей"""
        transaction = BankTransaction("TEST-004", "Отправитель")
        logger = TransactionLogger()

        transaction.attach(logger)
        # В реальном коде нужно проверить, что наблюдатель добавлен
        transaction_data = transaction.process_transaction(3000, "Получатель")
        log_result = logger.update(transaction_data)

        self.assertIn("ЛОГ: Транзакция TEST-004", log_result)

    def test_fraud_detector_normal(self):
        """Тест детектора мошенничества (нормальная сумма)"""
        detector = FraudDetector(threshold=50000)
        transaction_data = {
            "id": "TEST-005",
            "sender": "Отправитель",
            "amount": 30000,
            "recipient": "Получатель",
            "status": "completed"
        }

        result = detector.update(transaction_data)
        self.assertEqual(result, "")  # Пустая строка - мошенничества нет

    def test_fraud_detector_suspicious(self):
        """Тест детектора мошенничества (подозрительная сумма)"""
        detector = FraudDetector(threshold=50000)
        transaction_data = {
            "id": "TEST-006",
            "sender": "Отправитель",
            "amount": 80000,
            "recipient": "Получатель",
            "status": "completed"
        }

        result = detector.update(transaction_data)
        self.assertIn("ВНИМАНИЕ! Подозрительная транзакция", result)
        self.assertIn("80000", result)

# ==================== MOCK ТЕСТЫ ====================
class TestPatternsWithMocks(unittest.TestCase):
    """Тесты с использованием Mock объектов"""

    def test_factory_with_mock(self):
        """Тест фабрики с мок-объектом"""
        # Создаем мок-уведомление
        mock_notification = Mock()
        mock_notification.send.return_value = "Mocked result"

        # Патчим фабрику
        with patch.object(NotificationFactory, 'create_notification',
                         return_value=mock_notification):

            factory = NotificationFactory()
            notification = factory.create_notification("email")
            result = notification.send("Test message")

            # Проверяем вызовы
            mock_notification.send.assert_called_once_with("Test message")
            self.assertEqual(result, "Mocked result")

    def test_adapter_with_mock_legacy(self):
        """Тест адаптера с мок-системой"""
        # Создаем мок старой системы
        mock_legacy = Mock()
        mock_legacy.send_alert.return_value = "[Mocked Code] Mocked message"

        # Создаем адаптер с мок-системой
        adapter = BankSystemAdapter(mock_legacy)
        result = adapter.send("оплата")

        # Проверяем вызовы
        mock_legacy.send_alert.assert_called_once_with(100, "оплата")
        self.assertEqual(result, "[Mocked Code] Mocked message")

    def test_observer_with_mocks(self):
        """Тест наблюдателя с мок-объектами"""
        # Создаем транзакцию
        transaction = BankTransaction("MOCK-TRX-001", "Mock Sender")

        # Создаем мок-наблюдателей
        mock_logger = Mock()
        mock_fraud_detector = Mock()

        # Настраиваем возвращаемые значения
        mock_logger.update.return_value = "Mock log"
        mock_fraud_detector.update.return_value = ""

        # Прикрепляем мок-наблюдателей
        transaction.attach(mock_logger)
        transaction.attach(mock_fraud_detector)

        # Выполняем транзакцию
        transaction_data = transaction.process_transaction(5000, "Mock Recipient")

        # Проверяем, что update был вызван на обоих наблюдателях
        mock_logger.update.assert_called_once_with(transaction_data)
        mock_fraud_detector.update.assert_called_once_with(transaction_data)

        # Проверяем аргументы вызова
        call_args = mock_logger.update.call_args[0][0]
        self.assertEqual(call_args["id"], "MOCK-TRX-001")
        self.assertEqual(call_args["amount"], 5000)

    def test_notification_service_with_mock_factory(self):
        """Тест сервиса уведомлений с мок-фабрикой"""
        # Создаем мок-фабрику
        mock_factory = Mock()
        mock_notification = Mock()

        # Настраиваем моки
        mock_factory.create_notification.return_value = mock_notification
        mock_notification.send.return_value = "Mocked notification"

        # Создаем сервис с мок-фабрикой
        service = NotificationService(mock_factory)

        # Тестируем
        transaction_data = {
            "id": "TEST-007",
            "sender": "Отправитель",
            "amount": 10000,
            "recipient": "Получатель",
            "status": "completed"
        }

        result = service.update(transaction_data)

        # Проверяем вызовы
        mock_factory.create_notification.assert_called_once_with("email")
        mock_notification.send.assert_called_once()
        self.assertEqual(result, "Mocked notification")

# ==================== ИНТЕГРАЦИОННЫЕ ТЕСТЫ ====================
class TestIntegration(unittest.TestCase):
    """Интеграционные тесты всех паттернов"""

    def test_complete_workflow(self):
        """Тест полного рабочего процесса"""
        # 1. Создаем фабрику
        factory = NotificationFactory()

        # 2. Создаем адаптер для старой системы
        legacy_system = LegacyBankSystem()
        adapter = BankSystemAdapter(legacy_system)

        # 3. Создаем наблюдателей
        logger = TransactionLogger()
        fraud_detector = FraudDetector(threshold=100000)
        notification_service = NotificationService(factory)

        # 4. Создаем и настраиваем транзакцию
        transaction = BankTransaction("INT-TEST-001", "Интеграционный тест")
        transaction.attach(logger)
        transaction.attach(fraud_detector)
        transaction.attach(notification_service)

        # 5. Выполняем транзакцию
        transaction_data = transaction.process_transaction(
            75000,
            "Тестовый получатель"
        )

        # 6. Проверяем результаты
        self.assertEqual(transaction.status, "completed")

        log_result = logger.update(transaction_data)
        self.assertIn("ЛОГ: Транзакция INT-TEST-001", log_result)

        fraud_result = fraud_detector.update(transaction_data)
        self.assertEqual(fraud_result, "")  # Сумма меньше порога

        # 7. Проверяем адаптер
        alert_result = adapter.send("перевод 75000 руб.")
        self.assertEqual(alert_result, "[Код 200] перевод 75000 руб.")

        print("\n✅ Интеграционный тест пройден успешно!")
        print(f"   Транзакция: {transaction_data}")
        print(f"   Лог: {log_result[:50]}...")
        print(f"   Адаптер: {alert_result}")

# ==================== ТЕСТЫ С ИСКЛЮЧЕНИЯМИ ====================
class TestEdgeCases(unittest.TestCase):
    """Тесты граничных случаев и исключений"""

    def test_detach_nonexistent_observer(self):
        """Тест открепления несуществующего наблюдателя"""
        transaction = BankTransaction("EDGE-001", "Тест")
        observer = TransactionLogger()

        # Не должно вызывать исключение
        transaction.detach(observer)

    def test_multiple_attachments_same_observer(self):
        """Тест многократного прикрепления одного наблюдателя"""
        transaction = BankTransaction("EDGE-002", "Тест")
        observer = TransactionLogger()

        transaction.attach(observer)
        transaction.attach(observer)  # Второй раз
        transaction.attach(observer)  # Третий раз

        # Должен быть добавлен только один раз
        transaction_data = transaction.process_transaction(1000, "Тест")
        # В реальной реализации нужно проверить внутреннее состояние

    def test_empty_notification(self):
        """Тест пустого сообщения"""
        factory = NotificationFactory()
        notification = factory.create_notification("email")
        result = notification.send("")
        self.assertEqual(result, "📧 Отправка email: ")

# ==================== ЗАПУСК ТЕСТОВ ====================
def run_tests():
    """Запускает все тесты"""
    print("\n" + "=" * 70)
    print("ТЕСТИРОВАНИЕ ЛАБОРАТОРНОЙ РАБОТЫ №4")
    print("=" * 70)

    # Создаем тестовый набор
    loader = unittest.TestLoader()

    # Добавляем все тестовые классы
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestFactoryPatternTDD))
    suite.addTests(loader.loadTestsFromTestCase(TestAdapterPatternTDD))
    suite.addTests(loader.loadTestsFromTestCase(TestObserverPatternTDD))
    suite.addTests(loader.loadTestsFromTestCase(TestPatternsWithMocks))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestEdgeCases))

    # Запускаем тесты
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Выводим статистику
    print("\n" + "=" * 70)
    print("СТАТИСТИКА ТЕСТИРОВАНИЯ:")
    print(f"  Всего тестов: {result.testsRun}")
    print(f"  Успешно: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"  Провалено: {len(result.failures)}")
    print(f"  Ошибок: {len(result.errors)}")

    if result.failures:
        print("\nПРОВАЛЕННЫЕ ТЕСТЫ:")
        for test, traceback in result.failures:
            print(f"  - {test}")

    if result.errors:
        print("\nОШИБКИ:")
        for test, traceback in result.errors:
            print(f"  - {test}")

    print("=" * 70)

    return result

if __name__ == "__main__":
    # Запускаем все тесты
    test_result = run_tests()

    # Возвращаем код выхода для CI/CD
    exit_code = 0 if test_result.wasSuccessful() else 1
    exit(exit_code)
