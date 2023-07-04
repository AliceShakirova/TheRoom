"""Модуль описывает класс-контейнер Frame, его метод-конструктор и атрибуты"""

class Frame:
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

    # Графические объекты
    FOW = 0
    FOW_BLOCKED = 1
    ENTRY_POINT = 2
    EXIT = 3
    ALTAR = 4
    ACTIVE_ALTAR = 5
    WATER_OF_LIFE = 6
    EMPTY = 7
    BANDIT = 8
    HERO = 9

    def __init__(self, lvl=int, room=None, hero=None, mode=None, message={}, old_cell=None, new_cell=None, smoke=True,
                 battle_result=None, menu_btns=None, menu_select=None, in_game=False):
        self.level = lvl
        self.room = room
        self.hero = hero
        self.smoke = smoke
        self.mode = mode
        self.message = message
        self.old_cell = old_cell
        self.new_cell = new_cell
        self.battle_result = battle_result
        self.menu_btns = menu_btns
        self.menu_select = menu_select
        self.in_game = in_game

