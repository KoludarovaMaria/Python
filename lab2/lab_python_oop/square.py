try:
    from lab_python_oop.rectangle import Rectangle
except ImportError:
    from rectangle import Rectangle

class Square(Rectangle):
    """Класс квадрата, наследуется от прямоугольника"""

    figure_name = "Квадрат"

    def __init__(self, side, color):
        """
        Конструктор квадрата

        Args:
            side (float): длина стороны квадрата
            color (str): цвет квадрата
        """
        super().__init__(side, side, color)

    def __repr__(self):
        """Строковое представление квадрата"""
        return "{}, сторона: {}, цвет: {}, площадь: {:.2f}".format(
            self.get_name(),
            self.width,
            self.color_obj.color,
            self.area()
        )
