"""Модуль khan_controller описывает основной класс KhanGameController, обрабатывающий всю игровую логику.
"""
import random
import time
from datetime import datetime, timedelta

from Entities.frame import Frame
from Entities.entity_types import EntityTypes
from Entities.fow_mode import FowMode
from Entities.battle import Battle
from Entities.building import Building
from Entities.character import Character
from Entities.room_creator import RoomCreator
from Entities.drawing_cell import DrawingCell
from Entities.room import Room


class KhanGameController:
    """Класс KhanGameController обрабатывает всю игровую логику
    ----------
    Attributes
        lvl - int, уровень комнаты, от которого зависят размеры комнаты, количество и параметры персонажей
        room - object class Room, список списков, основная карта
        hero - object class Character, основной персонаж игры
        battle - object class Battle, интерфейс для проведения боя
        smoke - bool, флаг, определяющий, отображается туман или нет
        mode - int, режим отрисовки
        battle_result - object class BattleResult, содержит итоги боя
        message - dict, содержит сообщение и кнопки для messagebox
    -------
    Methods
        start_new_game(lvl)
            метод начинает новую игру, инициирует создание всех ключевых объектов
        process_key(button):
            метод передает нажатую кнопку на обработку в нужный метод, а затем фиксирует все произведенные изменения
        get_current_frame():
            метод вызывается из контроллера графического интерфейса для получения последних изменений для отрисовки кадра
    """

    # Constants
    # Кнопки управления
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    ENTER = 5

    # Режимы отрисовки
    MENU = 0
    MAP = 1
    MESSAGE = 2
    BATTLE = 3
    QUIT = 4

    # Режимы диалогого окна
    YES = 0
    NO = 1
    OK = 2

    # Шаги контроллера
    MOVE = 0
    ALTAR = 1
    EXIT = 2
    WATER = 4
    BATTLE = 3
    BATTLE_END = 5
    END = 6
    NEW_STEP = 7

    # Ключи словаря message
    MESSAGE_KEY = 0
    MESSAGE_MODE_KEY = 1

    # attrs
    lvl = 0
    room = None
    hero = None
    start_health = 0
    battle = None
    smoke = True
    mode = None
    battle_result = None
    message = {MESSAGE_KEY: '', MESSAGE_MODE_KEY: OK}
    time_to_rescue = datetime.max

    def __init__(self):
        """
        Метод-конструктор, создающий объект, связывая его с определенным представителем EngineConnector
        :param ec: представитель EngineConnector
        """
        self.battle = Battle()
        self.last_frame = Frame(2)
        self.old_cell = None
        self.new_cell = None
        self.step = self.MOVE
        self.room_creator = RoomCreator()

    def start_new_game(self, lvl):
        """Метод start_new_game начинает новую игру, инициирует создание основной карты (room), основного
        персонажа (hero), генерацию и размещение бандитов
        :parameter lvl: int, уровень карты
        """
        self.room = RoomCreator.get_room(self.room_creator, lvl)
        self.hero = Character(lvl)
        self.start_health = self.hero.start_health
        self.room[self.room.entry_point].hero_here = self.hero
        self.room.hero_cell = self.room.entry_point
        self.old_cell = self.room.hero_cell

        # Генерация и размещение бандитов и источников живой воды
        bandits = random.choices(self.room_creator.pointlist, k=(lvl * Character.ENEMY_COUNT_MULTIPLIER))
        for tup in bandits:
            if self.room[tup].entity_type == EntityTypes.EMPTY:
                self.room[tup].char_here = Character(lvl, hero=False)
                self.get_blocked_cell(tup, self.room[tup].char_here)
        water_of_life = random.choices(self.room_creator.pointlist, k=(lvl * Character.ENEMY_COUNT_MULTIPLIER // 2))
        for tup in water_of_life:
            if self.room[tup].entity_type == EntityTypes.EMPTY and not self.room[tup].char_here:
                self.room[tup].entity = Building.WATER_OF_LIFE
        self.mode = self.MAP
        self.last_frame = self.get_last_frame()

    def process_key(self, button, message=None):
        """Метод process_key в зависимости от режима отрисовки (mode) передает нажатую кнопку в нужный метод, а затем
        фиксирует все произведенные изменения в виде Frame
        :parameter button: int, соответствует введенной пользователем клавише"""
        if self.mode == self.MAP:
            self.new_move(button)
        elif self.mode == self.MESSAGE:
            self.process_messagebox_key(button)
        elif self.mode == self.BATTLE:
            if button:
                self.move_hero()
        self.last_frame = self.get_last_frame()

    def get_current_frame(self):
        """Метод get_current_frame вызывается из контроллера графического интерфейса для получения последних изменений
        для непосредственной отрисовки кадра"""
        return self.last_frame

    def get_last_frame(self):
        room = []
        x = 0
        for row in self.room:
            room.append([])
            y = 0
            for cell in row:
                room[x].append(DrawingCell())
                building = None
                unit = None
                if cell.entity_type == EntityTypes.ENTRY_POINT:
                    building = Frame.ENTRY_POINT
                elif self.smoke and cell.fow == FowMode.SHOWED:
                    building = Frame.FOW
                else:
                    if cell.entity_type == EntityTypes.EMPTY:
                        building = Frame.EMPTY
                    elif cell.entity_type == EntityTypes.EXIT:
                        building = Frame.EXIT
                    elif cell.entity_type == EntityTypes.ALTAR:
                        building = Frame.ALTAR
                    elif cell.entity_type == EntityTypes.ACTIVE_ALTAR:
                        building = Frame.ACTIVE_ALTAR
                    elif cell.entity_type == EntityTypes.WATER_OF_LIFE:
                        building = Frame.WATER_OF_LIFE
                if cell.hero_here:
                    unit = Frame.HERO
                elif cell.char_here and (cell.fow == FowMode.REVEALED or not self.smoke):
                    unit = Frame.BANDIT
                elif cell.blocked_by_enemy:
                    for enemy in cell.blocked_by_enemy:
                        if cell.fow == FowMode.SHOWED:
                            if enemy in self.room.discovered_bandits:
                                unit = Frame.FOW_BLOCKED
                                break
                room[x][y].building = building
                room[x][y].unit = unit
                y += 1
            x += 1

        self.last_frame = Frame(self.lvl, room, self.hero, self.mode, self.message, self.old_cell, self.new_cell,
                                self.smoke, self.battle_result)
        return self.last_frame

    def get_cell_to_move(self, button):
        """Метод get_cell_to_move в зависимости от полученной кнопки находит ячейку, куда перемещается герой
        :parameter button : int, соответствует введенной пользователем клавише"""
        if button == self.UP:
            self.new_cell = ((self.old_cell[0] - 1), self.old_cell[1])
        elif button == self.LEFT:
            self.new_cell = (self.old_cell[0], (self.old_cell[1] - 1))
        elif button == self.DOWN:
            self.new_cell = ((self.old_cell[0] + 1), self.old_cell[1])
        elif button == self.RIGHT:
            self.new_cell = (self.old_cell[0], (self.old_cell[1] + 1))
        elif button == self.ENTER:
            return

    def new_move(self, button):
        """Метод nem_move в случае жизнеспособности героя и невхождения героя в стенку, запускает новый ход"""
        if self.hero.health == 0:
            self.hero_live()
            return
        else:
            self.get_cell_to_move(button)

        if self.new_cell[0] in list(range(self.room.side_len)) and self.new_cell[1] in list(range(self.room.side_len)):
            enemy_discovered = None
            if self.room[self.new_cell].blocked_by_enemy:
                for enemy in self.room[self.new_cell].blocked_by_enemy:
                    if enemy in self.room.discovered_bandits:
                        enemy_discovered = True
                        break
                    else:
                        enemy_discovered = False
                if self.room[self.new_cell].fow == FowMode.SHOWED and enemy_discovered:
                    self.step = self.NEW_STEP
                    self.mode = self.MESSAGE
                    self.message = {self.MESSAGE_KEY: 'The bandit is nearby\n and he is vigilant',
                                    self.MESSAGE_MODE_KEY: self.OK}
                    return

            self.room[self.new_cell].fow = FowMode.REVEALED
            self.move_hero()
            if self.step != self.END:
                return
            else:
                self.end_of_step()
                return
        else:
            self.step = self.NEW_STEP
            self.mode = self.MESSAGE
            self.message = {KhanGameController.MESSAGE_KEY: 'You can\'t leave the\n playing field',
                            KhanGameController.MESSAGE_MODE_KEY: self.OK}
            return

    def get_blocked_cell(self, tup, bandit):
        """Метод вычисляет, какие клетки будут охранятся бандитами,в случае обнаружения"""
        adjacent_cell_coords = [(tup[0] + 1, tup[1]),
                                (tup[0], tup[1] + 1),
                                (tup[0] - 1, tup[1]),
                                (tup[0], tup[1] - 1)]
        valid_adjacent_cells_coords = []
        for cell_coord in adjacent_cell_coords:
            if cell_coord[0] in list(range(self.room.side_len)) and cell_coord[1] in list(range(self.room.side_len)):
                valid_adjacent_cells_coords.append(self.room[cell_coord])
                self.room[cell_coord].blocked_by_enemy.append(bandit)

    def hero_live(self):
        """Метод hero_live в случае наступления нужного времени (time_to_rescue) оживляет героя"""
        if self.time_to_rescue > datetime.now():
            self.mode = self.MESSAGE
            self.message[KhanGameController.MESSAGE_KEY] = 'Hero is defeat.\n He need a time...'
            self.message[KhanGameController.MESSAGE_MODE_KEY] = self.OK
            self.step = self.NEW_STEP
            return
        else:
            self.hero.health += 5
            return

    def process_messagebox_key(self, button):
        """Метод process_messagebox_key в зависимости от режима кнопок и введенной кнопки выбирает следующее действие
        :parameter button : int, соответствует введенной пользователем клавише"""
        if self.message[KhanGameController.MESSAGE_MODE_KEY] == self.OK:
            if button == self.ENTER:
                self.move_hero()
                if self.mode == self.QUIT:
                    return
                self.mode = self.MAP
                return
        if self.message[KhanGameController.MESSAGE_MODE_KEY] == self.YES:
            if button == self.ENTER:
                self.move_hero()
                if self.mode == self.QUIT:
                    return
                elif self.mode == self.BATTLE:
                    return
                self.mode = self.MAP
            if button == self.RIGHT:
                self.mode = self.MESSAGE
                self.message[KhanGameController.MESSAGE_MODE_KEY] = self.NO
        if self.message[KhanGameController.MESSAGE_MODE_KEY] == self.NO:
            if button == self.ENTER:
                if self.step == self.BATTLE:
                    self.mode = self.MAP
                    self.step = self.MOVE
                    return
                self.end_of_step()
            if button == self.LEFT:
                self.mode = self.MESSAGE
                self.message[KhanGameController.MESSAGE_MODE_KEY] = self.YES

    def move_hero(self):
        """Метод move_hero в завивисимости от атрибута step выбирает следующее действие"""
        new_cell = self.new_cell
        if self.step == self.MOVE:
            self.step_move()
            return
        elif self.step == self.ALTAR:
            self.altar_activate(new_cell)
            self.end_of_step()
            return
        elif self.step == self.EXIT:
            self.end_of_step()
            self.mode = self.QUIT
            return

        elif self.step == self.WATER:
            self.room[new_cell].entity = None
            self.hero.health = self.start_health
            self.end_of_step()
            return
        elif self.step == self.BATTLE:
            self.battle_result = self.battle.fight(self.hero, self.room[new_cell].char_here)
            self.mode = self.BATTLE
            self.step = self.BATTLE_END
            return
        elif self.step == self.BATTLE_END:
            if self.hero.health == 0 or self.battle_result.winner != self.hero:
                self.time_to_rescue = datetime.now() + timedelta(seconds=10)
                self.room.discovered_bandits.remove(self.room[new_cell].char_here)
                self.mode = self.MAP
                self.step = self.MOVE
            else:
                self.end_of_step()
        elif self.step == self.NEW_STEP:
            self.step = self.MOVE
            return
        self.end_of_step()

    def step_move(self):
        """Метод step_move в зависимости от entity_type полученной ячейки выбирает следующее действие"""
        # Сценарий с алтарем
        if self.room[self.new_cell].entity_type == EntityTypes.ALTAR:
            self.mode = self.MESSAGE
            self.message[KhanGameController.MESSAGE_KEY] = 'Altar. Activate?'
            self.message[KhanGameController.MESSAGE_MODE_KEY] = self.YES
            self.step = self.ALTAR
            return

        # Сценарий с выходом
        elif self.room[self.new_cell].entity_type == EntityTypes.EXIT:
            if self.room.active_altar == self.room.ACTIVE_ALL_ALTAR:
                self.mode = self.MESSAGE
                self.message[KhanGameController.MESSAGE_KEY] = 'Finish?'
                self.message[KhanGameController.MESSAGE_MODE_KEY] = self.YES
                self.step = self.EXIT
                return
            else:
                self.step = self.END
                return
        # Сценарий с живой водой
        elif self.room[self.new_cell].entity_type == EntityTypes.WATER_OF_LIFE:
            self.mode = self.MESSAGE
            self.message[KhanGameController.MESSAGE_KEY] = 'Water of life. Drink?'
            self.message[KhanGameController.MESSAGE_MODE_KEY] = self.YES
            self.step = self.WATER
            return
        # Сценарий с бандитом
        elif self.room[self.new_cell].char_here:
            if self.room[self.new_cell].char_here not in self.room.discovered_bandits:
                self.room.discovered_bandits.append(self.room[self.new_cell].char_here)
            self.mode = self.MESSAGE
            self.message[KhanGameController.MESSAGE_KEY] = 'Bandit. Battle?'
            self.message[KhanGameController.MESSAGE_MODE_KEY] = self.YES
            self.step = self.BATTLE
            return
        # Сценарий с пустой ячейкой
        elif self.room[self.new_cell].entity_type == EntityTypes.EMPTY \
                or self.room[self.new_cell].entity_type == EntityTypes.ACTIVE_ALTAR \
                or self.room[self.new_cell].entity_type == EntityTypes.ENTRY_POINT:
            self.step = self.END
            return

    def altar_activate(self, tup):
        """Внутренний метод altar_activate активирует алтари, вызывается из метода move_hero
        :param tup: tuple, ячейка, на которой необходимо автивировать алтарь
        """
        if self.room[tup].entity == Building.ALTAR:
            self.room[tup].entity = Building.ACTIVE_ALTAR
            self.room.active_altar += 1

    def end_of_step(self):
        """Метод end_of_step производит все необходимые действия для начала нового хода"""
        self.step = self.MOVE
        self.room.hero_cell = self.new_cell
        self.room[self.last_frame.old_cell].hero_here = False
        self.room[self.new_cell].hero_here = self.hero
        self.old_cell = self.new_cell
        self.mode = self.MAP


if __name__ == '__main__':
    """ control = KhanGameController(2)
    for x in control.room.rows:
        print(x)

    for row in control.room:
        print('\n')
        for cell in row:
            print(cell.status, cell.entity, sep=':', end=' ')"""
    from datetime import datetime, timedelta

    time = datetime.now()
    print(time)
    print(time + timedelta(seconds=5))
