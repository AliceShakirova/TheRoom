import time

import pyxel
from Controllers.khan_controller import KhanGameController
from Entities.room_class import Room, EntityTypes, FowMode


class PyxelDisplay:
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    ENTER = 5

    # Режимы работы метода draw
    MENU = 0
    MAP = 2
    MESSAGE = 3
    BATTLE = 4
    QUIT = 5

    # Режимы диалогого окна
    YES = 0
    NO = 1
    OK = 2

    view = None

    def __init__(self, controller):
        """Initiate pyxel, set up initial game variables, and run."""

        pyxel.init(200, 140)
        # pyxel.mouse(True)
        self.controller = controller
        self.map = self.controller.room
        self.smoke = self.controller.smoke
        pyxel.run(self.update, self.draw)

    def update(self):
        '''
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            return
        '''

        self.view = self.controller.view
        if self.view[0] == self.MAP:
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
            self.controller.process_key(inputs)

        elif self.view[0] == self.MESSAGE:
            if self.view[2] == self.OK:
                if pyxel.btn(pyxel.KEY_KP_ENTER) or pyxel.btn(pyxel.KEY_SPACE):
                    inputs = self.ENTER
                    self.controller.process_messagebox_key(inputs)
            if self.view[2] == self.YES:
                if pyxel.btn(pyxel.KEY_KP_ENTER) or pyxel.btn(pyxel.KEY_SPACE):
                    inputs = self.ENTER
                    self.controller.process_messagebox_key(inputs, select=self.YES)
                elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D) or \
                        pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
                    inputs = self.RIGHT
                    self.controller.process_messagebox_key(inputs, select=self.YES)
            if self.view[2] == self.NO:
                if pyxel.btn(pyxel.KEY_KP_ENTER) or pyxel.btn(pyxel.KEY_SPACE):
                    inputs = self.ENTER
                    self.controller.process_messagebox_key(inputs, select=self.NO)
                elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A) or \
                         pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
                    inputs = self.LEFT
                    self.controller.process_messagebox_key(inputs, select=self.NO)

        elif self.view[0] == self.MENU:
            if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W) or \
                    pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
                inputs = self.UP
            elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S) or \
                    pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
                inputs = self.DOWN
            if pyxel.btn(pyxel.KEY_KP_ENTER) or pyxel.btn(pyxel.KEY_SPACE):
                inputs = self.ENTER
            self.controller.process_key(inputs)

        elif self.view[0] == self.BATTLE:
            if pyxel.btn(pyxel.KEY_KP_ENTER) or pyxel.btn(pyxel.KEY_SPACE):
                string = '{} win'.format(self.view[1]['winner'])
                self.view = [self.MESSAGE, string, self.OK]
                inputs = self.ENTER
            self.controller.process_messagebox_key(inputs)

        elif self.view[0] == self.QUIT:
            pyxel.quit()

    def draw(self):
        if self.view[0] in [self.MAP, self.MESSAGE]:
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

            hero_status = 'HERO\nHealth = {}/{}\nArmor = {}\nDamage = {}'.format(self.controller.hero.health, self.controller.start_health, self.controller.hero.armor, self.controller.hero.damage)
            pyxel.rectb(125, 7, 67, 30, 7)
            pyxel.rect(126, 8, 65, 28, 13)
            pyxel.text(128, 10, hero_status, 15)

        elif self.view[0] == self.BATTLE:
            pyxel.cls(13)
            message = 'BATTLE!!!'
            pyxel.rect(20, 60, 98, 48, 0)
            pyxel.text(40, 90, message, 8)
            time.sleep(1)

            hero_status = 'HERO\nHealth = {}/{}\n'.format(self.controller.hero.health, self.controller.start_health)
            pyxel.rectb(125, 7, 67, 30, 7)
            pyxel.rect(126, 8, 65, 28, 13)
            pyxel.text(128, 10, hero_status, 15)

            bandit_status = 'BANDIT\nHealth = {}/{}\n'.format(self.view[1]['bandit'].health,
                                                              self.view[1]['bandit'].start_health)
            pyxel.rectb(25, 7, 67, 30, 7)
            pyxel.rect(26, 8, 65, 28, 13)
            pyxel.text(28, 10, bandit_status, 15)

        if self.view[0] == self.MESSAGE:
            string = self.view[1]
            message = '{}'.format(string)
            pyxel.rectb(29, 59, 100, 50, 7)
            pyxel.rect(30, 60, 98, 48, 13)
            pyxel.text(40, 70, message, 15)
            if self.view[2] == self.OK:
                # кнопка 'OK'
                pyxel.rectb(70, 90, 20, 15, 7)
                pyxel.rect(71, 91, 18, 13, 13)
                pyxel.text(75, 95, 'OK', 15)
            elif self.view[2] == self.YES:
                #кнопка 'YES'
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

        if self.view[0] == self.QUIT:
            pyxel.rectb(29, 59, 100, 50, 7)
            pyxel.rect(30, 60, 98, 48, 13)
            pyxel.text(40, 70, 'Goodbye', 15)

if __name__ == '__main__':
    control = KhanGameController()
    control.start_new_game(2)
    display = PyxelDisplay(control)
    # control.ec_draw(display)
    pyxel.show()
