from Entities.character import Character
from Entities.battle import Battle
import unittest


class TestBattle(unittest.TestCase):
    def test_fight_score(self):
        "Тест проверяет, что при обработке вычисляется верный счет"
        wright = [(39, 12), (38, 4), (37, 0)]
        hero = Character(2, True)
        bandit = Character(1, False)
        battle = Battle()
        result = battle.fight(hero, bandit)['score']

        self.assertEqual(result, wright)

    def test_fight_bandit(self):
        "Тест проверяет, что по ключу bandit располагается именно бандит"
        hero = Character(2, True)
        bandit = Character(1, False)
        battle = Battle()
        result = battle.fight(hero, bandit)['bandit']
        self.assertIs(result, bandit)

    def test_fight_winner_hero(self):
        "Тест проверяет, что по ключу winner располагается победитель, в данном случае hero"
        hero = Character(2, True)
        bandit = Character(1, False)
        battle = Battle()
        result = battle.fight(hero, bandit)['winner']
        self.assertIs(result, hero)

    def test_fight_winner_bandit(self):
        "Тест проверяет, что по ключу winner располагается победитель, в данном случае hero"
        hero = Character(1, True)
        bandit = Character(2, False)
        battle = Battle()
        result = battle.fight(hero, bandit)['winner']
        self.assertIs(result, bandit)

    def test_fight_winner_equal(self):
        "Тест проверяет, что при равных силах двух персонажей по ключу winner располагается победитель, в данном случае hero"
        hero = Character(2, True)
        bandit = Character(2, False)
        battle = Battle()
        result = battle.fight(hero, bandit)['winner']
        self.assertIs(result, hero)

if __name__ == '__main__':
    unittest.main()

