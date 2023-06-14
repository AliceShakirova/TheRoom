"""
Модуль описывает класс Cell (ячейка), из экземпляров которого состоит класс Room. Атрибуты: status
(развеян туман на клетке или нет), entity_type (описание содержимого ячейки), entity (само содержимое).
"""

from Entities.building import Building
from Entities.entity_types import EntityTypes
from Entities.fow_mode import FowMode


class Cell:
    """Класс Cell используется для взаимодействия с объектами расположенными на игровом поле

        __init__(entity, fow=FowMode.SHOWED, hero_here=False, terrain=None)
            метод-конструктор, создающий ячейку
        update_entity_type()
            обновляет entity_type в соответствии с полученными entity
    """

    fow = None                  # покрыто туманом (1) или нет (0)
    entity_type = None          # что расположено на ячейке
    entity = None               # непосредственно объект
    char_here = None            # наличие персонажа
    hero_here = None            # наличие перемещающегося героя
    blocked_by_enemy = []       # наличие бандита на соседней клетке
    # terrain = None            # ландшафт

    def __init__(self, entity, fow=FowMode.SHOWED, hero_here=False, terrain=None):
        """
        Конструктор, создающий ячейку с объектом Building внутри или пустую (Empty)
        :parameter entity: непосредственно расположенный объект
        :parameter fow: покрыто тумано (1) или нет (0)
        :parameter hero_here: наличие героя (по умолчанию False)
        :parameter terrain: ландшафт (в перспективе)
        """
        self.entity = entity
        self.fow = fow
        self.hero_here = hero_here
        self.blocked_by_enemy = []
        self.update_entity_type()
        # self.terrain = terrain

    def __setattr__(self, name, value):
        super().__setattr__(name, value)
        if name == 'entity':
            self.update_entity_type()

    def update_entity_type(self):
        """Метод update_entity_type в соответствии с атрибутом entity обновляет значения entity_type, необходимые для
        корректного отображения актуальной карты игры
        """
        if not self.entity:
            self.entity_type = EntityTypes.EMPTY
        elif self.entity == Building.ENTRY_POINT:
            self.entity_type = EntityTypes.ENTRY_POINT
        elif self.entity == Building.EXIT:
            self.entity_type = EntityTypes.EXIT
        elif self.entity == Building.ALTAR:
            self.entity_type = EntityTypes.ALTAR
        elif self.entity == Building.ACTIVE_ALTAR:
            self.entity_type = EntityTypes.ACTIVE_ALTAR
        elif self.entity == Building.WATER_OF_LIFE:
            self.entity_type = EntityTypes.WATER_OF_LIFE


# Самотестирование в случае запуска напрямую

if __name__ == '__main__':
    cell = Cell(Building.EXIT, FowMode.REVEALED)
    cell.entity = Building.ALTAR
    print(cell.fow.name, ':', cell.entity.name)
