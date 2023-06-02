from Entities.character import Character


class Battle:

    def fight(self, char1, char2):
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
            return {'score': score, 'bandit': char2, 'winner': char2}
        else:
            return {'score': score, 'bandit': char2, 'winner': char1}


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

