"""Модуль описывает класс Battle, позволяющий проводить сражение между персонажами"""
from Entities.character import Character
from Entities.battle_result import BattleResult

class Battle:
    """Класс Battle используется для проведения сражений между персонажами
        ----------
        Method
            fight(char1, char2)
                проводит битву, возвращает счет, бандита и победителя

    """

    def fight(self, char1, char2):
        """Метод fight проводит битву, возвращает экземпляр класса Winner со счетом (score), бандитом (bandit) и
        победителем(winner)"""
        score = []
        while char1 and char2:
            char1.health -= (char2.damage - char1.armor)
            char2.health -= (char1.damage - char2.armor)
            if char1.health < 0:
                char1.health = 0
            if char2.health < 0:
                char2.health = 0
            score.append((char1.health, char2.health))
        if char2:
            return BattleResult(score, char2, char2)
        else:
            return BattleResult(score, char2, char1)


if __name__ == '__main__':
    a = Character(2, True)
    b = Character(1, False)
    print('Health:', a.health, b.health)
    print('Damage:', a.damage, b.damage)
    print('Armor:', a.armor, b.armor)
    battle = Battle()
    score = battle.fight(a, b)
    num = score['score']
    print(num)
    print(score['bandit'] is b)
    print(score['winner'] is a)

