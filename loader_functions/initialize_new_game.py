import libtcodpy as libtcod

from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.social import Social

from entity import Entity

from equipment_slots import EquipmentSlots

from game_messages import MessageLog

from game_states import GameStates

from map_objects.game_map import GameMap

from render_functions import RenderOrder


def get_constants():
    window_title = 'Basic Roguelike'

    screen_width = 100
    screen_height = 80

    bar_width = 20
    panel_height = 20
    panel_y = screen_height - panel_height - 1

    hud_width = 15
    hud_height = panel_y - 2 

    message_x = bar_width + 3
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 4

    map_width = screen_width - hud_width - 3
    map_height = panel_y - 2
    map_x = hud_width + 2

    room_max_size = min(40, map_height)
    room_min_size = min(20, room_max_size-20)
    max_rooms = 20

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 12

    max_npcs_per_room = 7
    max_monsters_per_room = 4
    max_items_per_room = 2


    darkest_pink = libtcod.Color(202,96,96)
    darker_pink = libtcod.Color(222,116,116)
    dark_pink = libtcod.Color(242,146,146)
    light_pink = libtcod.Color(255,179,179)
    lighter_pink = libtcod.Color(255,220,247)

    dark_bluegreen = libtcod.Color(75,174,160)
    light_bluegreen = libtcod.Color(178,228,213)
    lighter_bluegreen = libtcod.Color(231,243,238)

    orange = libtcod.Color(248,169,120)
    dark_orange = libtcod.Color(228,129,100)

    black = libtcod.Color(0,0,0)

    purple = libtcod.Color(189,131,206)
    colors = {
        'dark_wall_bg': lighter_bluegreen,#libtcod.Color(182,230,189),
        'dark_wall_fg': dark_bluegreen,
        'light_wall_bg': lighter_bluegreen,
        'light_wall_fg': light_bluegreen,
        'dark_ground_bg': dark_pink,
        'dark_ground_fg': darker_pink, #libtcod.Color(177,142,166),
        'light_ground_bg': light_pink,
        'light_ground_fg': lighter_pink,
        'map_border': orange,
        'hp_bg1': darker_pink,
        'hp_bg2': light_pink,
        'hp_fg': black,
        'xp_bg1': dark_bluegreen,
        'xp_bg2': light_bluegreen,
        'xp_fg': black,
        'bad_alert': darkest_pink,
        'moderate_alert': dark_orange,
        'good_alert': purple
    }

    map_chars = {
        'wall_char': 8,
        'ground_char': 176,
        'empty_char': 0
    }

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'hud_width': hud_width,
        'hud_height': hud_height,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'map_x': map_x,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
        'max_nps_per_room': max_npcs_per_room,
        'max_monsters_per_room': max_monsters_per_room,
        'max_items_per_room': max_items_per_room,
        'colors': colors,
        'map_chars': map_chars
    }

    return constants


def get_game_variables(constants):
    fighter_component = Fighter(hp=100, defense=1, power=2)
    social_component = Social(bond=0)
    inventory_component = Inventory(26)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0, 0, '<', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.ACTOR,
                    fighter=fighter_component, inventory=inventory_component, level=level_component,
                    equipment=equipment_component)
    entities = [player]

    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2)
    dagger = Entity(0, 0, '-', libtcod.sky, 'Dagger', equippable=equippable_component)
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    game_map = GameMap(constants['map_x'],constants['map_width'], constants['map_height'])
    #game_map = GameMap(constants['map_x'],constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities)

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    #hud = HUD()

    game_state = GameStates.PLAYERS_TURN

    return player, entities, game_map, message_log, game_state
