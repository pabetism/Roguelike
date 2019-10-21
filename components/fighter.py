import libtcodpy as libtcod

from game_messages import Message


class Fighter:
    def __init__(self, hp, defense, power, xp=0):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp

    @property
    def max_hp(self):

        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def attack(self, target):
        results = []
        
        self.target = target

        damage = self.power - target.fighter.defense

        if damage > 0:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), libtcod.white)})
            results.extend(target.fighter.take_damage(damage))
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), libtcod.white)})
        
        if target.social:
            previously_pissed = target.social.pissed
            if previously_pissed == False:
                target.fighter.becomes_enemy()
                results.append({'message': Message('{0} is pissed!'.format(target.name.capitalize()), libtcod.red)})

        return results

    def becomes_enemy(self):
        results = []

        self.owner.social.attacked = True

        return results
    
    # def a_attack(self)
    #     lowest_hp=9999
    #     preferred_target = 0
    #     print('reg attack')
    #     if player.facing == 'Left':
    #         x = player.x + 1
    #         for y in range(player.y - 1, player.y + 2):
    #             target = get_blocking_entities_at_location(entities, x, y)
    #             if target:
    #                 if target.fighter.hp <= lowest_hp:
    #                     lowest_hp = target.fighter.hp
    #                     preferred_target = target
    #     elif player.facing == 'Right':
    #         x = player.x - 1
    #         for y in range(player.y - 1, player.y + 2):
    #             target = get_blocking_entities_at_location(entities,  x, y)
    #             if target:
    #                 if target.fighter.hp <= lowest_hp:
    #                     lowest_hp = target.fighter.hp
    #                     preferred_target = target
    #     elif player.facing == 'Up':
    #         y = player.y - 1
    #         for x in range(player.x - 1, player.x + 2):
    #             target = get_blocking_entities_at_location(entities, x, y)
    #             if target:
    #                 if target.fighter.hp <= lowest_hp:
    #                     lowest_hp = target.fighter.hp
    #                     preferred_target = target
    #     elif player.facing == 'Down':
    #         y = player.y + 1
    #         for x in range(player.x - 1, player.x + 2):
    #             target = get_blocking_entities_at_location(entities, x, y)
    #             if target:
    #                 if target.fighter.hp <= lowest_hp:
    #                     lowest_hp = target.fighter.hp
    #                     preferred_target = target
    #     if preferred_target:
    #         attack_results = player.fighter.attack(preferred_target)
    #         player_turn_results.extend(attack_results)
    #         game_state = GameStates.ENEMY_TURN
    #     else:
    #         player_turn_results.extend([{'message': Message('There is no one around to attack!', libtcod.white)}])




            
