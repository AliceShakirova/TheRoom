"""Модуль описывает класс PyxelDisplay, позволяющий использовать графичекий движок Pyxel для отображения игры"""
import os

import pyxel
from pyxelunicode import PyxelUnicode
from Controllers.khan_controller import KhanGameController
from Entities.frame import Frame
from Entities.entity_types import EntityTypes
from Entities.fow_mode import FowMode


class PyxelDisplay:
    """Класс PyxelDisplay используется для взаимодействия основного контроллера с графическим движком
    ----------
    Attributes
        controller : obj class KhanGameController, основной контроллер игры
        frame : obj class Frame, содержит последние изменения в игре
        map : obj class Room,  содержит основную карту
        smoke : bool, режим отображения тумана
        number : int, число нажатий на клавишу
        prev_inputs : int, предыдущая нажатая клавиша
    -------
    Methods
        __init__(controller)
            метод-конструктор, привязывающий основной контроллер игры
        update()
            метод, принимающий введенную пользователем клавишу
        draw()
            метод, отрисовывающий конкретный кадр
    """
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    ENTER = 5

    # Режимы работы метода draw
    MENU = 0
    MAP = 1
    MESSAGE = 2
    BATTLE = 3
    QUIT = 4

    # Режимы диалогого окна
    YES = 0
    NO = 1
    OK = 2

    # initial_info
    init_width = 400
    init_height = 280
    font_size = 12
    side_of_cell = (init_width/20) - 1  # -1, чтобы был центр, где был бы центр круга или крестика
    circ_radius = (side_of_cell - 5) / 2  # чтобы вписать в квадрат и осталось еще 2 пикселя с каждой стороны
    start_next_cell = side_of_cell + 4
    # отрисовка статуса
    status_rect_x = 256
    status_rect_y = 18
    status_rectb_x = status_rect_x - 1
    status_rectb_y = status_rect_y - 1
    status_text_x = status_rect_x + 2
    status_text_y = status_rect_y + 4
    status_rect_width = 100
    status_rect_height = 50
    status_rectb_width = status_rect_width + 2
    status_rectb_height = status_rect_height + 2
    # отрисовка messagebox
    all_btn_rect_width = 40
    all_btn_rect_height = 13
    mb_rect_x = init_height // 8
    mb_rect_y = 100
    mb_rectb_x = mb_rect_x - 1
    mb_rectb_y = mb_rect_y - 1
    mb_rect_width = 140
    mb_rectb_width = mb_rect_width + 2
    # mb_rectb_height = mb_rect_height + 2
    mb_text_x = mb_rect_x + 8
    mb_text_y = mb_rect_y + 10
    mb_text_max = mb_rect_width // 7  # примерно 20 символов
    # отрисовка кнопок
    ok_rect_x = mb_rect_x + 50
    ok_text_x = ok_rect_x + 14
    ok_rectb_x = ok_rect_x - 1
    yes_rect_x = mb_rect_x + 25
    yes_text_x = yes_rect_x + 15
    yes_rectb_x = yes_rect_x - 1
    no_rect_x = mb_rect_x + 75
    no_text_x = no_rect_x + 13
    no_rectb_x = no_rect_x - 1
    # отрисовка битвы
    battle_status_rect_width = 100
    battle_status_rectb_width = battle_status_rect_width + 2
    battle_status_rect_height = 30
    battle_status_rectb_height = battle_status_rect_height + 2
    battle_status_rect_y = 8
    battle_status_rectb_y = battle_status_rect_y - 1
    battle_status_text_y = battle_status_rect_y + 3
    # статус героя
    battle_hero_status_rect_x = 40
    battle_hero_status_rectb_x = battle_hero_status_rect_x - 1
    battle_hero_status_text_x = battle_hero_status_rect_x + 3
    # статус бандита
    battle_bandit_status_rect_x = 250
    battle_bandit_status_rectb_x = battle_bandit_status_rect_x - 1
    battle_bandit_status_text_x = battle_bandit_status_rect_x + 3
    # отрисовка счета
    battle_score_rect_width = 60
    battle_score_rectb_width = battle_score_rect_width + 2

    battle_score_rect_x = ((battle_hero_status_rect_x + battle_status_rectb_width + battle_bandit_status_rect_x)
                           // 2) - (battle_score_rectb_width // 2)
    battle_score_rect_y = battle_status_rect_y + battle_status_rectb_height + 10
    battle_score_rectb_x = battle_score_rect_x - 1
    battle_score_rectb_y = battle_score_rect_y - 1
    battle_score_text_x = battle_score_rect_x + 8
    battle_score_text_y = battle_score_rect_y + 3

    def __init__(self, controller):
        """Initiate pyxel, set up initial game variables, and run."""

        pyxel.init(PyxelDisplay.init_width, PyxelDisplay.init_height)
        # pyxel.mouse(True)
        self.controller = controller
        self.frame = self.controller.last_frame
        self.map = self.frame.room
        self.smoke = self.frame.smoke
        self.number = 0
        self.prev_inputs = None
        font_path_misc = "..\\Fonts\\misc-fixed.ttf"
        font_path_pyxel = "..\\Fonts\\Pixel-UniCode.ttf"
        font_path_arial = os.path.join(os.environ['WINDIR'], "Fonts\\arial.ttf")
        self.pyuni = PyxelUnicode(font_path_misc, self.font_size, 1)
        pyxel.run(self.update, self.draw)

    def update(self):
        """Метод update принимает введенную пользователем клавишу"""
        # if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        if self.frame.mode == self.QUIT:
            pyxel.quit()

        none = None
        inputs = none
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W) or \
                pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            inputs = self.UP
        elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S) or \
                pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            inputs = self.DOWN
        elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or \
                pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            inputs = self.LEFT
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or \
                pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            inputs = self.RIGHT
        elif pyxel.btn(pyxel.KEY_KP_ENTER) or pyxel.btn(pyxel.KEY_SPACE):
            inputs = self.ENTER

        if inputs:
            self.prev_inputs = inputs
            self.number += 1
            if self.number > 3 and self.prev_inputs == inputs:
                self.number = 0
                self.controller.process_key(inputs)
        else:
            self.number = 0

    def draw(self):
        """Метод draw отрисовывает конкретный кадр"""
        self.frame = self.controller.get_current_frame()
        self.map = self.frame.room
        if self.frame.mode in [self.MAP, self.MESSAGE]:
            self.draw_map()

        elif self.frame.mode == self.BATTLE:
            self.draw_battle()

        if self.frame.mode == self.MESSAGE:
            self.draw_messagebox(self.frame.message[KhanGameController.MESSAGE_KEY],
                                 self.frame.message[KhanGameController.MESSAGE_MODE_KEY])
        else:
            return

        if self.frame.mode == self.QUIT:
            pyxel.rectb(29, 59, 100, 50, 7)
            pyxel.rect(30, 60, 98, 48, 13)
            pyxel.text(40, 70, 'Goodbye', 15)

    def draw_map(self):
        """Метод описывает непосредственную отрисовку актуальной карты"""
        pyxel.cls(0)
        y = 0
        for row in self.map:
            x = 0
            y += self.start_next_cell
            for cell in row:
                col0 = 0
                col1 = 0
                if cell.building == Frame.ENTRY_POINT:
                    col0 = 4
                elif self.smoke and cell.building == Frame.FOW:
                    col0 = 7
                    col1 = 8
                else:
                    if cell.building == Frame.EMPTY:
                        col0 = 13
                    elif cell.building == Frame.EXIT:
                        col0 = 12
                    elif cell.building == Frame.ALTAR:
                        col0 = 3
                    elif cell.building == Frame.ACTIVE_ALTAR:
                        col0 = 11
                    elif cell.building == Frame.WATER_OF_LIFE:
                        col0 = 6
                pyxel.rect(x, y, self.side_of_cell, self.side_of_cell, col0)
                if cell.unit == Frame.HERO:
                    col0 = 15
                if cell.unit == Frame.BANDIT and not cell.building == Frame.FOW:
                    col0 = 8
                pyxel.circ(x + 9, y + 9, self.circ_radius, col0)
                if cell.unit == Frame.FOW_BLOCKED:
                    pyxel.line(x + 1, y + 1, x + 17, y + 17, col1)
                    pyxel.line(x + 17, y + 1, x + 1, y + 17, col1)
                x += self.start_next_cell
        hero_status = 'ГЕРОЙ\nЗдоровье = {}/{}\nБроня = {}\nУрон = {}'.format(self.frame.hero.health,
                                                                              self.frame.hero.start_health,
                                                                              self.frame.hero.armor,
                                                                              self.frame.hero.damage)
        pyxel.rectb(self.status_rectb_x, self.status_rectb_y, self.status_rectb_width, self.status_rectb_height, 7)
        pyxel.rect(self.status_rect_x, self.status_rect_y, self.status_rect_width, self.status_rect_height, 13)
        self.pyuni.text(self.status_text_x, self.status_text_y, hero_status, 15)

    def draw_battle(self):
        """Метод описывает рассчет внутренних переменных и непосредственную отрисовку боя между героем и бандитом"""
        pyxel.cls(0)
        hero_status = 'ГЕРОЙ\nЗДОРОВЬЕ = {}/{}\n'.format(self.frame.hero.health, self.frame.hero.start_health)
        bandit_status = 'БАНДИТ\nЗДОРОВЬЕ = {}/{}\n'.format(self.frame.battle_result.bandit.health,
                                                            self.frame.battle_result.bandit.start_health)
        # Отрисовка бандита
        pyxel.rectb(self.battle_bandit_status_rectb_x, self.battle_status_rectb_y, self.battle_status_rectb_width,
                    self.battle_status_rectb_height, 7)
        pyxel.rect(self.battle_bandit_status_rect_x, self.battle_status_rect_y, self.battle_status_rect_width,
                   self.battle_status_rect_height, 13)
        self.pyuni.text(self.battle_bandit_status_text_x, self.battle_status_text_y, bandit_status, 15)
        pyxel.circ(self.battle_bandit_status_rect_x + (self.battle_status_rect_width // 2), 200, 70, 8)
        # Отрисовка героя
        pyxel.rectb(self.battle_hero_status_rectb_x, self.battle_status_rectb_y, self.battle_status_rectb_width,
                    self.battle_status_rectb_height, 7)
        pyxel.rect(self.battle_hero_status_rect_x, self.battle_status_rect_y, self.battle_status_rect_width,
                   self.battle_status_rect_height, 13)
        self.pyuni.text(self.battle_hero_status_text_x, self.battle_status_text_y, hero_status, 15)
        pyxel.circ(self.battle_hero_status_rect_x + (self.battle_status_rect_width // 2), 200, 70, 15)

        score = self.frame.battle_result.score
        battle_score_rectb_width = self.battle_score_rect_width + 2
        battle_score_rect_height = len(score) * 12 + 2
        battle_score_rectb_height = battle_score_rect_height + 2
        pyxel.rectb(self.battle_score_rectb_x, self.battle_score_rectb_y, battle_score_rectb_width,
                    battle_score_rectb_height, 7)
        pyxel.rect(self.battle_score_rect_x, self.battle_score_rect_y, self.battle_score_rect_width,
                   battle_score_rect_height, 13)
        y = self.battle_score_text_y
        for tup in score:
            self.pyuni.text(self.battle_score_text_x, y, str(tup[0]), 15)
            self.pyuni.text(self.battle_score_text_x + 30, y, str(tup[1]), 15)
            y += 12

    def draw_messagebox(self, message, key):
        """Метод описывает рассчет внутренних переменных и непосредственную отрисовку messagebox"""
        message = self.get_formated_message(message)
        # отрисовка кнопок messagebox
        mb_rect_height = len(message) * 15 + self.all_btn_rect_height + 20
        mb_rectb_height = mb_rect_height + 2
        all_btn_rect_y = self.mb_rect_y + mb_rect_height - 20
        all_btn_rectb_y = all_btn_rect_y - 1
        all_btn_rectb_width = self.all_btn_rect_width + 2
        all_btn_rectb_height = self.all_btn_rect_height + 2
        all_btn_text_y = all_btn_rect_y + 2
        pyxel.rectb(self.mb_rectb_x, self.mb_rectb_y, self.mb_rectb_width, mb_rectb_height, 7)
        pyxel.rect(self.mb_rect_x, self.mb_rect_y, self.mb_rect_width, mb_rect_height, 13)
        y = self.mb_text_y
        for string in message:
            self.pyuni.text(self.mb_text_x, y, string, 15)
            y += 12
        if key == self.OK:
            # кнопка 'OK'
            pyxel.rectb(self.ok_rectb_x, all_btn_rectb_y, all_btn_rectb_width, all_btn_rectb_height, 7)
            pyxel.rect(self.ok_rect_x, all_btn_rect_y, self.all_btn_rect_width, self.all_btn_rect_height, 13)
            self.pyuni.text(self.ok_text_x, all_btn_text_y, 'OK', 15)
        elif key == self.YES:
            # кнопка 'ДА'
            pyxel.rectb(self.yes_rectb_x, all_btn_rectb_y, all_btn_rectb_width, all_btn_rectb_height, 7)
            pyxel.rect(self.yes_rect_x, all_btn_rect_y, self.all_btn_rect_width, self.all_btn_rect_height, 10)
            self.pyuni.text(self.yes_text_x, all_btn_text_y, 'ДА', 9)
            # кнопка 'НЕТ'
            pyxel.rectb(self.no_rectb_x, all_btn_rectb_y, all_btn_rectb_width, all_btn_rectb_height, 7)
            pyxel.rect(self.no_rect_x, all_btn_rect_y, self.all_btn_rect_width, self.all_btn_rect_height, 13)
            self.pyuni.text(self.no_text_x, all_btn_text_y, 'НЕТ', 15)
        elif key == self.NO:
            # кнопка 'ДА'
            pyxel.rectb(self.yes_rectb_x, all_btn_rectb_y, all_btn_rectb_width, all_btn_rectb_height, 7)
            pyxel.rect(self.yes_rect_x, all_btn_rect_y, self.all_btn_rect_width, self.all_btn_rect_height, 13)
            self.pyuni.text(self.yes_text_x, all_btn_text_y, 'ДА', 15)
            # кнопка 'НЕТ'
            pyxel.rectb(self.no_rectb_x, all_btn_rectb_y, all_btn_rectb_width, all_btn_rectb_height, 7)
            pyxel.rect(self.no_rect_x, all_btn_rect_y, self.all_btn_rect_width, self.all_btn_rect_height, 10)
            self.pyuni.text(self.no_text_x, all_btn_text_y, 'НЕТ', 9)

    def get_formated_message(self, string):
        """Метод динамически вычисляет расположение слов строки в messagebox"""
        string_to_draw = []
        pre_string = ''
        for string in string.split(' '):
            if len(pre_string + string) < self.mb_text_max:
                pre_string = pre_string + string + ' '
            else:
                string_to_draw.append(pre_string.center(self.mb_text_max))
                pre_string = string + ' '
        string_to_draw.append(pre_string.center(self.mb_text_max))
        return string_to_draw


if __name__ == '__main__':
    control = KhanGameController()
    control.start_new_game(2)
    display = PyxelDisplay(control)
    # control.ec_draw(display)
    pyxel.show()
