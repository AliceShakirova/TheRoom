"""
Модуль получает на обработку список списков, заполненный объектами, и отображает их так,
чтобы было очевидны размеры комнаты, её наполнение и содержимое, или же строку-сообщение,
которое необходимо вывести игроку
"""
from Entities.cell import Cell
from Entities.fow_mode import FowMode
from Entities.entity_types import EntityTypes
from Entities.character import Character


class consolDisplay:
    """Класс Display используется для вывода основной карты игры
    или строки-сообщения в консоль

    Основное применение - в контроллере игры для вывода

    Methods
    -------
    draw(self, map, smoke=True)
        метод описывает вывод каждого объекта map, покрытое (smoke=True) или не
        покрытое туманом (smoke=False)
    writer(string)
        метод выводит переданную контроллером строку-сообщение(string) в консоль
    """
    def draw(self, map, smoke=True):
        """Метод draw описывает вывод каждого объекта map, покрытое (smoke=True) или не
        покрытое туманом (smoke=False)
        :param map: list
        :param smoke: bool
        :return:
        """
        print('\n', 'H is hero', 'B is Bandit', 'O is out', 'A is altar', 'I is in', '- is empty', 'X is fog', sep='\n')
        for row in map:
            print('\n')
            for obj in row:
                obj.update_entity_type()
                if obj.hero_here:
                    print('H', end='  ')
                elif smoke and obj.fow == FowMode.SHOWED:
                    print('X', end='  ')
                elif obj.char_here:
                    print('B', end='  ')
                elif obj.entity_type == EntityTypes.EMPTY:
                    print('-', end='  ')
                elif obj.entity_type == EntityTypes.ENTRY_POINT:
                    print('I', end='  ')
                elif obj.entity_type == EntityTypes.EXIT:
                    print('O', end='  ')
                elif obj.entity_type == EntityTypes.ALTAR:
                    print('A', end='  ')
                elif obj.entity_type == EntityTypes.ACTIVE_ALTAR:
                    print('A*', end=' ')
                elif obj.entity_type == EntityTypes.WATER_OF_LIFE:
                    print('W', end='  ')
                else:
                    print('?', end='  ')

    def writer(self, string):
        """

        :param string:
        :return:
        """
        print('\n{}'.format(string))
        return ''

    def fighter(self, winner):
        print('%s побеждает в этой нелегкой схватке' % winner)
        return ''


