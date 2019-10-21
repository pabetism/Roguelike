import libtcodpy as libtcod

from game_messages import Message

from game_states import GameStates

from render_functions import RenderOrder


def kill_player(player, text_color, char_color):
    player.char = '%'
    player.color = char_color

    return Message('You died!', text_color), GameStates.PLAYER_DEAD


def kill_monster(monster, text_color, char_color):
    death_message = Message('{0} is dead!'.format(monster.name.capitalize()), text_color)

    monster.char = '%'
    monster.color = char_color
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
