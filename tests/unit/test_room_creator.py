from Entities.room_creator import RoomCreator
from Entities.building import Building
import unittest


class TestRoomCreator(unittest.TestCase):
    def test_positive_room(self):
        wright = {Building.ENTRY_POINT: 1, Building.EXIT: 1, Building.ALTAR: 2}
        room_creator = RoomCreator()
        test_room = RoomCreator.get_room(room_creator, 2)
        result = {Building.ENTRY_POINT: 0, Building.EXIT: 0, Building.ALTAR: 0}
        for row in test_room:
            for cell in row:
                if cell.entity:
                    result[cell.entity] += 1
        self.assertEqual(result, wright)

    "В планах: генерация с использованием сида"

if __name__ == '__main__':
    unittest.main()

