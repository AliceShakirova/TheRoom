"""Модуль описывает класс RoomCreator, два его метода get_room и fill_room, атрибуты"""

import random
from Entities.cell import Cell
from Entities.building import Building
from Entities.fow_mode import FowMode
from Entities.room import Room


class RoomCreator:
    """Класс RoomCreator используется для создания основной карты игры, экземпляра класса Room
        -------
        Methods
            get_room(lvl)
                метод, создающий квадратную комнату, внутренне вызывающий метод fill_room
            fill_room(lvl, room)
                Заполняет комнату(room) основными объектами: вход, выход, алтари, пустые клетки
    """

    level_room = {0: 10, 1: 10, 2: 11, 3: 12, 4: 13, 5: 14, 6: 16, 7: 18, 8: 20, 9: 22, 10: 24, 11: 26, 12: 28, 13: 30,
                  14: 33, 15: 36, 16: 39, 17: 42, 18: 45, 19: 48, 20: 50, 21: 50, 22: 50, 23: 50, 24: 50, 25: 50}
    pointlist = []
    point1, point2, point3 = tuple(), tuple(), tuple()

    def get_room(self, lvl):
        """
        Метод get_room создает квадратную комнату с длиной стены (side_len), соотвествующей переданному уровню (lvl)
        вo внутреннем словаре level_room
        :parameter lvl: int, уровень карты
        """
        room = Room()
        side = list(range(RoomCreator.level_room[lvl]))
        room.rows.clear()
        for x in side:
            room.rows.append([])
            for y in side:
                room.rows[x].append(0)
        self.fill_room(lvl, room)
        return room


    """h
        def __next__(self): # Возвратить ячейку на каждой итерации
            if self.rows == self.rows[-1]:  # Также вызывается встроенной функцией next
                raise StopIteration
            self.rows.
            return
    """

    def fill_room(self, lvl, room):
        """
        Внутреннний метод, заполняющий комнату основными объектами, автоматически вызываемый в конструкторе. На вход
        принимает уровень (lvl), возвращает экземпляр класса Room.
        :parameter lvl: int, уровень карты
        :parameter room: class Room, сформированная квадратная комната
        """
        # Выделяем периметр, меняем 0 на 4
        room.side_len = (RoomCreator.level_room[lvl])
        for x in range(room.side_len):
            for y in range(room.side_len):
                if (x in [0, 1, (room.side_len - 2), (room.side_len - 1)]
                        or y in [0, 1, (room.side_len - 2), (room.side_len - 1)]):
                    room.rows[x][y] = 4

        # Определяем вход, меняем 4 на полноценный объект класса Cell
        room_angles = [(0, 0), (0, room.side_len-1), (room.side_len-1, 0), (room.side_len-1, room.side_len-1)]
        angle_indices = [0, 1, 2, 3]
        angle_index = random.choice(angle_indices)
        room.entry_point = room_angles[angle_index]
        room.rows[room.entry_point[0]][room.entry_point[1]] = Cell(Building.ENTRY_POINT, FowMode.REVEALED)

        # Создаем список кортежей
        self.pointlist = []
        for x in range(room.side_len):
            for y in range(room.side_len):
                self.pointlist.append((x, y))

        # Создаем вес
        weight = []
        for x in range(room.side_len):
            for y in range(room.side_len):
                if room.rows[x][y] == 4:
                    weight.append(85)
                elif room.rows[x][y] == Cell(Building.ENTRY_POINT, FowMode.REVEALED):
                    weight.append(0)
                else:
                    weight.append(15)

        # Выбираем три точки
        points = random.choices(self.pointlist, weights=weight, k=3)
        self.point1 = points[0]
        self.point2 = points[1]
        self.point3 = points[2]
        room.rows[self.point1[0]][self.point1[1]] = Cell(Building.EXIT, FowMode.SHOWED)
        room.rows[self.point2[0]][self.point2[1]] = Cell(Building.ALTAR, FowMode.SHOWED)
        room.rows[self.point3[0]][self.point3[1]] = Cell(Building.ALTAR, FowMode.SHOWED)

        # Подчищаем периметр
        for x in range(room.side_len):
            for y in range(room.side_len):
                if room.rows[x][y] in [0, 4]:
                    room.rows[x][y] = Cell(None, FowMode.SHOWED)
        return room


# Самотестирование в случае запуска напрямую
if __name__ == '__main__':
    room_creator = RoomCreator()
    test_room = RoomCreator.get_room(room_creator, 2)
    for row in test_room:
        print('\n')
        for cell in row:
            print(cell.fow, cell.entity, sep=':', end=' ')
    print(test_room.entry_point)
