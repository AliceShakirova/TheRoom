import pyxel

class App:
    def __init__(self):
        pyxel.init(200, 120)
        pyxel.mouse(True)
        self.x = 0
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.x = (self.x + 2)

    def draw(self):
        pyxel.cls(6)
        pyxel.rect(self.x, 0, 8, 8, 1)


App()

if __name__ == '__main__':
    App()