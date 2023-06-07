from Entities.cell import Cell
from Entities.fow_mode import FowMode
from Entities.building import Building
from Entities.entity_types import EntityTypes
import unittest


class TestCell(unittest.TestCase):
    def test_get_entity_type(self):
        "Тест проверяет работу метода get_entity_type, конкретно, что при изменении здания, entity_type меняется корректно"
        cell1 = Cell(Building.ALTAR, FowMode.REVEALED)
        cell1.get_entity_type()
        correct_ent_type = EntityTypes.ACTIVE_ALTAR
        cell1.entity = Building.ACTIVE_ALTAR
        cell1.get_entity_type()
        result = cell1.entity_type
        self.assertEqual(correct_ent_type, result)


if __name__ == '__main__':
    unittest.main()
