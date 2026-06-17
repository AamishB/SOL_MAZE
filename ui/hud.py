import pygame
import math
import config
from graphics import (
    draw_gradient,
    draw_rainbow_icon,
    draw_wave_icon,
    draw_bell_icon,
    draw_tie_icon,
    draw_music_note_icon,
    draw_sun_icon,
    draw_moon_icon,
    draw_grill,
    draw_tie_item,
    draw_mug,
    draw_musical_note,
    draw_sun_stone,
    draw_moon_stone
)

def draw_hud(engine, moves):
    panel = pygame.Surface((config.WIDTH, config.HUD_HEIGHT))
    draw_gradient(panel, (25, 25, 45), (15, 15, 30), vertical=True)
    config.screen.blit(panel, (0, 0))
    pygame.draw.line(config.screen, (80, 80, 110), (0, config.HUD_HEIGHT), (config.WIDTH, config.HUD_HEIGHT), 2)

    if getattr(engine, "mode", "standard") == "calendar_pride_maze":
        icon = draw_rainbow_icon(40)
        phase_text = "PRIDE MAZE"
        phase_color = (255, 215, 0)
    elif getattr(engine, "mode", "standard") == "calendar_world_environment_day":
        icon = draw_rainbow_icon(40)
        phase_text = "ENV. DAY"
        phase_color = (50, 255, 50)
    elif getattr(engine, "mode", "standard") == "calendar_world_oceans_day":
        icon = draw_wave_icon(40)
        phase_text = "OCEANS DAY"
        phase_color = (100, 200, 255)
    elif getattr(engine, "mode", "standard") == "calendar_juneteenth":
        icon = draw_bell_icon(40)
        phase_text = "JUNETEENTH"
        phase_color = (200, 30, 30)
    elif getattr(engine, "mode", "standard") == "calendar_fathers_day":
        icon = draw_tie_icon(40)
        phase_text = "FATHER'S DAY"
        phase_color = (135, 206, 250)
    elif getattr(engine, "mode", "standard") == "calendar_world_music_day":
        icon = draw_music_note_icon(40)
        phase_text = "MUSIC DAY"
        phase_color = (255, 105, 180)
    elif engine.is_day:
        icon = draw_sun_icon(40, engine.sun_angle)
        phase_text = "DAY"
        phase_color = (255, 200, 50)
    else:
        icon = draw_moon_icon(40)
        phase_text = "NIGHT"
        phase_color = (180, 160, 255)
    config.screen.blit(icon, (10, 10))
    
    title_display = "SOLSTICE SHIFT" if getattr(engine, "mode", "standard") == "solstice_shift" else phase_text
    if getattr(engine, "mode", "standard") in ["calendar_pride_maze", "calendar_world_environment_day", "calendar_world_oceans_day", "calendar_juneteenth", "calendar_fathers_day", "calendar_world_music_day"]:
        title_display = phase_text
    txt_phase = config.fonts['hud_title'].render(title_display, True, phase_color)
    config.screen.blit(txt_phase, (55, 15))
    
    if getattr(engine, "mode", "standard") not in ["calendar_pride_maze", "calendar_world_environment_day", "calendar_world_oceans_day", "calendar_juneteenth", "calendar_fathers_day", "calendar_world_music_day"]:
        dial_center = (config.WIDTH // 2, 45)
        dial_radius = 30
        pygame.draw.circle(config.screen, (30, 30, 45), dial_center, dial_radius)
        pygame.draw.circle(config.screen, (80, 80, 110), dial_center, dial_radius, 2)
        pygame.draw.line(config.screen, (80, 80, 110), (dial_center[0] - dial_radius, dial_center[1]), (dial_center[0] + dial_radius, dial_center[1]), 1)
        
        rad_angle = math.radians(engine.sun_angle - 180)
        dot_x = dial_center[0] + math.cos(rad_angle) * (dial_radius - 6)
        dot_y = dial_center[1] + math.sin(rad_angle) * (dial_radius - 6)
        dot_color = (255, 200, 50) if engine.is_day else (180, 160, 255)
        pygame.draw.circle(config.screen, dot_color, (int(dot_x), int(dot_y)), 5)

    if getattr(engine, "mode", "standard") == "calendar_pride_maze":
        collected = len(getattr(engine, "collected_prisms", []))
        if collected < 6:
            order = getattr(engine, "prism_order", ["red", "orange", "yellow", "green", "blue", "purple"])
            next_color = order[collected] if collected < len(order) else "unknown"
            color_map = {"red": (255, 50, 50), "orange": (255, 150, 0), "yellow": (255, 230, 0), "green": (50, 255, 50), "blue": (50, 150, 255), "purple": (200, 50, 255)}
            c_val = color_map.get(next_color, (255, 255, 255))
            txt_prisms = config.fonts['hud_title'].render(f"NEXT: {next_color.upper()}", True, c_val)
        else:
            txt_prisms = config.fonts['hud_title'].render("GO TO CENTER!", True, (255, 255, 255))
        config.screen.blit(txt_prisms, (config.WIDTH - 160, 30))
    elif getattr(engine, "mode", "standard") == "calendar_world_environment_day":
        coverage = len(getattr(engine, "grass_tiles", set()))
        required = int(0.8 * getattr(engine, "grid_size", 10) ** 2)
        txt_cov = config.fonts['hud_title'].render(f"COVERAGE: {coverage}/{required}", True, (50, 255, 50))
        config.screen.blit(txt_cov, (config.WIDTH - 180, 30))
    elif getattr(engine, "mode", "standard") == "calendar_world_oceans_day":
        turtles_left = len(getattr(engine, "turtles", set()))
        turtles_rescued = 4 - turtles_left
        
        tide_text = "HIGH TIDE" if getattr(engine, "is_high_tide", True) else "LOW TIDE"
        tide_color = (100, 150, 255) if getattr(engine, "is_high_tide", True) else (50, 200, 200)
        timer = getattr(engine, "tide_timer", 0)
        
        txt_turtles = config.fonts['hud_title'].render(f"RESCUED: {turtles_rescued}/4", True, (100, 200, 255))
        txt_tide = config.fonts['hud_title'].render(f"{tide_text} (Next in {timer})", True, tide_color)
        
        turtle_x = config.WIDTH - 65 - txt_turtles.get_width()
        tide_x = config.WIDTH - 65 - txt_tide.get_width()
        
        config.screen.blit(txt_turtles, (turtle_x, 20))
        config.screen.blit(txt_tide, (tide_x, 45))
    elif getattr(engine, "mode", "standard") == "calendar_juneteenth":
        bells_left = len(getattr(engine, "freedom_bells", {}))
        stars_left = len(getattr(engine, "freedom_stars", set()))
        if bells_left > 0:
            txt = config.fonts['hud_title'].render(f"GOAL: RING THE BELLS ({3 - bells_left}/3)", True, (255, 215, 0))
            config.screen.blit(txt, (config.WIDTH - 300, 30))
        else:
            stars_collected = 3 - stars_left
            txt = config.fonts['hud_title'].render(f"STARS: {stars_collected}/3", True, (255, 215, 0))
            config.screen.blit(txt, (config.WIDTH - 150, 30))
    elif getattr(engine, "mode", "standard") == "calendar_fathers_day":
        energy = getattr(engine, "dad_energy", 100.0)
        bar_w = 120
        bar_h = 16
        bar_x = config.WIDTH - bar_w - 20
        bar_y = 15
        
        if energy > 50:
            bar_color = (50, 220, 50)
        elif energy > 20:
            bar_color = (220, 180, 50)
        else:
            bar_color = (220, 50, 50)
            
        pygame.draw.rect(config.screen, (40, 40, 50), (bar_x, bar_y, bar_w, bar_h), border_radius=4)
        pygame.draw.rect(config.screen, bar_color, (bar_x, bar_y, int(bar_w * (energy / 100.0)), bar_h), border_radius=4)
        pygame.draw.rect(config.screen, (100, 100, 120), (bar_x, bar_y, bar_w, bar_h), 1, border_radius=4)
        
        txt_energy = config.fonts['hud_title'].render(f"ENERGY: {int(energy)}%", True, (255, 255, 255))
        config.screen.blit(txt_energy, (bar_x - txt_energy.get_width() - 10, bar_y - 2))
        
        collected = getattr(engine, "collected_items", set())
        checklist_y = 45
        checklist_items = [("GRILL", "grill", draw_grill), ("TIE", "tie", draw_tie_item), ("MUG", "mug", draw_mug)]
        draw_x = config.WIDTH - 310
        for label, key, draw_fn in checklist_items:
            is_collected = key in collected
            slot_rect = pygame.Rect(draw_x, checklist_y, 22, 22)
            pygame.draw.rect(config.screen, (30, 30, 45), slot_rect, border_radius=4)
            pygame.draw.rect(config.screen, (100, 100, 130) if is_collected else (50, 50, 70), slot_rect, 1, border_radius=4)
            
            item_surf = draw_fn(16)
            if not is_collected:
                item_surf.set_alpha(80)
            else:
                item_surf.set_alpha(255)
                pygame.draw.rect(config.screen, (50, 220, 50), slot_rect, 1, border_radius=4)
                
            config.screen.blit(item_surf, (draw_x + 3, checklist_y + 3))
            
            color = (255, 215, 0) if is_collected else (130, 130, 150)
            txt_item = config.fonts['game_text'].render(label, True, color)
            config.screen.blit(txt_item, (draw_x + 28, checklist_y + 3))
            draw_x += 85
    elif getattr(engine, "mode", "standard") == "calendar_world_music_day":
        tempo = getattr(engine, "beat_counter", 0) + 1
        if tempo == 4:
            tempo_text = "BEAT: 4/4 [BLAST!]"
            tempo_color = (255, 80, 80)
        elif tempo == 3:
            tempo_text = "BEAT: 3/4 [WARNING]"
            tempo_color = (255, 165, 0)
        else:
            tempo_text = f"BEAT: {tempo}/4"
            tempo_color = (100, 255, 100)
        txt_tempo = config.fonts['hud_text'].render(tempo_text, True, tempo_color)
        config.screen.blit(txt_tempo, (55, 45))

        seq = getattr(engine, "note_sequence", [])
        seq_idx = getattr(engine, "player_seq_idx", 0)
        color_map = {"red": (255, 50, 50), "blue": (50, 150, 255), "green": (50, 255, 50), "yellow": (255, 230, 0)}
        
        draw_x = config.WIDTH - 180
        for i, color_name in enumerate(seq):
            is_completed = i < seq_idx
            is_next = i == seq_idx
            c_val = color_map.get(color_name, (255, 255, 255))
            
            note_rect = pygame.Rect(draw_x, 25, 22, 22)
            pygame.draw.rect(config.screen, (30, 30, 45), note_rect, border_radius=4)
            
            note_surf = draw_musical_note(16, c_val)
            if not is_completed and not is_next:
                note_surf.set_alpha(80)
            config.screen.blit(note_surf, (draw_x + 3, 28))
            
            if is_completed:
                pygame.draw.rect(config.screen, (50, 220, 50), note_rect, 1, border_radius=4)
            elif is_next:
                pygame.draw.rect(config.screen, (255, 255, 255), note_rect, 1, border_radius=4)
                
            if i < len(seq) - 1:
                arrow_color = (50, 220, 50) if is_completed else (100, 100, 110)
                line_y = 25 + 11
                pygame.draw.line(config.screen, arrow_color, (draw_x + 26, line_y), (draw_x + 34, line_y), 2)
                pygame.draw.line(config.screen, arrow_color, (draw_x + 31, line_y - 3), (draw_x + 34, line_y), 2)
                pygame.draw.line(config.screen, arrow_color, (draw_x + 31, line_y + 3), (draw_x + 34, line_y), 2)
                
            draw_x += 38
    else:
        sun_icon = draw_sun_stone(20)
        moon_icon = draw_moon_stone(20)
        config.screen.blit(sun_icon, (config.WIDTH - 120, 15))
        config.screen.blit(moon_icon, (config.WIDTH - 60, 15))
        
        txt_sun = config.fonts['hud_numbers'].render(str(len(engine.sun_stones)), True, (255, 215, 0))
        txt_moon = config.fonts['hud_numbers'].render(str(len(engine.moon_stones)), True, (200, 160, 255))
        config.screen.blit(txt_sun, (config.WIDTH - 95, 35))
        config.screen.blit(txt_moon, (config.WIDTH - 35, 35))

    txt_moves = config.fonts['hud_text'].render(f"Moves: {moves}", True, config.COLOR_TEXT)
    is_calendar = getattr(engine, "mode", "standard").startswith("calendar_")
    moves_y = 68 if is_calendar else 80
    config.screen.blit(txt_moves, (config.WIDTH // 2 - txt_moves.get_width()//2, moves_y))

    help_center = (config.WIDTH - 40, 75)
    pygame.draw.circle(config.screen, (40, 45, 70), help_center, 15)
    pygame.draw.circle(config.screen, (255, 180, 50), help_center, 15, 2)
    txt_help = config.fonts['hud_title'].render("!", True, (255, 180, 50))
    config.screen.blit(txt_help, (help_center[0] - txt_help.get_width()//2, help_center[1] - txt_help.get_height()//2))
