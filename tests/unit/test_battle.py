"""Тест-комплект тестирует методы класса Battle"""

from Entities.character import Character
from Entities.battle import Battle
import unittest


class TestBattle(unittest.TestCase):
    def test_fight_score(self):
        """Тест проверяет, что при обработке вычисляется верный счет"""
        correct_score = [(39, 12), (38, 4), (37, 0)]
        hero = Character(2, True)
        bandit = Character(1, False)
        battle = Battle()
        result = battle.fight(hero, bandit)

        self.assertEqual(result.score, correct_score)

    def test_fight_bandit(self):
        """Тест проверяет, что по ключу bandit располагается именно бандит"""
        hero = Character(2, True)
        bandit = Character(1, False)
        battle = Battle()
        result = battle.fight(hero, bandit)
        self.assertIs(result.bandit, bandit)

    def test_fight_winner_hero(self):
        """Тест проверяет, что по ключу winner располагается победитель, в данном случае hero"""
        hero = Character(2, True)
        bandit = Character(1, False)
        battle = Battle()
        result = battle.fight(hero, bandit)
        self.assertIs(result.winner, hero)

    def test_fight_winner_bandit(self):
        """Тест проверяет, что по ключу winner располагается победитель, в данном случае hero"""
        hero = Character(1, True)
        bandit = Character(2, False)
        battle = Battle()
        result = battle.fight(hero, bandit)
        self.assertIs(result.winner, bandit)

    def test_fight_winner_equal(self):
        """Тест проверяет, что при равных силах двух персонажей по ключу winner располагается победитель, в данном
        случае hero"""
        hero = Character(2, True)
        bandit = Character(2, False)
        battle = Battle()
        result = battle.fight(hero, bandit)
        self.assertIs(result.winner, hero)

if __name__ == '__main__':
    unittest.main()

