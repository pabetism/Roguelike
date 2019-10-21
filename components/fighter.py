import libtcodpy as libtcod

from game_messages import Message
from entity import get_blocking_entities_in_rectangle, remove_entity_fron_sublist_of_entities

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
    
    def forward_attack(self, entities):
        self.entities = entities
        results = []
        lowest_hp=9999
        preferred_npc_target = 0
        preferred_target = 0

        if self.owner.facing == 'Left':
            targets_in_range = get_blocking_entities_in_rectangle(entities, self.owner.x + 1, self.owner.y, 1, 3)
            targets_in_range = remove_entity_fron_sublist_of_entities(self.owner, targets_in_range)
            for target in targets_in_range:
                if target.fighter.hp <= lowest_hp:
                    lowest_hp = target.fighter.hp
                    preferred_npc_target = target
                    if not target.social:
                        preferred_target = target        
        elif self.owner.facing == 'Right':
            targets_in_range = get_blocking_entities_in_rectangle(entities, self.owner.x - 1, self.owner.y, 1, 3)
            targets_in_range = remove_entity_fron_sublist_of_entities(self.owner, targets_in_range)
            for target in targets_in_range:
                if target.fighter.hp <= lowest_hp:
                    lowest_hp = target.fighter.hp
                    preferred_npc_target = target
                    if not target.social:
                        preferred_target = target        
        elif self.owner.facing == 'Up':
            targets_in_range = get_blocking_entities_in_rectangle(entities, self.owner.x, self.owner.y - 1, 3, 1)
            targets_in_range = remove_entity_fron_sublist_of_entities(self.owner, targets_in_range)
            for target in targets_in_range:
                if target.fighter.hp <= lowest_hp:
                    lowest_hp = target.fighter.hp
                    preferred_npc_target = target
                    if not target.social:
                        preferred_target = target        
        elif self.owner.facing == 'Down':
            targets_in_range = get_blocking_entities_in_rectangle(entities, self.owner.x, self.owner.y + 1, 3, 1)
            targets_in_range = remove_entity_fron_sublist_of_entities(self.owner, targets_in_range)
            for target in targets_in_range:
                if target.fighter.hp <= lowest_hp:
                    lowest_hp = target.fighter.hp
                    preferred_npc_target = target
                    if not target.social:
                        preferred_target = target = target
        if preferred_target:
            attack_results = self.owner.fighter.attack(preferred_target)
            results.extend(attack_results)
        elif preferred_npc_target:
            attack_results = self.owner.fighter.attack(preferred_npc_target)
            results.extend(attack_results)
        else:
            results.extend([{'message': Message('There is no one around to attack!', libtcod.white)}])

        return results

    def circle_attack(self, entities):
        self.entities = entities
        results = []
        lowest_hp=9999
        preferred_npc_target = 0
        preferred_target = 0
        
        targets_in_range = get_blocking_entities_in_rectangle(entities, self.owner.x, self.owner.y, 3, 3)
        targets_in_range = remove_entity_fron_sublist_of_entities(self.owner, targets_in_range)
        for target in targets_in_range:
            if target.fighter.hp <= lowest_hp:
                lowest_hp = target.fighter.hp
                preferred_npc_target = target
                if not target.social:
                    preferred_target = target

        if preferred_target:
            attack_results = self.owner.fighter.attack(preferred_target)
            results.extend(attack_results)
        elif preferred_npc_target:
            attack_results = self.owner.fighter.attack(preferred_npc_target)
            results.extend(attack_results)
        else:
            results.extend([{'message': Message('There is no one around to attack!', libtcod.white)}])

        return results







            
