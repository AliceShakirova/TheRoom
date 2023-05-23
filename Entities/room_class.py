"""Модуль описывает класс Room
"""

import random
from Entities.cell import Cell
from Entities.building import Building
from Entities.FowMode import FowMode
from Entities.EntityTypes import EntityTypes


class Room:
    """Класс Room используется для создания основной карты игры

    Основное применение - в контроллере игры для обращения
    к элементам игры

    Note:
        В перспективе возможна генерация комнаты прямоугольной
        комнаты произвольной величины

    Attributes
    ----------
    level_room : dict
        соответствие уровня и длины комнаты
    rows : list
        список списков с экземплярами класса Cell
    entry_point : tuple
        кортеж с координатами точки входа
    side_len : int
        длина комнаты
    pointlist : list
        список кортежей с координатами всех ячеек
    point1, point2, point3 : tuple
        кортежи с координатами ключевых ячеек для перехода на новый уровень
    active_altar : int
        количество активировванных алтарей
    hero_cell : объект class Cell
        ячейка, в которой находится герой

    Methods
    -------
    __init__(lvl)
        метод-конструктор, создающий квадратную комнату,автоматически
        вызывающий метод fill_room
    fill_room(lvl)
        Заполняет комнату основными объектами: вход, выход, алтари, пустые клетки
    """

    ACTIVE_ALL_ALTAR = 2
    level_room = {0: 10, 1: 10, 2: 11, 3: 12, 4: 13, 5: 14, 6: 16, 7: 18, 8: 20, 9: 22, 10: 24, 11: 26, 12: 28, 13: 30,
                  14: 33, 15: 36, 16: 39, 17: 42, 18: 45, 19: 48, 20: 50, 21: 50, 22: 50, 23: 50, 24: 50, 25: 50}
    rows = []
    entry_point = tuple()
    side_len = 0
    pointlist = []
    point1, point2, point3 = tuple(), tuple(), tuple()
    active_altar = 0
    hero_cell = None

    def __init__(self, lvl):
        """
        Конструктор, создающий квадратную комнату с длиной стены (side_len), соотвествующей переданному уровню (lvl)
        в словаре level_room
        :param lvl:
        """
        side = list(range(Room.level_room[lvl]))
        for x in side:
            self.rows.append([])
            for y in side:
                self.rows[x].append(0)
        self.fill_room(lvl)

    def __iter__(self):  # Получить объект итератора при вызове iter
        return self.rows.__iter__()

    def __getitem__(self, index):
        return self.rows[index]

    def __setitem__(self, index, value):
        self.rows[index] = value

    """h
        def __next__(self): # Возвратить ячейку на каждой итерации
            if self.rows == self.rows[-1]:  # Также вызывается встроенной функцией next
                raise StopIteration
            self.rows.
            return
    """

    def fill_room(self, lvl):
        """
        Внутреннний метод, заполняющий комнату основными объектами, автоматически вызываемый в конструкторе. На вход
        принимает уровень (lvl), возвращает атрибут rows.
        """
        # Выделяем периметр, меняем 0 на 4
        self.side_len = (Room.level_room[lvl])
        for x in range(self.side_len):
            for y in range(self.side_len):
                if (x in [0, 1, (self.side_len - 2), (self.side_len - 1)]
                        or y in [0, 1, (self.side_len - 2), (self.side_len - 1)]):
                    self.rows[x][y] = 4

        # Определяем вход, меняем 4 на полноценный объект класса Cell
        room_angles = [(0, 0), (0, self.side_len-1), (self.side_len-1, 0), (self.side_len-1, self.side_len-1)]
        angle_indices = [0, 1, 2, 3]
        angle_index = random.choice(angle_indices)
        self.entry_point = room_angles[angle_index]
        self.rows[self.entry_point[0]][self.entry_point[1]] = Cell(Building.ENTRY_POINT, FowMode.REVEALED)

        # Создаем список кортежей
        for x in range(self.side_len):
            for y in range(self.side_len):
                self.pointlist.append((x, y))

        # Создаем вес
        weight = []
        for x in range(self.side_len):
            for y in range(self.side_len):
                if self.rows[x][y] == 4:
                    weight.append(85)
                elif self.rows[x][y] == Cell(Building.ENTRY_POINT, FowMode.REVEALED):
                    weight.append(0)
                else:
                    weight.append(15)

        # Выбираем три точки
        points = random.choices(self.pointlist, weights=weight, k=3)
        self.point1 = points[0]
        self.point2 = points[1]
        self.point3 = points[2]
        self.rows[self.point1[0]][self.point1[1]] = Cell(Building.EXIT, FowMode.SHOWED)
        self.rows[self.point2[0]][self.point2[1]] = Cell(Building.ALTAR, FowMode.SHOWED)
        self.rows[self.point3[0]][self.point3[1]] = Cell(Building.ALTAR, FowMode.SHOWED)

        # Подчищаем периметр
        for x in range(self.side_len):
            for y in range(self.side_len):
                if self.rows[x][y] in [0, 4]:
                    self.rows[x][y] = Cell(None, FowMode.SHOWED)
        return self.rows



# Самотестирование в случае запуска напрямую
if __name__ == '__main__':
    room = Room(2)
    for row in room:
        print('\n')
        for cell in row:
            print(cell.fow, cell.entity, sep=':', end=' ')
    print(room.entry_point)