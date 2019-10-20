import libtcodpy as libtcod

#from game_messages import Message


class Social:
    def __init__(self, bond, attacked=False):
        self.bond = bond
        self.attacked = attacked

    def lower_bond(self, amount):
        results = []

        self.bond -= amount

        if self.bond <= -10:
            results.append({'attacked': self.owner, 'bond': self.bond})

        return results

    def increase_bond(self, amount):
        results = []

        self.bond += amount

        if self.bond > -10:
            results.append({'bond': self.bond})

        return results

    @property
    def pissed(self):
        if self.bond<=-10 or self.attacked == True:
            return True
        else:
            return False


    # def talk(self, target):
    #     results = []

    #     damage = self.power - target.fighter.defense

    #     if damage > 0:
    #         results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
    #             self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
    #         results.extend(target.fighter.take_damage(damage))
    #     else:
    #         results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
    #             self.owner.name.capitalize(), target.name), libtcod.white)})

    #     return results
