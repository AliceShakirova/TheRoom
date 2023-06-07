import unittest
from Controllers.khan_controller import KhanGameController
from Entities.cell import Cell
from Entities.fow_mode import FowMode
from Entities.building import Building


class TestKhanGameController(unittest.TestCase):
    def test_get_cell_to_move(self):
        "Тест проверяет, что при всех возможных кнопках новая ячейка для движения героя вычисляется корректно"
        game_controller = KhanGameController()
        self.buttons = [KhanGameController.ENTER, KhanGameController.UP, KhanGameController.DOWN,
                        KhanGameController.RIGHT, KhanGameController.LEFT]
        self.start_cell = (5, 7)
        correct_cell = {self.start_cell: (5, 7), KhanGameController.UP: (4, 7), KhanGameController.DOWN: (6, 7),
                        KhanGameController.RIGHT: (5, 8), KhanGameController.LEFT: (5, 6),
                        KhanGameController.ENTER: None}
        result = {self.start_cell: (5, 7)}
        for button in self.buttons:
            game_controller.old_cell = self.start_cell
            game_controller.get_cell_to_move(button)
            result[button] = game_controller.new_cell
        self.assertEqual(result, correct_cell)

    def test_altar_activate(self):
        "Тест проверяет, что метод altar_activate корректно изменяет атрибуты ячейки Cell"
        controller = KhanGameController()
        controller.start_new_game(2)
        test_cell = (3, 3)
        controller.room[test_cell[0]][test_cell[1]] = Cell(entity=Building.ALTAR, fow=FowMode.SHOWED)
        controller.altar_activate(test_cell)
        self.assertIs(controller.room[test_cell[0]][test_cell[1]].entity, Building.ACTIVE_ALTAR)
