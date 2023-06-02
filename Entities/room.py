

class Room:
    ACTIVE_ALL_ALTAR = 2
    rows = []
    entry_point = tuple()
    side_len = 0
    active_altar = 0
    hero_cell = None

    def __iter__(self):  # Получить объект итератора при вызове iter
        return self.rows.__iter__()

    def __getitem__(self, index):
        return self.rows[index]

    def __setitem__(self, index, value):
        self.rows[index] = value
