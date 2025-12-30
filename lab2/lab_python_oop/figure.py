from abc import ABC, abstractmethod

class GeometricFigure(ABC):
    """Абстрактный класс геометрической фигуры"""

    @abstractmethod
    def area(self):
        """Абстрактный метод для вычисления площади"""
        pass

    def get_name(self):
        """Возвращает название фигуры"""
        return self.figure_name if hasattr(self, 'figure_name') else self.__class__.__name__

    @abstractmethod
    def __repr__(self):
        pass
