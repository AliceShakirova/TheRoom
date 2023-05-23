"""
Модуль описывает класс Building, позволяющий создать следующие объекты:
вход(entry_point), выход(exit), алтари (altar), источники живой воды (water_of_life), в перспективе сундуки(box) и что-нибудь еще.
"""
from enum import Enum


class Building(Enum):
    """Класс Building используется для хранения констант, соответсвующих
    типу объекта Building, и для создания объектов

        Основное применение - в классе Cell и контроллере игры

        Note:
            В перспективе планируется использовать дополнительные константы
            и объекты (пример, сундуки(box))

    Attributes
    ----------
    kind : object
        тип объекта, используются константы

    Methods
    -------
    __init__(kind)
        метод-конструктор, создающий объект определенного типа
    """

    ENTRY_POINT = 1
    EXIT = 2
    ALTAR = 3
    ACTIVE_ALTAR = 4
    WATER_OF_LIFE = 5

    kind = None


    def __init__(self, kind):
        """
        Метод-контруктор, создающий объект определенного типа
        :param kind: int
        """
        self.kind = kind


if __name__ == '__main__':
    obj = Building(Building.ALTAR)
    print('Объект:', obj.name)

    print(list(Building))
