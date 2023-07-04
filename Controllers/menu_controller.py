"""Модуль описывает класс Menu, отвечающий за главное и игровое меню"""
from Entities.menu_item import MenuItem


class Menu:
    """Класс Menu обрабатывает внеигровую логику. На вход передаются коллбэки из основного контроллера игры для каждой
    из кнопок
    ----------
    Attributes
        lvl - int, уровень комнаты, от которого зависят размеры комнаты, количество и параметры персонажей
        select - int, индекс, указывающий выбранную в данный момент кнопку меню
        in_game - bool, флаг, отображающий запущена игра в данный момент или нет
        menu_btns - list, набор кнопок меню для отображения
    -------
    Methods
        __init__(cb_start_new_game, cb_quit_the_game, cb_return_to_level, cb_leave_the_level)
            метод-конструктор, задающий начальные параметры меню, получает коллбэки на вход
        process_key(btn):
            метод обрабатывает нажатую кнопку, а затем запускает выбранное пользователем действие
    """

    # Кнопки управления
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    ENTER = 5

    select = None

    def __init__(self, cb_start_new_game, cb_quit_the_game, cb_return_to_level, cb_leave_the_level):
        btn_new_game = MenuItem('НОВАЯ ИГРА', cb_start_new_game)
        btn_load_game = MenuItem('ЗАГРУЗИТЬ ИГРУ')
        btn_settings = MenuItem('НАСТРОЙКИ')
        btn_quit = MenuItem('ВЫЙТИ ИЗ ИГРЫ', cb_quit_the_game)
        btn_return = MenuItem('ПРОДОЛЖИТЬ', cb_return_to_level)
        btn_save_game = MenuItem('СОХРАНИТЬ ИГРУ')
        btn_leave_the_level = MenuItem('ЗАВЕРШИТЬ ТЕКУЩУЮ ИГРУ', cb_leave_the_level)
        self.main_menu = [btn_new_game, btn_load_game, btn_settings, btn_quit]
        self.game_menu = [btn_return, btn_save_game, btn_settings, btn_leave_the_level]
        self.select = 0
        self.in_game = False
        self.menu_btns = self.main_menu
        self.lvl = 1

    def process_key(self, btn):
        """Метод process_key обрабатывет нажатую пользователем клавишу и выполняет выбранное действие
        :parameter btn: int, нажатая клавиша"""
        self.menu_btns = None
        if self.in_game:
            self.menu_btns = self.game_menu
        else:
            self.menu_btns = self.main_menu
        if btn == self.UP:
            if self.select > 0:
                self.select -= 1
            else:
                pass
        elif btn == self.DOWN:
            if (self.select + 1) < len(self.menu_btns):
                self.select += 1
            else:
                pass
        elif btn == self.ENTER:
            if self.menu_btns[self.select].action:
                # Новая игра
                if self.menu_btns[self.select] == self.main_menu[0]:
                    self.menu_btns[self.select].action(self.lvl)
                    self.in_game = True
                # Загрузить игру
                elif self.menu_btns[self.select] == self.main_menu[1]:
                    pass
                # Настройки
                elif self.menu_btns[self.select] == self.main_menu[2]:
                    pass
                # Выйти из игры
                elif self.menu_btns[self.select] == self.main_menu[3]:
                    self.menu_btns[self.select].action()
                # Продолжить
                elif self.menu_btns[self.select] == self.game_menu[0]:
                    self.menu_btns[self.select].action()
                # Сохранить игру
                elif self.menu_btns[self.select] == self.game_menu[1]:
                    pass
                # Настройки
                elif self.menu_btns[self.select] == self.game_menu[2]:
                    pass
                # Покинуть уровень
                elif self.menu_btns[self.select] == self.game_menu[3]:
                    self.menu_btns[self.select].action()
            else:
                pass



