"""Модуль описывает класс-контейнер Room, его атрибуты и перегрузку некоторых операций"""

class Room:
    """Класс Room используется для взаимодействия с объектами расположенными на игровом поле
        Methods
        __iter__
           полчуить объект итератора (rows) при вызове iter
        __getitem__() и __setitem__
           перегрузка операций индексирования и присваивания по индексу
       """
    ACTIVE_ALL_ALTAR = 2
    rows = []
    entry_point = tuple()
    side_len = 0
    active_altar = 0
    hero_cell = None
    discovered_bandits = []

    def __iter__(self):
        """Получить объект итератора (rows) при вызове iter"""
        return self.rows.__iter__()

    def __getitem__(self, index):
        """Перегрузка операции индексирования для получения прямого доступа к атрибуту rows"""
        return self.rows[index[0]][index[1]]

    def __setitem__(self, index, value):
        """Перегрузка операции присваивания по индексу для получения прямого доступа к атрибуту rows"""
        self.rows[index[0]][index[1]] = value
