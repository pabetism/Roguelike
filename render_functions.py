import libtcodpy as libtcod

from enum import Enum

from game_states import GameStates

from menus import character_screen, inventory_menu, level_up_menu

#from Components import level


class RenderOrder(Enum):
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4


def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color, font_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SET)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SET)

    libtcod.console_set_default_foreground(panel, font_color)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_SET, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(con, hud, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, map_x, bar_width, panel_height, panel_y, mouse, colors, map_chars, game_state):

    if fov_recompute:
    # Draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                if visible:
                    if wall:
                        libtcod.console_set_default_foreground(con, colors.get('light_wall_fg'))   
                        libtcod.console_set_default_background(con, colors.get('light_wall_bg'))
                        libtcod.console_put_char(con, x, y, map_chars.get('wall_char'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_default_foreground(con, colors.get('light_ground_fg'))   
                        libtcod.console_set_default_background(con, colors.get('light_ground_bg'))
                        libtcod.console_put_char(con, x, y, map_chars.get('ground_char'), libtcod.BKGND_SET)
                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_default_foreground(con, colors.get('dark_wall_fg'))
                        libtcod.console_set_default_background(con, colors.get('dark_wall_bg'))
                        libtcod.console_put_char(con, x, y, map_chars.get('wall_char'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_default_foreground(con, colors.get('dark_ground_fg'))   
                        libtcod.console_set_default_background(con, colors.get('dark_ground_bg'))
                        libtcod.console_put_char(con, x, y, map_chars.get('ground_char'), libtcod.BKGND_SET)
    #libtcod.console_set_default_foreground(con, libtcod.black)   
    #libtcod.console_set_default_background(con, libtcod.black)

    #gosh, i probably don't need to redraw the borders every time!
    draw_borders(con, game_map.height, game_map.width, colors.get('map_border'))

    #the code below is the begining of a bit of code to add information at the bottom edge of the con
    #libtcod.console_set_default_foreground(con, colors.get('map_border'))
    #libtcod.console_set_default_background(con, libtcod.black)

    #libtcod.console_put_char(con, 2, game_map.height - 1, 181, libtcod.BKGND_SET)
    #libtcod.console_print_ex(con, 3, game_map.height - 1, libtcod.BKGND_SET, libtcod.LEFT, '          ')
    #libtcod.console_put_char(con, 13, game_map.height - 1, 198, libtcod.BKGND_SET)
    #libtcod.console_print_ex(con, 3, game_map.height - 1, libtcod.BKGND_SET, libtcod.LEFT, get_names_under_mouse(mouse, entities, fov_map))
        

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map, colors)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, map_x, 1)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # Print the game messages, one line at a time
    y = 2
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_SET, libtcod.LEFT, message.text)
        y += 1

    draw_borders(panel, panel.height, panel.width, colors.get('map_border'))

    # render HP bar
    render_bar(panel, 2, 2, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               colors.get('hp_bg1'), colors.get('hp_bg2'), colors.get('hp_fg'))
    # render XP bar
    render_bar(panel, 2, 4, bar_width, 'XP', player.level.current_xp, player.level.experience_to_next_level,
               colors.get('xp_bg1'), colors.get('xp_bg2'), colors.get('xp_fg'))

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_set_default_foreground(panel, libtcod.white)

    libtcod.console_print_ex(panel, 2, 6, libtcod.BKGND_SET, libtcod.LEFT, 'Dungeon level: {0}'.format(game_map.dungeon_level))

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 1, panel_y)

    #blit the hud

    draw_borders(hud, hud.height, hud.width, colors.get('map_border'))
    
    libtcod.console_blit(hud, 0, 0, hud.width, hud.height, 1, 1, 1)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'Level up! Choose a stat to raise:', player, 40, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 10, screen_width, screen_height)


def clear_all(con, entities, map_chars, game_map, colors):
    for entity in entities:
        clear_entity(con, entity, map_chars, game_map, colors)


def draw_entity(con, entity, fov_map, game_map, colors):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_set_default_background(con, colors.get('light_ground_bg'))
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_SET)


def clear_entity(con, entity, map_chars, game_map, colors):
    # erase the character that represents this object
    if game_map.tiles[entity.x][entity.y].explored:
        libtcod.console_set_default_background(con, colors.get('dark_ground_bg'))
        libtcod.console_set_default_foreground(con, colors.get('dark_ground_fg'))
        libtcod.console_put_char(con, entity.x, entity.y, map_chars.get('ground_char'), libtcod.BKGND_SET)
    else:
        libtcod.console_set_default_background(con, libtcod.black)
        libtcod.console_put_char(con, entity.x, entity.y, map_chars.get('empty_char'), libtcod.BKGND_SET)

def draw_borders(con, h, w, color):
    libtcod.console_set_default_background(con, libtcod.black)
    libtcod.console_set_default_foreground(con, color)   
    for x in range(1, w - 1):
        libtcod.console_put_char(con, x, 0, 205, libtcod.BKGND_SET)
        libtcod.console_put_char(con, x, h - 1, 205, libtcod.BKGND_SET)
    for y in range(1, h - 1):
        libtcod.console_put_char(con, 0, y, 186, libtcod.BKGND_SET)
        libtcod.console_put_char(con, w - 1, y, 186, libtcod.BKGND_SET)
    libtcod.console_put_char(con, 0, 0, 201, libtcod.BKGND_SET)
    libtcod.console_put_char(con, w - 1, 0, 187, libtcod.BKGND_SET)
    libtcod.console_put_char(con, 0, h - 1, 200, libtcod.BKGND_SET)
    libtcod.console_put_char(con, w - 1, h - 1, 188, libtcod.BKGND_SET)
