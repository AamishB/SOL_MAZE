import pygame
import math
import config
from graphics import (
    draw_gradient,
    draw_god_rays,
    draw_starfield,
    draw_character,
    draw_sun_stone,
    draw_moon_stone,
    draw_prism,
    draw_rainbow_bridge,
    draw_gate,
    draw_trash,
    draw_tree_of_life,
    draw_boat,
    draw_coral_reef,
    draw_trench,
    draw_turtle,
    draw_whirlpool,
    draw_pillar,
    draw_freedom_bell,
    draw_freedom_star,
    draw_shadow_wall,
    draw_grill,
    draw_tie_item,
    draw_mug,
    draw_coffee_cup,
    draw_lawn_chair,
    draw_lawn_gnome,
    draw_lawn_bush,
    draw_garden_hose,
    draw_musical_note,
    draw_speaker_obstacle,
    draw_drum_obstacle,
    draw_mic_obstacle,
    draw_treble_clef
)

def draw_grid(engine, animation_offset=0):
    bg_surf = pygame.Surface((config.GRID_SIZE * config.CELL_SIZE, config.GRID_SIZE * config.CELL_SIZE))
    if getattr(engine, "mode", "standard") == "calendar_pride_maze":
        if engine.is_day:
            draw_gradient(bg_surf, (255, 200, 200), (200, 200, 255), vertical=True)
            if config.settings_god_rays:
                draw_god_rays(bg_surf, engine.sun_angle, intensity=10)
        else:
            draw_gradient(bg_surf, (40, 20, 40), (20, 20, 60), vertical=True)
            draw_starfield(bg_surf, 100)
    elif getattr(engine, "mode", "standard") == "calendar_world_environment_day":
        draw_gradient(bg_surf, (150, 100, 60), (120, 80, 50), vertical=True)
    elif getattr(engine, "mode", "standard") == "calendar_world_oceans_day":
        if getattr(engine, "is_high_tide", True):
            draw_gradient(bg_surf, (0, 75, 120), (0, 50, 90), vertical=True)
        else:
            draw_gradient(bg_surf, (0, 150, 180), (0, 100, 150), vertical=True)
    elif getattr(engine, "mode", "standard") == "calendar_juneteenth":
        if len(getattr(engine, "freedom_bells", {})) == 0:
            draw_gradient(bg_surf, (200, 30, 30), (0, 150, 50), vertical=True)
        else:
            draw_gradient(bg_surf, (50, 10, 10), (10, 30, 10), vertical=True)
    elif getattr(engine, "mode", "standard") == "calendar_fathers_day":
        draw_gradient(bg_surf, (20, 60, 25), (46, 139, 87), vertical=True)
    elif getattr(engine, "mode", "standard") == "calendar_world_music_day":
        draw_gradient(bg_surf, (25, 10, 45), (15, 5, 30), vertical=True)
        for i in range(5):
            y_line = int(bg_surf.get_height() * 0.35 + i * 14)
            pygame.draw.line(bg_surf, (80, 80, 100), (0, y_line), (bg_surf.get_width(), y_line), 1)
        for i in range(5):
            y_line = int(bg_surf.get_height() * 0.65 + i * 14)
            pygame.draw.line(bg_surf, (80, 80, 100), (0, y_line), (bg_surf.get_width(), y_line), 1)
    else:
        if engine.is_day:
            draw_gradient(bg_surf, (210, 230, 250), (180, 210, 240), vertical=True)
            if config.settings_god_rays:
                draw_god_rays(bg_surf, engine.sun_angle, intensity=20)
        else:
            draw_gradient(bg_surf, (20, 20, 60), (10, 10, 40), vertical=True)
            draw_starfield(bg_surf, 100)
    config.screen.blit(bg_surf, (0, config.HUD_HEIGHT))

    shadow_surf = pygame.Surface((config.CELL_SIZE, config.CELL_SIZE), pygame.SRCALPHA)
    shadow_surf.fill((15, 15, 35, 200))
    light_surf = pygame.Surface((config.CELL_SIZE, config.CELL_SIZE), pygame.SRCALPHA)
    light_surf.fill((255, 240, 150, 80))

    for r in range(config.GRID_SIZE):
        for c in range(config.GRID_SIZE):
            x = c * config.CELL_SIZE
            y = config.HUD_HEIGHT + r * config.CELL_SIZE
            if getattr(engine, "mode", "standard") == "solstice_shift":
                is_pit = (r, c) in engine.pits
                if engine.is_day:
                    if is_pit:
                        pygame.draw.rect(config.screen, (5, 5, 10), (x + 1, y + 1, config.CELL_SIZE - 2, config.CELL_SIZE - 2))
                        pygame.draw.rect(config.screen, (0, 0, 0), (x + 5, y + 5, config.CELL_SIZE - 10, config.CELL_SIZE - 10))
                    else:
                        pygame.draw.rect(config.screen, (245, 235, 180), (x + 1, y + 1, config.CELL_SIZE - 2, config.CELL_SIZE - 2))
                else:
                    if is_pit:
                        pygame.draw.rect(config.screen, (190, 200, 230), (x + 1, y + 1, config.CELL_SIZE - 2, config.CELL_SIZE - 2))
                        pygame.draw.rect(config.screen, (220, 230, 255), (x + 5, y + 5, config.CELL_SIZE - 10, config.CELL_SIZE - 10))
                    else:
                        pygame.draw.rect(config.screen, (20, 20, 30), (x + 1, y + 1, config.CELL_SIZE - 2, config.CELL_SIZE - 2))
            else:
                is_pass = engine.is_passable(r, c)
                in_shadow = engine.shadow_map[r, c]
                if (r, c) not in engine.pillars and (r, c) not in getattr(engine, "trash_tiles", set()):
                    if is_pass:
                        if getattr(engine, "mode", "standard") == "calendar_pride_maze":
                            tile_color = (255, 240, 255) if engine.is_day else (100, 70, 120)
                        elif getattr(engine, "mode", "standard") == "calendar_world_environment_day":
                            if (r, c) in engine.grass_tiles:
                                tile_color = (50, 200, 50)
                            else:
                                tile_color = (160, 110, 70)
                        elif getattr(engine, "mode", "standard") == "calendar_world_oceans_day":
                            is_high = getattr(engine, "is_high_tide", True)
                            tile_color = (0, 120, 180) if is_high else (0, 180, 220)
                        elif getattr(engine, "mode", "standard") == "calendar_fathers_day":
                            tile_color = (34, 139, 34)
                        elif getattr(engine, "mode", "standard") == "calendar_world_music_day":
                            tile_color = (35, 18, 55)
                        else:
                            tile_color = (245, 235, 180) if engine.is_day else (70, 80, 120)
                        pygame.draw.rect(config.screen, tile_color, (x + 1, y + 1, config.CELL_SIZE - 2, config.CELL_SIZE - 2))
                        
                        if getattr(engine, "mode", "standard") == "calendar_world_environment_day" and (r, c) in engine.grass_tiles:
                            pygame.draw.rect(config.screen, (34, 139, 34), (x + 1, y + 1, config.CELL_SIZE - 2, config.CELL_SIZE - 2), 2)
                    else:
                        if getattr(engine, "mode", "standard") == "calendar_world_environment_day" and (r, c) in engine.grass_tiles:
                            pygame.draw.rect(config.screen, (50, 200, 50), (x + 1, y + 1, config.CELL_SIZE - 2, config.CELL_SIZE - 2))
                            pygame.draw.rect(config.screen, (34, 139, 34), (x + 1, y + 1, config.CELL_SIZE - 2, config.CELL_SIZE - 2), 2)
                        else:
                            pygame.draw.rect(config.screen, (30, 30, 40), (x + 1, y + 1, config.CELL_SIZE - 2, config.CELL_SIZE - 2))
                    
                    if in_shadow and getattr(engine, "mode", "standard") not in ["calendar_pride_maze", "calendar_world_environment_day", "calendar_world_oceans_day", "calendar_juneteenth", "calendar_fathers_day", "calendar_world_music_day"]:
                        config.screen.blit(shadow_surf, (x, y))
                    elif not engine.is_day and getattr(engine, "mode", "standard") not in ["calendar_pride_maze", "calendar_world_environment_day", "calendar_world_oceans_day", "calendar_juneteenth", "calendar_fathers_day", "calendar_world_music_day"]:
                        config.screen.blit(light_surf, (x, y))
                elif (r, c) in engine.pillars:
                    if getattr(engine, "mode", "standard") == "calendar_fathers_day":
                        obstacle_type = getattr(engine, "backyard_obstacles", {}).get((r, c), "bush")
                        if obstacle_type == "gnome":
                            pillar_img = draw_lawn_gnome(config.CELL_SIZE)
                        elif obstacle_type == "hose":
                            pillar_img = draw_garden_hose(config.CELL_SIZE)
                        else:
                            pillar_img = draw_lawn_bush(config.CELL_SIZE)
                    elif getattr(engine, "mode", "standard") == "calendar_world_music_day":
                        obstacle_type = getattr(engine, "music_obstacles", {}).get((r, c), "drum")
                        if obstacle_type == "mic":
                            pillar_img = draw_mic_obstacle(config.CELL_SIZE)
                        elif (r, c) in getattr(engine, "speakers", set()):
                            is_pulsing = getattr(engine, "beat_counter", 0) >= 2
                            pillar_img = draw_speaker_obstacle(config.CELL_SIZE, is_pulsing)
                        else:
                            pillar_img = draw_drum_obstacle(config.CELL_SIZE)
                    else:
                        pillar_img = draw_pillar(config.CELL_SIZE)
                    config.screen.blit(pillar_img, (x, y))

            if getattr(engine, "mode", "standard") == "calendar_pride_maze":
                if (r, c) in getattr(engine, "gates", {}) and engine.gates[(r, c)] not in getattr(engine, "collected_prisms", []):
                    color_name = engine.gates[(r, c)]
                    gate_img = draw_gate(config.CELL_SIZE, color_name)
                    config.screen.blit(gate_img, (x, y))
                    
                if (r, c) in getattr(engine, "prisms", {}):
                    color_name = engine.prisms[(r, c)]
                    prism_img = draw_prism(config.CELL_SIZE - 10, color_name)
                    offset_y = math.sin(animation_offset + r + c) * 3
                    config.screen.blit(prism_img, (x + 5, y + 5 + offset_y))
            elif getattr(engine, "mode", "standard") == "calendar_world_environment_day":
                if (r, c) in getattr(engine, "trash_tiles", set()):
                    trash_img = draw_trash(config.CELL_SIZE - 10)
                    config.screen.blit(trash_img, (x + 5, y + 5))
            elif getattr(engine, "mode", "standard") == "calendar_world_oceans_day":
                is_high = getattr(engine, "is_high_tide", True)
                if (r, c) in getattr(engine, "coral_reefs", set()):
                    coral_img = draw_coral_reef(config.CELL_SIZE, is_high)
                    config.screen.blit(coral_img, (x, y))
                if (r, c) in getattr(engine, "deep_trenches", set()):
                    trench_img = draw_trench(config.CELL_SIZE, is_high)
                    config.screen.blit(trench_img, (x, y))
                    
                if (r, c) in getattr(engine, "turtles", set()):
                    turtle_img = draw_turtle(config.CELL_SIZE - 10)
                    config.screen.blit(turtle_img, (x + 5, y + 5))
            elif getattr(engine, "mode", "standard") == "calendar_juneteenth":
                if (r, c) in getattr(engine, "shadow_walls", set()):
                    wall_img = draw_shadow_wall(config.CELL_SIZE)
                    config.screen.blit(wall_img, (x, y))
                if (r, c) in getattr(engine, "freedom_bells", {}):
                    bell_img = draw_freedom_bell(config.CELL_SIZE - 10)
                    offset_y = math.sin(animation_offset + r + c) * 3
                    config.screen.blit(bell_img, (x + 5, y + 5 + offset_y))
                if (r, c) in getattr(engine, "freedom_stars", set()):
                    star_img = draw_freedom_star(config.CELL_SIZE - 10)
                    offset_y = math.sin(animation_offset + r + c) * 3
                    config.screen.blit(star_img, (x + 5, y + 5 + offset_y))
            elif getattr(engine, "mode", "standard") == "calendar_fathers_day":
                if (r, c) in getattr(engine, "fathers_day_items", {}):
                    item_type = engine.fathers_day_items[(r, c)]
                    offset_y = math.sin(animation_offset + r + c) * 3
                    if item_type == "grill":
                        item_img = draw_grill(config.CELL_SIZE - 10)
                    elif item_type == "tie":
                        item_img = draw_tie_item(config.CELL_SIZE - 10)
                    else:
                        item_img = draw_mug(config.CELL_SIZE - 10)
                    config.screen.blit(item_img, (x + 5, y + 5 + offset_y))
                if (r, c) in getattr(engine, "coffee_cups", set()):
                    cup_img = draw_coffee_cup(config.CELL_SIZE - 10)
                    offset_y = math.sin(animation_offset + r + c) * 3
                    config.screen.blit(cup_img, (x + 5, y + 5 + offset_y))
            elif getattr(engine, "mode", "standard") == "calendar_world_music_day":
                if (r, c) in getattr(engine, "musical_notes", {}):
                    color_name = engine.musical_notes[(r, c)]
                    color_map = {"red": (255, 50, 50), "blue": (50, 150, 255), "green": (50, 255, 50), "yellow": (255, 230, 0)}
                    c_val = color_map.get(color_name, (255, 255, 255))
                    note_img = draw_musical_note(config.CELL_SIZE - 10, c_val)
                    offset_y = math.sin(animation_offset + r + c) * 3
                    config.screen.blit(note_img, (x + 5, y + 5 + offset_y))
            else:
                if (r, c) in engine.sun_stones:
                    stone_img = draw_sun_stone(config.CELL_SIZE - 10)
                    offset_y = math.sin(animation_offset + r + c) * 3
                    config.screen.blit(stone_img, (x + 5, y + 5 + offset_y))
                elif (r, c) in engine.moon_stones:
                    stone_img = draw_moon_stone(config.CELL_SIZE - 10)
                    offset_y = math.sin(animation_offset + r + c) * 3
                    config.screen.blit(stone_img, (x + 5, y + 5 + offset_y))

            if getattr(engine, "mode", "standard") == "solstice_shift":
                if [r, c] == engine.goal_pos_day:
                    color = (255, 215, 0) if engine.reached_day_goal else (100, 100, 30)
                    pygame.draw.rect(config.screen, color, (x + 10, y + 10, config.CELL_SIZE - 20, config.CELL_SIZE - 20), 3)
                if [r, c] == engine.goal_pos_night:
                    color = (180, 160, 255) if engine.reached_night_goal else (60, 50, 100)
                    pygame.draw.rect(config.screen, color, (x + 10, y + 10, config.CELL_SIZE - 20, config.CELL_SIZE - 20), 3)
            elif getattr(engine, "mode", "standard") == "calendar_pride_maze":
                if getattr(engine, "rainbow_bridge_spawned", False) and [r, c] == engine.goal_pos:
                    bridge_img = draw_rainbow_bridge(config.CELL_SIZE)
                    config.screen.blit(bridge_img, (x, y))
            elif getattr(engine, "mode", "standard") == "calendar_world_environment_day":
                if getattr(engine, "tree_spawned", False) and [r, c] == engine.goal_pos:
                    tree_img = draw_tree_of_life(config.CELL_SIZE)
                    config.screen.blit(tree_img, (x, y))
            elif getattr(engine, "mode", "standard") == "calendar_world_oceans_day":
                if getattr(engine, "whirlpool_spawned", False) and [r, c] == engine.goal_pos:
                    whirlpool_img = draw_whirlpool(config.CELL_SIZE)
                    config.screen.blit(whirlpool_img, (x, y))
            elif getattr(engine, "mode", "standard") == "calendar_fathers_day":
                if [r, c] == engine.goal_pos and engine.goal_pos != [-1, -1]:
                    chair_img = draw_lawn_chair(config.CELL_SIZE)
                    config.screen.blit(chair_img, (x, y))
            elif getattr(engine, "mode", "standard") == "calendar_world_music_day":
                if [r, c] == engine.goal_pos and engine.goal_pos != [-1, -1]:
                    clef_img = draw_treble_clef(config.CELL_SIZE)
                    config.screen.blit(clef_img, (x, y))
            else:
                if [r, c] == engine.goal_pos:
                    unlocked = (len(engine.sun_stones) == 0 and len(engine.moon_stones) == 0)
                    if unlocked:
                        pygame.draw.rect(config.screen, (100, 255, 100, 100), (x + 10, y + 10, config.CELL_SIZE - 20, config.CELL_SIZE - 20))
                        pygame.draw.rect(config.screen, (50, 200, 50), (x + 10, y + 10, config.CELL_SIZE - 20, config.CELL_SIZE - 20), 2)
                    else:
                        pygame.draw.rect(config.screen, (80, 80, 100), (x + 10, y + 10, config.CELL_SIZE - 20, config.CELL_SIZE - 20), 2)

    # Draw World Music Day soundwave blasts
    if getattr(engine, "mode", "standard") == "calendar_world_music_day":
        for (sr, sc) in getattr(engine, "soundwave_tiles", set()):
            sx = sc * config.CELL_SIZE
            sy = config.HUD_HEIGHT + sr * config.CELL_SIZE
            wave_surf = pygame.Surface((config.CELL_SIZE, config.CELL_SIZE), pygame.SRCALPHA)
            pulse_offset = (pygame.time.get_ticks() // 150) % 3
            for r_circle in range(8 + pulse_offset * 6, config.CELL_SIZE // 2, 8):
                alpha = max(0, 140 - r_circle * 3)
                pygame.draw.circle(wave_surf, (0, 255, 255, alpha), (config.CELL_SIZE//2, config.CELL_SIZE//2), r_circle, 2)
            config.screen.blit(wave_surf, (sx, sy))

    for i in range(config.GRID_SIZE + 1):
        pygame.draw.line(config.screen, (100, 100, 130, 100), (i * config.CELL_SIZE, config.HUD_HEIGHT),
                         (i * config.CELL_SIZE, config.HUD_HEIGHT + config.GRID_SIZE * config.CELL_SIZE), 1)
        pygame.draw.line(config.screen, (100, 100, 130, 100), (0, config.HUD_HEIGHT + i * config.CELL_SIZE),
                         (config.WIDTH, config.HUD_HEIGHT + i * config.CELL_SIZE), 1)

    if getattr(engine, "mode", "standard") == "solstice_shift" and not engine.is_day:
        vision_radius = 2 if engine.vision_buff_active else 1
        vision_surf = pygame.Surface((config.WIDTH, config.GRID_SIZE * config.CELL_SIZE), pygame.SRCALPHA)
        vision_surf.fill((0, 0, 0, 250))
        pr, pc = engine.player_pos
        px = pc * config.CELL_SIZE + config.CELL_SIZE // 2
        py = pr * config.CELL_SIZE + config.CELL_SIZE // 2
        pygame.draw.circle(vision_surf, (0, 0, 0, 0), (px, py), int(vision_radius * config.CELL_SIZE + config.CELL_SIZE*0.5))
        pygame.draw.circle(vision_surf, (0, 0, 0, 100), (px, py), int(vision_radius * config.CELL_SIZE + config.CELL_SIZE*0.5), width=int(config.CELL_SIZE*0.5))
        config.screen.blit(vision_surf, (0, config.HUD_HEIGHT))

def draw_player(engine, visual_pos=None):
    if visual_pos is None:
        visual_pos = getattr(engine, "player_pos", None)
    if visual_pos is None:
        return
    r, c = visual_pos
    x = c * config.CELL_SIZE + config.CELL_SIZE // 2
    y = config.HUD_HEIGHT + r * config.CELL_SIZE + config.CELL_SIZE // 2 - 5
    config.animation_frame = (config.animation_frame + 0.1) % (2 * math.pi)
    if getattr(engine, "mode", "standard") == "calendar_world_oceans_day":
        player_img = draw_boat(config.CELL_SIZE)
    elif getattr(engine, "mode", "standard") == "calendar_juneteenth":
        player_img = draw_character(config.CELL_SIZE - 10, "juneteenth", config.animation_frame)
    elif getattr(engine, "mode", "standard") == "calendar_fathers_day":
        player_img = draw_character(config.CELL_SIZE - 10, "fathers_day", config.animation_frame)
    elif getattr(engine, "mode", "standard") == "calendar_world_music_day":
        player_img = draw_character(config.CELL_SIZE - 10, "rockstar", config.animation_frame)
    else:
        player_img = draw_character(config.CELL_SIZE - 10, config.current_skin, config.animation_frame)
    config.screen.blit(player_img, (x - (config.CELL_SIZE - 10) // 2, y - (config.CELL_SIZE - 10) // 2))
