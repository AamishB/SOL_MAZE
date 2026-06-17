import pygame
import sys
import math
import random
import asyncio
import config
from engine import SolMazeEngine
from ui.hud import draw_hud
from ui.grid import draw_grid, draw_player
from ui.screens import (
    show_help_screen,
    show_pause_menu,
    show_win_screen,
    show_fail_screen,
    screen_transition
)

async def phase_transition(engine_before, engine_after):
    if engine_before.is_day == engine_after.is_day:
        return
    flash = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
    for alpha in range(0, 100, 5):
        flash.fill((255, 240, 150, alpha) if engine_after.is_day else (50, 30, 100, alpha))
        config.screen.blit(flash, (0, 0))
        pygame.display.flip()
        config.clock.tick(60)
        await asyncio.sleep(0)

async def play_game(mode="standard"):
    engine = SolMazeEngine(grid_size=config.GRID_SIZE, num_pillars=8, seed=None, mode=mode)
    moves = 0
    last_phase = engine.is_day
    particles = []
    visual_player_pos = list(engine.player_pos) if engine.player_pos is not None else [0, 0]

    def draw_particles():
        for p in particles[:]:
            p['t'] -= 1
            if p['t'] <= 0:
                particles.remove(p)
                continue
            p['x'] += p['vx']
            p['y'] += p['vy']
            pygame.draw.circle(config.screen, p['color'], (int(p['x']), int(p['y'])), p['size'])

    if not config.has_seen_help:
        config.screen.fill((15, 20, 35))
        draw_hud(engine, moves)
        draw_grid(engine, config.animation_frame)
        draw_player(engine, visual_player_pos)
        pygame.display.flip()
        await show_help_screen(mode)
        config.has_seen_help = True

    touch_start_pos = None

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                touch_start_pos = event.pos
                if (x - (config.WIDTH - 40))**2 + (y - 75)**2 <= 15**2:
                    await show_help_screen(mode)
                    continue
                
                # Handle placement for Environment Day
                if getattr(engine, "mode", "standard") == "calendar_world_environment_day" and getattr(engine, "player_pos", None) is None:
                    if y > config.HUD_HEIGHT:
                        r = (y - config.HUD_HEIGHT) // config.CELL_SIZE
                        c = x // config.CELL_SIZE
                        if 0 <= r < config.GRID_SIZE and 0 <= c < config.GRID_SIZE:
                            if (r, c) not in getattr(engine, "trash_tiles", set()):
                                engine.player_pos = [r, c]
                                engine.grass_tiles.add((r, c))

            if event.type == pygame.MOUSEBUTTONUP and touch_start_pos:
                dx = event.pos[0] - touch_start_pos[0]
                dy = event.pos[1] - touch_start_pos[1]
                touch_start_pos = None
                
                # If drag distance > 30px, treat as swipe
                if abs(dx) > 30 or abs(dy) > 30:
                    key_event = None
                    if abs(dx) > abs(dy):
                        key_event = pygame.K_RIGHT if dx > 0 else pygame.K_LEFT
                    else:
                        key_event = pygame.K_DOWN if dy > 0 else pygame.K_UP
                    
                    if key_event:
                        # Post a simulated keyboard event to use the existing movement logic
                        pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=key_event))

                                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    config.toggle_fullscreen()
                    continue
                if event.key == pygame.K_h:
                    await show_help_screen(mode)
                    continue
                if event.key in (pygame.K_TAB, pygame.K_s):
                    current_angle = engine.sun_angle
                    if engine.is_day:
                        degrees_to_next = 225.0 - current_angle
                        target_angle = 225.0
                    else:
                        degrees_to_next = 360.0 - current_angle
                        target_angle = 0.0
                    
                    added_moves = int(math.ceil(degrees_to_next / engine.angle_step))
                    engine.sun_angle = target_angle
                    engine.update_shadows()
                    engine.collect_stones()
                    moves += added_moves
                    
                    # Spawn particles to indicate skip transition
                    r, c = engine.player_pos
                    x = c * config.CELL_SIZE + config.CELL_SIZE // 2
                    y = config.HUD_HEIGHT + r * config.CELL_SIZE + config.CELL_SIZE // 2
                    for _ in range(15):
                        angle = random.uniform(0, 2 * math.pi)
                        speed = random.uniform(1.5, 4)
                        particles.append({
                            'x': x, 'y': y,
                            'vx': math.cos(angle) * speed,
                            'vy': math.sin(angle) * speed,
                            'color': (255, 200, 50) if engine.is_day else (180, 160, 255),
                            'size': random.randint(2, 4),
                            't': random.randint(10, 20)
                        })
                    
                    if engine.check_win():
                        return
            
                    if getattr(engine, "mode", "standard") == "calendar_world_environment_day":
                        if getattr(engine, "failed_on_trash", False):
                            res = await show_fail_screen("You stepped on toxic trash!")
                            if res == "restart":
                                engine = SolMazeEngine(config.GRID_SIZE, mode)
                                engine.generate_layout(8)
                                moves = 0
                            else:
                                return
                        elif engine.player_pos is not None and not getattr(engine, "tree_spawned", False):
                            if engine.is_trapped():
                                res = await show_fail_screen("You are trapped in grass!")
                                if res == "restart":
                                    engine = SolMazeEngine(config.GRID_SIZE, mode)
                                    engine.generate_layout(8)
                                    moves = 0
                                else:
                                    return
                    elif getattr(engine, "mode", "standard") == "calendar_world_oceans_day":
                        if getattr(engine, "failed_in_tide", False):
                            res = await show_fail_screen("Your boat was destroyed by the shifting tide!")
                            if res == "restart":
                                engine = SolMazeEngine(config.GRID_SIZE, mode)
                                engine.generate_layout(8)
                                moves = 0
                            else:
                                return
                        elif getattr(engine, "failed_in_current", False):
                            res = await show_fail_screen("A strong current smashed your boat!")
                            if res == "restart":
                                engine = SolMazeEngine(config.GRID_SIZE, mode)
                                engine.generate_layout(8)
                                moves = 0
                            else:
                                return
                    
                    if engine.is_day != last_phase:
                        await phase_transition(engine, engine)
                        last_phase = engine.is_day
                    continue
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    res = await show_pause_menu()
                    if res == "restart":
                        await play_game(mode)
                        return
                    elif res == "menu":
                        await screen_transition()
                        return
                    continue
                
                dr = dc = 0
                if event.key == pygame.K_UP:
                    dr = -1
                elif event.key == pygame.K_DOWN:
                    dr = 1
                elif event.key == pygame.K_LEFT:
                    dc = -1
                elif event.key == pygame.K_RIGHT:
                    dc = 1
                elif event.key == pygame.K_SPACE:
                    dr = dc = 0
                else:
                    continue

                prev_sun = len(engine.sun_stones)
                prev_moon = len(engine.moon_stones)
                prev_fathers_items = len(getattr(engine, "fathers_day_items", {})) if mode == "calendar_fathers_day" else 0
                prev_coffee = len(getattr(engine, "coffee_cups", set())) if mode == "calendar_fathers_day" else 0

                engine.move_player(dr, dc)
                
                if getattr(engine, "mode", "standard") == "calendar_world_environment_day":
                    if getattr(engine, "failed_on_trash", False):
                        res = await show_fail_screen("You stepped on toxic trash!")
                        if res == "restart":
                            engine = SolMazeEngine(config.GRID_SIZE, mode)
                            engine.generate_layout(8)
                            moves = 0
                        else:
                            return
                    elif engine.player_pos is not None and not getattr(engine, "tree_spawned", False):
                        if engine.is_trapped():
                            res = await show_fail_screen("You are trapped in grass!")
                            if res == "restart":
                                engine = SolMazeEngine(config.GRID_SIZE, mode)
                                engine.generate_layout(8)
                                moves = 0
                            else:
                                return
                
                if engine.mode == "solstice_shift" and not engine.is_day and engine.vision_buff_active:
                    moves += 2
                else:
                    moves += 1

                # Check fails
                if getattr(engine, "failed_in_pit", False):
                    result = await show_fail_screen("FELL IN THE PIT!")
                    if result == "menu": return
                    elif result == "replay": await play_game(mode); return
                    
                if getattr(engine, "failed_in_tide", False):
                    result = await show_fail_screen("Your boat was destroyed by the shifting tide!")
                    if result == "menu": return
                    elif result == "replay": await play_game(mode); return
                    
                if getattr(engine, "failed_in_current", False):
                    result = await show_fail_screen("A strong current smashed your boat!")
                    if result == "menu": return
                    elif result == "replay": await play_game(mode); return
                    
                if getattr(engine, "failed_asleep", False):
                    result = await show_fail_screen("Dad fell asleep on the lawn!")
                    if result == "menu": return
                    elif result == "replay": await play_game(mode); return
                
                if engine.mode == "solstice_shift" and moves > 200:
                    result = await show_fail_screen("OUT OF MOVES!")
                    if result == "menu": return
                    elif result == "replay": await play_game(mode); return
                    
                if getattr(engine, "mode", "standard") == "calendar_world_environment_day":
                    if getattr(engine, "failed_on_trash", False):
                        res = await show_fail_screen("You stepped on toxic trash!")
                        if res == "restart":
                            engine = SolMazeEngine(config.GRID_SIZE, mode)
                            engine.generate_layout(8)
                            moves = 0
                        else:
                            return
                    elif engine.player_pos is not None and not getattr(engine, "tree_spawned", False):
                        if engine.is_trapped():
                            res = await show_fail_screen("You are trapped in grass!")
                            if res == "restart":
                                engine = SolMazeEngine(config.GRID_SIZE, mode)
                                engine.generate_layout(8)
                                moves = 0
                            else:
                                return

                collected_fathers_item = (mode == "calendar_fathers_day" and len(engine.fathers_day_items) < prev_fathers_items)
                collected_coffee = (mode == "calendar_fathers_day" and len(engine.coffee_cups) < prev_coffee)
                
                if mode == "calendar_world_music_day":
                    if getattr(engine, "correct_note_collected", False):
                        pulse = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
                        pulse.fill((50, 255, 50, 60))
                        config.screen.blit(pulse, (0, 0))
                        pygame.display.flip()
                        pygame.time.wait(20)
                        
                        r, c = engine.player_pos
                        x_p = c * config.CELL_SIZE + config.CELL_SIZE // 2
                        y_p = config.HUD_HEIGHT + r * config.CELL_SIZE + config.CELL_SIZE // 2
                        for _ in range(25):
                            angle = random.uniform(0, 2 * math.pi)
                            speed = random.uniform(3, 8)
                            particles.append({
                                'x': x_p, 'y': y_p,
                                'vx': math.cos(angle) * speed,
                                'vy': math.sin(angle) * speed,
                                'color': (50, 255, 50),
                                'size': random.randint(2, 5),
                                't': random.randint(15, 30)
                            })
                    elif getattr(engine, "sequence_failed", False):
                        shake_surf = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
                        shake_color = (255, 50, 50, 80) if getattr(engine, "failed_dazed", False) else (255, 150, 0, 80)
                        shake_surf.fill(shake_color)
                        config.screen.blit(shake_surf, (0, 0))
                        pygame.display.flip()
                        pygame.time.wait(30)
                        
                        r, c = engine.player_pos
                        x_p = c * config.CELL_SIZE + config.CELL_SIZE // 2
                        y_p = config.HUD_HEIGHT + r * config.CELL_SIZE + config.CELL_SIZE // 2
                        for _ in range(30):
                            angle = random.uniform(0, 2 * math.pi)
                            speed = random.uniform(4, 9)
                            particles.append({
                                'x': x_p, 'y': y_p,
                                'vx': math.cos(angle) * speed,
                                'vy': math.sin(angle) * speed,
                                'color': (255, 50, 50) if getattr(engine, "failed_dazed", False) else (255, 150, 0),
                                'size': random.randint(3, 6),
                                't': random.randint(20, 35)
                            })

                if len(engine.sun_stones) < prev_sun or len(engine.moon_stones) < prev_moon or collected_fathers_item or collected_coffee:
                    pulse = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
                    pulse.fill((255, 255, 255, 100))
                    config.screen.blit(pulse, (0, 0))
                    pygame.display.flip()
                    pygame.time.wait(30)
                    
                    r, c = engine.player_pos
                    x = c * config.CELL_SIZE + config.CELL_SIZE // 2
                    y = config.HUD_HEIGHT + r * config.CELL_SIZE + config.CELL_SIZE // 2
                    if collected_fathers_item:
                        color = (135, 206, 250)
                    elif collected_coffee:
                        color = (240, 240, 245)
                    else:
                        color = (255, 215, 0) if len(engine.sun_stones) < prev_sun else (200, 160, 255)
                    for _ in range(20):
                        angle = random.uniform(0, 2 * math.pi)
                        speed = random.uniform(2, 6)
                        particles.append({
                            'x': x, 'y': y,
                            'vx': math.cos(angle) * speed,
                            'vy': math.sin(angle) * speed,
                            'color': color,
                            'size': random.randint(2, 5),
                            't': random.randint(15, 30)
                        })

                if engine.check_win():
                    result = await show_win_screen(moves, mode)
                    if result == "menu":
                        return
                    elif result == "replay":
                        await play_game(mode)
                        return
                if engine.is_day != last_phase:
                    await phase_transition(engine, engine)
                    last_phase = engine.is_day

                if getattr(engine, "just_teleported", False):
                    flash = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
                    flash.fill((255, 255, 255, 100))
                    config.screen.blit(flash, (0, 0))
                    pygame.display.flip()
                    pygame.time.wait(40)
                    
                    locations = list(engine.sun_stones) + list(engine.moon_stones) + [tuple(engine.goal_pos_day), tuple(engine.goal_pos_night)]
                    for r, c in locations:
                        px = c * config.CELL_SIZE + config.CELL_SIZE // 2
                        py = config.HUD_HEIGHT + r * config.CELL_SIZE + config.CELL_SIZE // 2
                        for _ in range(10):
                            angle = random.uniform(0, 2 * math.pi)
                            speed = random.uniform(2, 6)
                            particles.append({
                                'x': px, 'y': py,
                                'vx': math.cos(angle) * speed,
                                'vy': math.sin(angle) * speed,
                                'color': (255, 255, 255),
                                'size': random.randint(2, 5),
                                't': random.randint(15, 30)
                            })
                    engine.just_teleported = False

        if engine.player_pos is not None:
            visual_player_pos[0] += (engine.player_pos[0] - visual_player_pos[0]) * 0.3
            visual_player_pos[1] += (engine.player_pos[1] - visual_player_pos[1]) * 0.3

        config.screen.fill((15, 20, 35))
        draw_hud(engine, moves)
        draw_grid(engine, config.animation_frame)
        draw_player(engine, visual_player_pos)
        draw_particles()
        
        if moves == 0:
            if mode == "calendar_pride_maze":
                tooltip_txt = config.fonts['hud_text'].render("Tip: Collect Prisms in Rainbow order to shatter Gates!", True, (255, 255, 255))
            elif mode == "calendar_world_environment_day":
                if engine.player_pos is None:
                    tooltip_txt = config.fonts['hud_text'].render("Tip: Click an empty space to start planting grass!", True, (255, 255, 255))
                else:
                    tooltip_txt = config.fonts['hud_text'].render("Tip: Encircle trash to clean it up!", True, (255, 255, 255))
            elif mode == "calendar_world_oceans_day":
                tooltip_txt = config.fonts['hud_text'].render("Tip: Rescue turtles! Use TAB/S to advance the tide if you get stuck.", True, (255, 255, 255))
            elif mode == "calendar_juneteenth":
                tooltip_txt = config.fonts['hud_text'].render("Tip: Find and ring the 3 Freedom Bells to free the Stars!", True, (255, 255, 255))
            elif mode == "calendar_fathers_day":
                tooltip_txt = config.fonts['hud_text'].render("Tip: Collect the Grill, Tie, and Mug! Keep Energy up by a Coffee sip!", True, (255, 255, 255))
            elif mode == "calendar_world_music_day":
                tooltip_txt = config.fonts['hud_text'].render("Tip: Step on notes in HUD sequence order! Beware Speaker blasts!", True, (255, 255, 255))
            else:
                tooltip_txt = config.fonts['hud_text'].render("Tip: Collect stones! Day paths are light, Night paths are dark.", True, (255, 255, 255))
            pygame.draw.rect(config.screen, (30, 30, 50, 200), (config.WIDTH//2 - tooltip_txt.get_width()//2 - 10, config.HEIGHT - 50, tooltip_txt.get_width() + 20, 30), border_radius=5)
            config.screen.blit(tooltip_txt, (config.WIDTH//2 - tooltip_txt.get_width()//2, config.HEIGHT - 45))
            
        pygame.display.flip()
        config.clock.tick(config.FPS)
        await asyncio.sleep(0)