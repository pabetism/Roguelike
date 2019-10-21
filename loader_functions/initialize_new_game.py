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

    screen_width = 120
    screen_height = 80

    bar_width = 20
    panel_height = 20
    panel_y = screen_height - panel_height - 1

    hud_width = 15
    hud_height = panel_y - 2 

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = screen_width - hud_width - 3
    map_height = panel_y - 2
    map_x = hud_width + 2

    room_max_size = 40
    room_min_size = 40
    max_rooms = 20

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 12

    max_npcs_per_room = 5
    max_monsters_per_room = 0
    max_items_per_room = 2

    colors = {
        'dark_wall': libtcod.Color(10, 10, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(120, 100, 50),
        'light_ground': libtcod.Color(180, 180, 50),
        'map_border': libtcod.Color(180, 180, 180)
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
        'colors': colors
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
