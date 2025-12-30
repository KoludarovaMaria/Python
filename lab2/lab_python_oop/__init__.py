# Делаем классы доступными при импорте пакета
from .figure import GeometricFigure
from .color import FigureColor
from .rectangle import Rectangle
from .circle import Circle
from .square import Square

__all__ = [
    'GeometricFigure',
    'FigureColor',
    'Rectangle',
    'Circle',
    'Square'
]
