"""Модуль khan_controller описывает основной класс KhanGameController, позволяющий взаимодействовать с игрой
"""
import random
import time
from datetime import datetime

from Entities.EntityTypes import EntityTypes
from Entities.FowMode import FowMode
from Entities.battle import Battle
from Entities.building import Building
from Entities.character import Character
from Entities.room_class import Room


class KhanGameController:
    """Класс KhanGameController используется для взаимодействия с объектами,
    расположенными на игровом поле

    Основное применение - в классе Room и контроллере игры

    Note:
        В перспективе планируется использовать атрибут terrain,
        описывающий ландшафт на ячейке (пример: вода, земля, гора и т.д.

    Attributes
    ----------
    lvl : int
        уровень комнаты, от которого зависят размеры комнаты, количество и параметры персонажей
    room : list
        список списков, представляющий собой основную карту
    hero : object class Character
        основной персонаж игры
    ec : object
        интерфейс для EngineConnector
    battle :  object class Battle
        интерфейс для проведения сражений между героем и бандитами

    Methods
    -------
    __init__(eс)
       метод-конструктор, создающий объект, связывая его с определенным представителем EngineConnector
     start_new_game(lvl)
        метод начинает новую игру, инициирует создание основной карты(room), основного персонажа(hero),
        генерацию и размещение бандитов (Character(lvl, hero=False)) и источников живой воды (water_of_life)
    move_hero(direction)
        метод производит сдвиг основного персонажа на одну клетку в выбранном (direction) направлении
    altar_active(tup)
        внутренний метод, активирующий алтари, вызывается из метода move_hero
    countdown(num_of_secs)
        внутренний метод-таймер, вызывается из метода move_hero
    """
    # Кнопки управления персонажем
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    ENTER = 5

    # Режимы отрисовки
    MENU = 0
    MAP = 2
    MESSAGE = 3
    BATTLE = 4
    QUIT = 5

    # Режимы диалогого окна
    YES = 0
    NO = 1
    OK = 2

    # Шаги контроллера
    MOVE = 0
    ALTAR = 1
    EXIT = 2
    WATER = 3
    BATTLE = 4
    BATTLE_END = 5
    END = 6
    NEW_STEP = 7

    lvl = 0
    room = None
    hero = None
    start_health = 0
    view = None
    battle = None
    smoke = True
    time_to_rescue = datetime.max


    def __init__(self):
        """
        Метод-конструктор, создающий объект, связывая его с определенным представителем EngineConnector
        :param ec: представитель EngineConnector
        """
        self.battle = Battle()
        self.old_cell = None
        self.new_cell = None
        self.step = self.MOVE

    def start_new_game(self, lvl):
        """Метод start_new_game начинает новую игру, инициирует создание основной карты(room), основного персонажа(hero),
        генерацию и размещение бандитов
        """
        self.room = Room(lvl)
        self.hero = Character(lvl)
        self.start_health = self.hero.start_health
        self.room[self.room.entry_point[0]][self.room.entry_point[1]].hero_here = self.hero
        self.room.hero_cell = (self.room.entry_point[0], self.room.entry_point[1])
        self.old_cell = (self.room.hero_cell[0], self.room.hero_cell[1])

        # Генерация и размещение бандитов и источников живой воды
        bandits = random.choices(self.room.pointlist, k=(lvl * Character.ENEMY_COUNT_MULTIPLIER))
        for tup in bandits:
            if self.room[tup[0]][tup[1]].entity_type == EntityTypes.EMPTY:
                self.room[tup[0]][tup[1]].char_here = Character(lvl, hero=False)
        water_of_life = random.choices(self.room.pointlist, k=(lvl * Character.ENEMY_COUNT_MULTIPLIER//2))
        for tup in water_of_life:
            if self.room[tup[0]][tup[1]].entity_type == EntityTypes.EMPTY and not self.room[tup[0]][tup[1]].char_here:
                self.room[tup[0]][tup[1]].entity = Building.WATER_OF_LIFE
                self.room[tup[0]][tup[1]].get_entity_type()
        self.view = [self.MAP]

    def process_key(self, button):
        if self.hero.health == 0:
            self.hero_live()
            return
        else:
            if not button:
                return
            elif button == self.UP:
                self.new_cell = ((self.old_cell[0] - 1), self.old_cell[1])
            elif button == self.LEFT:
                self.new_cell = (self.old_cell[0], (self.old_cell[1] - 1))
            elif button == self.DOWN:
                self.new_cell = ((self.old_cell[0] + 1), self.old_cell[1])
            elif button == self.RIGHT:
                self.new_cell = (self.old_cell[0], (self.old_cell[1] + 1))
            elif button == self.ENTER:
                return

        if self.new_cell[0] in list(range(self.room.side_len)) and self.new_cell[1] in list(range(self.room.side_len)):
            self.room[self.new_cell[0]][self.new_cell[1]].fow = FowMode.REVEALED
            time.sleep(0.2)
            self.move_hero()
            if self.step != self.END:
                return
            else:
                self.end_of_step()
                return
        else:
            self.step = self.NEW_STEP
            self.view = [self.MESSAGE, 'Outside the playing field', self.OK]
            return

    def hero_live(self):
        if self.time_to_rescue < datetime.now():
            self.view = [self.MESSAGE, 'Hero is defeat. He need a time...', self.OK]
            self.step = self.NEW_STEP
            return
        else:
            self.hero.health += 5
            return

    def process_messagebox_key(self, button, select=OK):
        if select == self.OK:
            if button == self.ENTER:
                self.move_hero()
                if self.view[0] == self.QUIT:
                    return
                self.view[0] = self.MAP
                return
        if select == self.YES:
            if button == self.ENTER:
                self.move_hero()
                if self.view[0] == self.QUIT:
                    return
                elif self.view[0] == self.BATTLE:
                    return
                self.view[0] = self.MAP
            if button == self.RIGHT:
                self.view[0] = self.MESSAGE
                self.view[2] = self.NO
        if select == self.NO:
            if button == self.ENTER:
                self.step = self.END
                self.end_of_step()
            if button == self.LEFT:
                self.view[0] = self.MESSAGE
                self.view[2] = self.YES


    def move_hero(self):

        new_cell = self.new_cell
        if self.step == self.MOVE:
            self.step_move()
            return
        elif self.step == self.ALTAR:
            self.altar_active(new_cell)
            self.end_of_step()
            return
        elif self.step == self.EXIT:
            self.end_of_step()
            self.view[0] = self.QUIT
            return

        elif self.step == self.WATER:
            self.room[new_cell[0]][new_cell[1]].entity = None
            self.hero.health = self.start_health
            self.end_of_step()
            return
        elif self.step == self.BATTLE:
            winner = self.battle.fight(self.hero, self.room[new_cell[0]][new_cell[1]].char_here)
            self.view = [self.BATTLE, winner]
            self.step = self.BATTLE_END
            return
        elif self.step == self.BATTLE_END:
            if self.hero.health == 0 or self.view[1]['winner'] != self.hero:
                self.time_to_rescue = datetime.now() + timedelta(seconds=20)
                self.view[0] = self.MAP
                self.step = self.MOVE
            else:
                self.end_of_step()
        elif self.step == self.NEW_STEP:
            self.step = self.MOVE
            return
        self.end_of_step()

        """      
        # Сценарий с бандитом
        
            continuer = input(self.ec.writer('На пути стоит бандит. Разберемся с ним? Ответ Y или N:'))
            if continuer == 'N' or continuer == 'n':
                return
            elif continuer == 'Y' or continuer == 'y':
                # self.ec.writer('BATTLE!!!')
                win = self.battle.fight(self.hero, self.room[new_cell[0]][new_cell[1]].char_here)
                for score in win[0]:
                    self.ec.writer('%s' % score)
                    time.sleep(1)
                if win[1] is self.hero:
                    self.ec.fighter('Наш герой')
                    self.room.hero_cell = new_cell
                    self.room[old_cell[0]][old_cell[1]].hero_here = False
                    self.room[new_cell[0]][new_cell[1]].char_here = None
                    self.room[new_cell[0]][new_cell[1]].hero_here = self.hero
                    continuer = input(self.ec.writer('Принять? Нажмите любую кнопку'))
                    if continuer:
                        return
                else:
                    self.ec.fighter('Бандит')
                    continuer = input(self.ec.writer('Сожалею, Вы проиграли. Или играем дальше? Ответ Y или N:'))
                    if continuer == 'Y' or continuer == 'y':
                        self.countdown(10)
                        self.ec.writer('Продолжаем вечеринку!')
                        time.sleep(2)
                        self.hero.health += 10
                        self.ec.draw(self.room, smoke=True)
                        return
                    else:
                        continuer = input(self.ec.writer('Вы хотите закончить текущую игру? Ответ Y или N:'))
                        if continuer == 'Y' or continuer == 'y':
                            return 'Y'
                        else:
                            return
            else:
                self.ec.writer('Не понятно. Еще раз?')


    # self.ec.draw(self.room, smoke=False)
"""
    def step_move(self):
        # Сценарий с алтарем
        if self.room[self.new_cell[0]][self.new_cell[1]].entity_type == EntityTypes.ALTAR:
            self.view = [self.MESSAGE, 'Altar. Active?', self.YES]
            self.step = self.ALTAR
            return

        # Сценарий с выходом
        elif self.room[self.new_cell[0]][self.new_cell[1]].entity_type == EntityTypes.EXIT:
            if self.room.active_altar == self.room.ACTIVE_ALL_ALTAR:
                self.view = [self.MESSAGE, 'Finish?', self.YES]
                self.step = self.EXIT
                return
            else:
                self.step = self.END
                return
        # Сценарий с живой водой
        elif self.room[self.new_cell[0]][self.new_cell[1]].entity_type == EntityTypes.WATER_OF_LIFE:
            self.view = [self.MESSAGE, 'Water of life. Drink?', self.YES]
            self.step = self.WATER
            return
        # Сценарий с бандитом
        elif self.room[self.new_cell[0]][self.new_cell[1]].char_here:
            self.view = [self.MESSAGE, 'Bandit. Battle?', self.YES]
            self.step = self.BATTLE
            return
        # Сценарий с пустой ячейкой
        elif self.room[self.new_cell[0]][self.new_cell[1]].entity_type == EntityTypes.EMPTY:
            self.step = self.END
            return


    def altar_active(self, tup):
        """
        Внутренний метод altar_active активирует алтари, вызывается из метода move_hero
        :param tup:
        :return:
        """
        if self.room[tup[0]][tup[1]].entity == Building.ALTAR:
            self.room[tup[0]][tup[1]].entity = Building.ACTIVE_ALTAR
            self.room.active_altar += 1

    def end_of_step(self):
        self.step = self.MOVE
        self.room.hero_cell = self.new_cell
        self.room[self.old_cell[0]][self.old_cell[1]].hero_here = False
        self.room[self.new_cell[0]][self.new_cell[1]].hero_here = self.hero
        self.room[self.old_cell[0]][self.old_cell[1]].get_entity_type()
        self.room[self.new_cell[0]][self.new_cell[1]].get_entity_type()
        self.old_cell = self.new_cell
        self.view[0] = self.MAP


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
