# Убираем относительный импорт, используем прямой
try:
    # Пытаемся импортировать из того же пакета
    from lab_python_oop.figure import GeometricFigure
    from lab_python_oop.color import FigureColor
except ImportError:
    # Если не работает, определяем классы локально или импортируем напрямую
    from figure import GeometricFigure
    from color import FigureColor

class Rectangle(GeometricFigure):
    """Класс прямоугольника"""

    figure_name = "Прямоугольник"

    def __init__(self, width, height, color):
        """
        Конструктор прямоугольника

        Args:
            width (float): ширина прямоугольника
            height (float): высота прямоугольника
            color (str): цвет прямоугольника
        """
        self.width = width
        self.height = height
        self.color_obj = FigureColor(color)

    def area(self):
        """Вычисление площади прямоугольника"""
        return self.width * self.height

    def __repr__(self):
        """Строковое представление прямоугольника"""
        return "{}, ширина: {}, высота: {}, цвет: {}, площадь: {:.2f}".format(
            self.get_name(),
            self.width,
            self.height,
            self.color_obj.color,
            self.area()
        )
