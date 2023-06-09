"""Модуль описывает класс-контейнер, содержащий только константы"""
from enum import Enum


class EntityTypes(Enum):
    """Класс EntityTypes описывает константы, соотвестствующие типу объекта,
    расположенного в ячейке Cell
    """
    EMPTY = 0
    ENTRY_POINT = 1
    EXIT = 2
    ALTAR = 3
    ACTIVE_ALTAR = 4
    WATER_OF_LIFE = 5
