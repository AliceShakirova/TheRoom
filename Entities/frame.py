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

    def __init__(self, lvl=int, room=None, hero=None, mode=None, message={}, old_cell=None, new_cell=None, smoke=True,
                 winner=None):

    # В дальнейшем этот атрибут будет браться из меню или по прохождении уровней обновляться, пока так
        self.level = lvl
        self.room = room
        self.hero = hero
        self.smoke = smoke
        self.mode = mode
        self.message = message
        self.old_cell = old_cell
        self.new_cell = new_cell
        self.winner = winner
