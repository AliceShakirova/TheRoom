"""Модуль описывает класс PyxelDisplay, позволяющий использовать графичекий движок Pyxel для отображения игры"""
import pyxel
from Controllers.khan_controller import KhanGameController
from Entities.room import Room
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

    def __init__(self, controller):
        """Initiate pyxel, set up initial game variables, and run."""

        pyxel.init(200, 140)
        # pyxel.mouse(True)
        self.controller = controller
        self.frame = self.controller.last_frame
        self.map = self.frame.room
        self.smoke = self.frame.smoke
        self.number = 0
        self.prev_inputs = None
        pyxel.run(self.update, self.draw)

    def update(self):
        """Метод update принимает введенную пользователем клавишу"""
        # if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        if self.frame.mode == self.QUIT:
            pyxel.quit()

        inputs = None
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
        if self.frame.mode in [self.MAP, self.MESSAGE]:
            pyxel.cls(0)
            y = 0
            col = 0
            for row in self.map:
                x = 0
                y += 11
                for cell in row:
                    if cell.entity_type == EntityTypes.ENTRY_POINT:
                        col = 4
                    elif self.smoke and cell.fow == FowMode.SHOWED:
                        col = 7
                    else:
                        if cell.entity_type == EntityTypes.EMPTY:
                            col = 13
                        elif cell.entity_type == EntityTypes.EXIT:
                            col = 12
                        elif cell.entity_type == EntityTypes.ALTAR:
                            col = 3
                        elif cell.entity_type == EntityTypes.ACTIVE_ALTAR:
                            col = 11
                        elif cell.entity_type == EntityTypes.WATER_OF_LIFE:
                            col = 6
                    pyxel.rect(x, y, 9, 9, col)
                    if cell.hero_here:
                        col = 15
                    elif cell.char_here and (not self.smoke or cell.fow == FowMode.REVEALED):
                        col = 8
                    pyxel.circ(x + 4, y + 4, 4, col)
                    x += 11

            hero_status = 'HERO\nHealth = {}/{}\nArmor = {}\nDamage = {}'.format(self.frame.hero.health,
                                                                                 self.frame.hero.start_health,
                                                                                 self.frame.hero.armor,
                                                                                 self.frame.hero.damage)
            pyxel.rectb(125, 7, 67, 30, 7)
            pyxel.rect(126, 8, 65, 28, 13)
            pyxel.text(128, 10, hero_status, 15)

        elif self.frame.mode == self.BATTLE:
            pyxel.cls(0)
            """message = 'BATTLE!!!'
            pyxel.rect(20, 60, 98, 48, 0)
            pyxel.text(40, 90, message, 8)
            time.sleep(1)
            """
            hero_status = 'HERO\nHealth = {}/{}\n'.format(self.frame.hero.health, self.frame.hero.start_health)
            bandit_status = 'BANDIT\nHealth = {}/{}\n'.format(self.frame.battle_result.bandit.health,
                                                              self.frame.battle_result.bandit.start_health)
            # Отрисовка бандита
            pyxel.rect(110, 7, 67, 20, 7)
            pyxel.rect(111, 8, 65, 18, 13)
            pyxel.text(113, 10, bandit_status, 15)

            pyxel.circ(140, 100, 30, 8)

            # Отрисовка героя
            pyxel.rectb(10, 7, 67, 20, 7)
            pyxel.rect(11, 8, 65, 18, 13)
            pyxel.text(13, 10, hero_status, 15)

            pyxel.circ(50, 100, 30, 15)

            score = self.frame.battle_result.score
            pyxel.rectb(60, 30, 67, 28, 7)
            pyxel.rect(61, 31, 65, 26, 13)
            y = 33
            for tup in score:
                pyxel.text(75, y, str(tup[0]), 15)
                pyxel.text(105, y, str(tup[1]), 15)
                y += 7

        if self.frame.mode == self.MESSAGE:
            string = self.frame.message[KhanGameController.MESSAGE_KEY]
            message = '{}'.format(string)
            pyxel.rectb(29, 59, 100, 50, 7)
            pyxel.rect(30, 60, 98, 48, 13)
            pyxel.text(40, 70, message, 15)
            if self.frame.message[KhanGameController.MESSAGE_MODE_KEY] == self.OK:
                # кнопка 'OK'
                pyxel.rectb(70, 90, 20, 15, 7)
                pyxel.rect(71, 91, 18, 13, 13)
                pyxel.text(75, 95, 'OK', 15)
            elif self.frame.message[KhanGameController.MESSAGE_MODE_KEY] == self.YES:
                # кнопка 'YES'
                pyxel.rectb(50, 90, 20, 15, 7)
                pyxel.rect(51, 91, 18, 13, 10)
                pyxel.text(54, 95, 'YES', 9)
                # кнопка 'NO'
                pyxel.rectb(85, 90, 20, 15, 7)
                pyxel.rect(86, 91, 18, 13, 13)
                pyxel.text(92, 95, 'NO', 15)
            else:
                # кнопка 'YES'
                pyxel.rectb(50, 90, 20, 15, 7)
                pyxel.rect(51, 91, 18, 13, 13)
                pyxel.text(54, 95, 'YES', 15)
                # кнопка 'NO'
                pyxel.rectb(85, 90, 20, 15, 7)
                pyxel.rect(86, 91, 18, 13, 10)
                pyxel.text(92, 95, 'NO', 9)
        else:
            return

        if self.frame.mode == self.QUIT:
            pyxel.rectb(29, 59, 100, 50, 7)
            pyxel.rect(30, 60, 98, 48, 13)
            pyxel.text(40, 70, 'Goodbye', 15)


if __name__ == '__main__':
    control = KhanGameController()
    control.start_new_game(2)
    display = PyxelDisplay(control)
    # control.ec_draw(display)
    pyxel.show()
