"""Модуль описывает класс-контейнер BattleResult"""


class BattleResult:
    """Класс BattleResult хранит результаты проведенного боя
    __________
    Attributes
    score : list, список кортежей, хранящих health персонажей на каждом раунде боя
    bandit : object class Character, хранит в себе бандита
    winner : object class Character, хранит в себе победителя, бандита или героя"""
    def __init__(self, score, bandit, winner):
        self.score = score
        self.bandit = bandit
        self.winner = winner
