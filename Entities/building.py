"""
Модуль описывает класс Building, позволяющий создать следующие объекты:
вход(entry_point), выход(exit), алтари (altar), источники живой воды (water_of_life), в перспективе сундуки(box) и что-нибудь еще.
"""
from enum import Enum


class Building(Enum):
    """Класс Building используется для хранения констант, соответсвующих типу объекта Building, и для создания объектов
    ----------
    Attributes
        kind : int, тип объекта, используются константы
    -------
    Methods
    __init__(kind)
        метод-конструктор, создающий объект определенного типа (kind)
    """

    ENTRY_POINT = 1
    EXIT = 2
    ALTAR = 3
    ACTIVE_ALTAR = 4
    WATER_OF_LIFE = 5

    def __init__(self, kind=None):
        """Метод-контруктор, создающий объект определенного типа (kind)
        :parameter kind: int
        """
        self.kind = kind


if __name__ == '__main__':
    obj = Building(Building.ALTAR)
    print('Объект:', obj.name)

    print(list(Building))
