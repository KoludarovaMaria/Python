import math

try:
    from lab_python_oop.figure import GeometricFigure
    from lab_python_oop.color import FigureColor
except ImportError:
    from figure import GeometricFigure
    from color import FigureColor

class Circle(GeometricFigure):
    """Класс круга"""

    figure_name = "Круг"

    def __init__(self, radius, color):
        """
        Конструктор круга

        Args:
            radius (float): радиус круга
            color (str): цвет круга
        """
        self.radius = radius
        self.color_obj = FigureColor(color)

    def area(self):
        """Вычисление площади круга"""
        return math.pi * self.radius ** 2

    def __repr__(self):
        """Строковое представление круга"""
        return "{}, радиус: {}, цвет: {}, площадь: {:.2f}".format(
            self.get_name(),
            self.radius,
            self.color_obj.color,
            self.area()
        )
