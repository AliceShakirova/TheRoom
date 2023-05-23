"""
Модуль описывает класс Character, позволяющий создать основного персонажа и персонажей противников
"""


class Character:
    """Класс Character используется для создания объектов с параметрами,
    соответствтующими уровню

    Основное применение - в контроллере игры для создания основного
    персонажа и бандитов

    Attributes
    ----------
    health : int
        величина, отвечающая за здоровье персонажа
    armor : int
        величина, отвечающая за броню
    damage : int
        величина, отвечающая за наносимый противнику урон
    hero : bool
        флаг, отличающий основного персонажа и противников
    """
    ENEMY_COUNT_MULTIPLIER = 5
    health, armor, damage = 0, 0, 0
    hero = None

    def __init__(self, lvl, hero=True):
        self.health = 20 * lvl
        self.armor = 2 * lvl
        self.damage = 5 * lvl
        self.hero = hero
        self.start_health = self.health

    def __bool__(self):
        return self.health > 0


""" Принято решение перенести эти вычисления в контроллер
class Bandit(Character):
    might = {0:1, 1:2, 2:4, 3:9, 4:20}
    def __init__(self, lvl, power):
        Character.__init__(self, lvl)
        self.health *= Bandit.might[power]
        self.damage *= Bandit.might[power]
        if power != 0:
            self.armor *= Bandit.might[power]

"""
if __name__ == '__main__':
    hero = Character(2)
    print('Основной персонаж:', hero.health, hero.armor, hero.damage)
