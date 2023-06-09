"""Модуль описывает класс-контейнер MenuItem, содержащее всю информацию о каждой кнопке меню. Атрибуты: text (текст,
который выводится непосредственно на кнопке при отображении), action (callback, содержащий ссылку на выбранное действие)
"""


class MenuItem:
    """Класс MenuItem используется для создания объектов с параметрами, соответствтующими уровню
        ----------
        Attributes
            text - str, текст, отображемый поверх кнопки
            action - callback, действие, выполняемое при нажатии этой кнопки
        ----------
        Methods
            __init__(text, action=None)
                метод-конструктор, создающий кнопку"""

    def __init__(self, text, action=None):
        self.text = text
        self.action = action

