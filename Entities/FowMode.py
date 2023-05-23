from enum import Enum


class FowMode(Enum):
    """
    Класс FowMode описывает две константы, соотвестствующие
    состоянию тумана в ячейке
    """
    SHOWED = 1
    REVEALED = 0
