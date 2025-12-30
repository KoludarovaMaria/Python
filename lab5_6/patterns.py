"""
Лабораторная работа №4
Шаблоны проектирования в Python
Все паттерны реализованы в одном файле для удобства
"""

# ==================== БАЗОВЫЙ КЛАСС ====================
from abc import ABC, abstractmethod

class Notification(ABC):
    """Абстрактный класс уведомления"""
    @abstractmethod
    def send(self, message: str) -> str:
        pass


# ==================== ПОРОЖДАЮЩИЙ ПАТТЕРН: ФАБРИЧНЫЙ МЕТОД ====================
class EmailNotification(Notification):
    """Email уведомление"""
    def send(self, message: str) -> str:
        return f"📧 Отправка email: {message}"

class SMSNotification(Notification):
    """SMS уведомление"""
    def send(self, message: str) -> str:
        return f"📱 Отправка SMS: {message}"

class PushNotification(Notification):
    """Push уведомление"""
    def send(self, message: str) -> str:
        return f"🔔 Отправка Push-уведомления: {message}"

class NotificationFactory:
    """Фабрика для создания уведомлений"""

    @staticmethod
    def create_notification(notification_type: str) -> Notification:
        """Создает уведомление указанного типа"""
        notification_types = {
            "email": EmailNotification,
            "sms": SMSNotification,
            "push": PushNotification
        }

        if notification_type not in notification_types:
            raise ValueError(f"Неизвестный тип уведомления: {notification_type}")

        return notification_types[notification_type]()


# ==================== СТРУКТУРНЫЙ ПАТТЕРН: АДАПТЕР ====================
class LegacyBankSystem:
    """Старая банковская система с несовместимым интерфейсом"""

    def send_alert(self, code: int, text: str) -> str:
        """Метод старой системы"""
        return f"[Код {code}] {text}"

class BankSystemAdapter(Notification):
    """Адаптер для интеграции старой банковской системы с новой"""

    def __init__(self, legacy_system: LegacyBankSystem):
        self.legacy_system = legacy_system

    def send(self, message: str) -> str:
        """Адаптирует вызов нового метода к старой системе"""
        code_map = {
            "оплата": 100,
            "перевод": 200,
            "ошибка": 300,
            "блокировка": 400
        }

        for key, code in code_map.items():
            if key in message.lower():
                return self.legacy_system.send_alert(code, message)

        return self.legacy_system.send_alert(0, message)


# ==================== ПОВЕДЕНЧЕСКИЙ ПАТТЕРН: НАБЛЮДАТЕЛЬ ====================
from typing import List

class Subject(ABC):
    """Субъект для наблюдения (издатель)"""

    def __init__(self):
        self._observers: List['Observer'] = []

    def attach(self, observer: 'Observer') -> None:
        """Прикрепляет наблюдателя"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: 'Observer') -> None:
        """Открепляет наблюдателя"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, transaction_data: dict) -> None:
        """Уведомляет всех наблюдателей"""
        for observer in self._observers:
            observer.update(transaction_data)

class Observer(ABC):
    """Наблюдатель (подписчик)"""

    @abstractmethod
    def update(self, transaction_data: dict) -> str:
        """Метод, вызываемый при изменении субъекта"""
        pass

class BankTransaction(Subject):
    """Банковская транзакция (субъект)"""

    def __init__(self, transaction_id: str, sender: str):
        super().__init__()
        self.transaction_id = transaction_id
        self.sender = sender
        self.status = "pending"
        self.amount = 0.0
        self.recipient = ""

    def process_transaction(self, amount: float, recipient: str) -> dict:
        """Обрабатывает транзакцию и уведомляет наблюдателей"""
        self.amount = amount
        self.recipient = recipient

        transaction_data = {
            "id": self.transaction_id,
            "sender": self.sender,
            "amount": amount,
            "recipient": recipient,
            "status": "completed"
        }

        self.status = "completed"
        self.notify(transaction_data)

        return transaction_data

    def cancel_transaction(self) -> dict:
        """Отменяет транзакцию и уведомляет наблюдателей"""
        transaction_data = {
            "id": self.transaction_id,
            "sender": self.sender,
            "amount": self.amount,
            "recipient": self.recipient,
            "status": "cancelled"
        }

        self.status = "cancelled"
        self.notify(transaction_data)

        return transaction_data

class TransactionLogger(Observer):
    """Логгер транзакций (наблюдатель)"""

    def update(self, transaction_data: dict) -> str:
        """Логирует информацию о транзакции"""
        log_message = (
            f"📝 ЛОГ: Транзакция {transaction_data['id']} | "
            f"От: {transaction_data['sender']} | "
            f"Кому: {transaction_data['recipient']} | "
            f"Сумма: {transaction_data['amount']} руб. | "
            f"Статус: {transaction_data['status']}"
        )
        return log_message

class FraudDetector(Observer):
    """Детектор мошенничества (наблюдатель)"""

    def __init__(self, threshold: float = 100000.0):
        self.threshold = threshold

    def update(self, transaction_data: dict) -> str:
        """Проверяет транзакцию на мошенничество"""
        if transaction_data['amount'] > self.threshold:
            alert_message = (
                f"🚨 ВНИМАНИЕ! Подозрительная транзакция!\n"
                f"   ID: {transaction_data['id']}\n"
                f"   Сумма: {transaction_data['amount']} руб. (превышен порог {self.threshold} руб.)\n"
                f"   От: {transaction_data['sender']} -> Кому: {transaction_data['recipient']}"
            )
            return alert_message
        return ""

class NotificationService(Observer):
    """Сервис уведомлений (наблюдатель)"""

    def __init__(self, notification_factory: NotificationFactory):
        self.notification_factory = notification_factory

    def update(self, transaction_data: dict) -> str:
        """Отправляет уведомление о транзакции"""
        if transaction_data['status'] == 'completed':
            notification = self.notification_factory.create_notification("email")
            message = (
                f"Транзакция {transaction_data['id']} успешно выполнена.\n"
                f"Сумма: {transaction_data['amount']} руб.\n"
                f"Получатель: {transaction_data['recipient']}"
            )
            return notification.send(message)
        elif transaction_data['status'] == 'cancelled':
            notification = self.notification_factory.create_notification("sms")
            message = f"Транзакция {transaction_data['id']} отменена."
            return notification.send(message)
        return ""
