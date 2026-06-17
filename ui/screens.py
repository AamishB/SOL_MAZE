import pygame
import sys
import math
import asyncio
import config
from graphics import (
    draw_rainbow_icon,
    draw_leaf_icon,
    draw_wave_icon,
    draw_bell_icon,
    draw_tie_icon,
    draw_music_note_icon,
    draw_sun_icon
)

async def screen_transition():
    fade = pygame.Surface((config.WIDTH, config.HEIGHT))
    fade.fill((0, 0, 0))
    for alpha in range(0, 255, 20):
        fade.set_alpha(alpha)
        config.screen.blit(fade, (0, 0))
        pygame.display.flip()
        config.clock.tick(60)
        await asyncio.sleep(0)

async def show_fail_screen(reason):
    fade_surf = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
    for alpha in range(0, 180, 10):
        fade_surf.fill((50, 0, 0, alpha))
        config.screen.blit(fade_surf, (0, 0))
        pygame.display.flip()
        config.clock.tick(60)
        await asyncio.sleep(0)

    options = ["RETRY", "MAIN MENU"]
    selected = 0
    button_width = 200
    button_height = 50
    start_y = 350
    
    finish_bg = config.get_finish_background()
    while True:
        config.screen.blit(finish_bg, (0, 0))
        veil = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        veil.fill((30, 5, 5, 200))
        config.screen.blit(veil, (0, 0))
        
        txt_title = config.fonts['game_large'].render("GAME OVER", True, (255, 50, 50))
        config.screen.blit(txt_title, (config.WIDTH // 2 - txt_title.get_width() // 2, 170))
        
        txt_reason = config.fonts['game_text'].render(reason, True, (245, 246, 250))
        config.screen.blit(txt_reason, (config.WIDTH // 2 - txt_reason.get_width() // 2, 215))
        
        for i, opt in enumerate(options):
            button_rect = pygame.Rect(config.WIDTH // 2 - button_width // 2, start_y + i * 65, button_width, button_height)
            if i == selected:
                pygame.draw.rect(config.screen, (255, 100, 100, 180), button_rect, border_radius=10)
                pygame.draw.rect(config.screen, (255, 150, 150), button_rect, 3, border_radius=10)
                color = (0, 0, 0)
            else:
                pygame.draw.rect(config.screen, (60, 20, 20, 150), button_rect, border_radius=10)
                pygame.draw.rect(config.screen, (130, 50, 50), button_rect, 2, border_radius=10)
                color = config.COLOR_TEXT
            txt = config.fonts['button'].render(opt, True, color)
            txt_rect = txt.get_rect(center=(config.WIDTH // 2, start_y + i * 65 + button_height // 2))
            config.screen.blit(txt, txt_rect)
            
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "menu"
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                for i in range(len(options)):
                    button_rect = pygame.Rect(config.WIDTH // 2 - button_width // 2, start_y + i * 65, button_width, button_height)
                    if button_rect.collidepoint(mx, my):
                        selected = i
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    for i, opt in enumerate(options):
                        button_rect = pygame.Rect(config.WIDTH // 2 - button_width // 2, start_y + i * 65, button_width, button_height)
                        if button_rect.collidepoint(mx, my):
                            selected = i
                            if opt == "RETRY": return "replay"
                            elif opt == "MAIN MENU": return "menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN: selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "RETRY": return "replay"
                    elif options[selected] == "MAIN MENU": return "menu"
        config.clock.tick(config.FPS)
        await asyncio.sleep(0)

async def show_win_screen(moves, mode="standard"):
    fade_surf = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
    for alpha in range(0, 180, 10):
        fade_surf.fill((0, 0, 0, alpha))
        config.screen.blit(fade_surf, (0, 0))
        pygame.display.flip()
        config.clock.tick(60)
        await asyncio.sleep(0)

    theme_info = {
        "calendar_pride_maze": {
            "title": "PRIDE CELEBRATED!",
            "title_color": (255, 105, 180),
            "shadow_color": (80, 20, 40),
            "rank_label": "PRIDE RANK:",
            "ranks": ["Prismatic Pride", "Rainbow Rider", "Color Seeker"],
            "icon_fn": lambda: draw_rainbow_icon(70)
        },
        "calendar_world_environment_day": {
            "title": "ECOSYSTEM RESTORED!",
            "title_color": (50, 255, 50),
            "shadow_color": (10, 80, 10),
            "rank_label": "ECO RANK:",
            "ranks": ["Green Guardian", "Forest Friend", "Sprout Seeker"],
            "icon_fn": lambda: draw_leaf_icon(70)
        },
        "calendar_world_oceans_day": {
            "title": "VOYAGE COMPLETED!",
            "title_color": (100, 200, 255),
            "shadow_color": (20, 50, 80),
            "rank_label": "OCEAN RANK:",
            "ranks": ["Abyssal Admiral", "Sea Captain", "Wave Wanderer"],
            "icon_fn": lambda: draw_wave_icon(70)
        },
        "calendar_juneteenth": {
            "title": "FREEDOM ACHIEVED!",
            "title_color": (255, 215, 0),
            "shadow_color": (80, 60, 10),
            "rank_label": "FREEDOM RANK:",
            "ranks": ["Liberty Liberator", "Bell Ringer", "Freedom Seeker"],
            "icon_fn": lambda: draw_bell_icon(70)
        },
        "calendar_fathers_day": {
            "title": "HAPPY FATHER'S DAY!",
            "title_color": (135, 206, 250),
            "shadow_color": (20, 50, 80),
            "rank_label": "DAD RANK:",
            "ranks": ["Grill Master Supreme", "Lawn Care Legend", "Dad Lore Apprentice"],
            "icon_fn": lambda: draw_tie_icon(70)
        },
        "calendar_world_music_day": {
            "title": "STAGE CLEARED!",
            "title_color": (255, 105, 180),
            "shadow_color": (80, 20, 40),
            "rank_label": "MUSIC RANK:",
            "ranks": ["Virtuoso Rockstar", "Beat Maestro", "Melody Maker"],
            "icon_fn": lambda: draw_music_note_icon(70)
        }
    }

    info = theme_info.get(mode, {
        "title": "HARMONY ACHIEVED!",
        "title_color": (255, 215, 0),
        "shadow_color": (80, 60, 10),
        "rank_label": "SOLSTICE RANK:",
        "ranks": ["Celestial Sovereign", "Star Navigator", "Solstice Seeker"],
        "icon_fn": lambda: draw_sun_icon(70)
    })

    if moves < 100:
        rating_text = info["ranks"][0]
        rating_color = (255, 215, 0)
    elif moves <= 150:
        rating_text = info["ranks"][1]
        rating_color = (190, 210, 255)
    else:
        rating_text = info["ranks"][2]
        rating_color = (205, 127, 50)

    options = ["PLAY AGAIN", "MAIN MENU"]
    selected = 0
    
    float_offset = 0
    float_direction = 1
    
    button_width = 200
    button_height = 50
    start_y = 350
    
    finish_bg = config.get_finish_background()
    while True:
        config.screen.blit(finish_bg, (0, 0))
        
        veil = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        veil.fill((10, 12, 25, 160))
        config.screen.blit(veil, (0, 0))
        
        float_offset += 0.05 * float_direction
        if float_offset > 5 or float_offset < -5:
            float_direction *= -1
            
        win_icon = info["icon_fn"]()
        icon_y = 70 + float_offset
        config.screen.blit(win_icon, (config.WIDTH // 2 - 35, icon_y))
        
        txt_title = config.fonts['game_large'].render(info["title"], True, info["title_color"])
        txt_title_shadow = config.fonts['game_large'].render(info["title"], True, info["shadow_color"])
        config.screen.blit(txt_title_shadow, (config.WIDTH // 2 - txt_title.get_width() // 2 + 1, 170 + 1))
        config.screen.blit(txt_title, (config.WIDTH // 2 - txt_title.get_width() // 2, 170))
        
        txt_steps = config.fonts['game_text'].render(f"Completed in {moves} moves", True, (245, 246, 250))
        config.screen.blit(txt_steps, (config.WIDTH // 2 - txt_steps.get_width() // 2, 215))
        
        if mode == "solstice_shift":
            txt_mode = config.fonts['instructions'].render("SOLSTICE SHIFT CLEARED", True, (255, 180, 50))
            config.screen.blit(txt_mode, (config.WIDTH // 2 - txt_mode.get_width() // 2, 235))
        
        txt_rating_label = config.fonts['instructions'].render(info["rank_label"], True, (180, 180, 200))
        txt_rating = config.fonts['hud_title'].render(rating_text.upper(), True, rating_color)
        config.screen.blit(txt_rating_label, (config.WIDTH // 2 - txt_rating_label.get_width() // 2, 255))
        config.screen.blit(txt_rating, (config.WIDTH // 2 - txt_rating.get_width() // 2, 275))
        
        for i, opt in enumerate(options):
            button_rect = pygame.Rect(config.WIDTH // 2 - button_width // 2, start_y + i * 65, button_width, button_height)
            
            if i == selected:
                pygame.draw.rect(config.screen, (255, 180, 50, 180), button_rect, border_radius=10)
                pygame.draw.rect(config.screen, (255, 200, 80), button_rect, 3, border_radius=10)
                color = (0, 0, 0)
            else:
                pygame.draw.rect(config.screen, (40, 40, 60, 150), button_rect, border_radius=10)
                pygame.draw.rect(config.screen, (100, 100, 130), button_rect, 2, border_radius=10)
                color = config.COLOR_TEXT
                
            txt = config.fonts['button'].render(opt, True, color)
            txt_rect = txt.get_rect(center=(config.WIDTH // 2, start_y + i * 65 + button_height // 2))
            config.screen.blit(txt, txt_rect)
            
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "menu"
                
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                for i in range(len(options)):
                    button_rect = pygame.Rect(config.WIDTH // 2 - button_width // 2, start_y + i * 65, button_width, button_height)
                    if button_rect.collidepoint(mx, my):
                        selected = i
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    for i, opt in enumerate(options):
                        button_rect = pygame.Rect(config.WIDTH // 2 - button_width // 2, start_y + i * 65, button_width, button_height)
                        if button_rect.collidepoint(mx, my):
                            selected = i
                            if opt == "PLAY AGAIN":
                                return "replay"
                            elif opt == "MAIN MENU":
                                return "menu"
                                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    config.toggle_fullscreen()
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "PLAY AGAIN":
                        return "replay"
                    elif options[selected] == "MAIN MENU":
                        return "menu"
                elif event.key == pygame.K_ESCAPE:
                    return "menu"
                elif event.key == pygame.K_r:
                    return "replay"
                    
        config.clock.tick(config.FPS)
        await asyncio.sleep(0)

async def show_pause_menu():
    background_copy = config.screen.copy()
    
    small_bg = pygame.transform.smoothscale(background_copy, (config.WIDTH // 8, config.HEIGHT // 8))
    blurred_bg = pygame.transform.smoothscale(small_bg, (config.WIDTH, config.HEIGHT))
    
    overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 12, 25, 120))
    
    pane_surf = pygame.Surface((280, 320), pygame.SRCALPHA)
    
    options = ["RESUME", "RESTART", "MAIN MENU"]
    selected = 0
    
    while True:
        config.screen.blit(blurred_bg, (0, 0))
        config.screen.blit(overlay, (0, 0))
        
        pane_surf.fill((0, 0, 0, 0))
        pygame.draw.rect(pane_surf, (20, 25, 45, 230), (0, 0, 280, 320), border_radius=15)
        pygame.draw.rect(pane_surf, (255, 180, 50), (0, 0, 280, 320), 2, border_radius=15)
        
        txt_paused = config.fonts['game_large'].render("PAUSED", True, (255, 215, 0))
        pane_surf.blit(txt_paused, (140 - txt_paused.get_width() // 2, 30))
        pygame.draw.line(pane_surf, (80, 80, 110), (40, 70), (240, 70), 1)
        
        btn_start_y = 100
        btn_w, btn_h = 200, 42
        
        for i, opt in enumerate(options):
            bx = 140 - btn_w // 2
            by = btn_start_y + i * 60
            btn_rect = pygame.Rect(bx, by, btn_w, btn_h)
            
            if i == selected:
                pygame.draw.rect(pane_surf, (255, 180, 50), btn_rect, border_radius=8)
                color = (0, 0, 0)
            else:
                pygame.draw.rect(pane_surf, (35, 40, 65), btn_rect, border_radius=8)
                pygame.draw.rect(pane_surf, (80, 80, 110), btn_rect, 1, border_radius=8)
                color = config.COLOR_TEXT
                
            txt = config.fonts['button'].render(opt, True, color)
            txt_rect = txt.get_rect(center=(140, by + btn_h // 2))
            pane_surf.blit(txt, txt_rect)
            
        config.screen.blit(pane_surf, (config.WIDTH // 2 - 140, config.HEIGHT // 2 - 160))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "menu"
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                pane_x, pane_y = config.WIDTH // 2 - 140, config.HEIGHT // 2 - 160
                for i in range(len(options)):
                    bx = 140 - btn_w // 2
                    by = btn_start_y + i * 60
                    button_rect = pygame.Rect(pane_x + bx, pane_y + by, btn_w, btn_h)
                    if button_rect.collidepoint(mx, my):
                        selected = i
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    pane_x, pane_y = config.WIDTH // 2 - 140, config.HEIGHT // 2 - 160
                    for i in range(len(options)):
                        bx = 140 - btn_w // 2
                        by = btn_start_y + i * 60
                        button_rect = pygame.Rect(pane_x + bx, pane_y + by, btn_w, btn_h)
                        if button_rect.collidepoint(mx, my):
                            selected = i
                            if options[selected] == "RESUME":
                                return "resume"
                            elif options[selected] == "RESTART":
                                return "restart"
                            elif options[selected] == "MAIN MENU":
                                await screen_transition()
                                return "menu"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    config.toggle_fullscreen()
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "RESUME":
                        return "resume"
                    elif options[selected] == "RESTART":
                        return "restart"
                    elif options[selected] == "MAIN MENU":
                        await screen_transition()
                        return "menu"
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    return "resume"
                    
        config.clock.tick(config.FPS)
        await asyncio.sleep(0)

async def show_help_screen(mode="standard"):
    background_copy = config.screen.copy()
    overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 12, 25, 180))
    
    pane_surf = pygame.Surface((380, 440), pygame.SRCALPHA)
    
    while True:
        config.screen.blit(background_copy, (0, 0))
        config.screen.blit(overlay, (0, 0))
        
        pane_surf.fill((0, 0, 0, 0))
        pygame.draw.rect(pane_surf, (20, 25, 45, 240), (0, 0, 380, 440), border_radius=15)
        pygame.draw.rect(pane_surf, (255, 180, 50), (0, 0, 380, 440), 2, border_radius=15)
        
        txt_title = config.fonts['game_large'].render("HOW TO PLAY", True, (255, 215, 0))
        pane_surf.blit(txt_title, (190 - txt_title.get_width() // 2, 20))
        pygame.draw.line(pane_surf, (80, 80, 110), (40, 55), (340, 55), 1)
        
        if mode == "solstice_shift":
            lines = [
                "MODE: SOLSTICE SHIFT",
                "- Day: Walk on field. Pits are deadly.",
                "- Night: Field is dark. Pits are safe bridges.",
                "- Phase shifts every 10 moves.",
                "- CAUTION: Get off bridges before Day",
                "- Teleports occur at Dawn. 200 move limit.",
                "",
                "ESC / P: Pause | H: Help"
            ]
        elif mode == "calendar_pride_maze":
            lines = [
                "MODE: PRIDE MAZE",
                "- Movement: Slide 2 tiles at a time.",
                "- Prisms: Collect in ROYGBIV order.",
                "- Gates: Shatter solid gates by finding",
                "  the matching Prism.",
                "- Goal: Reach the Rainbow Bridge!",
                "",
                "ESC / P: Pause | H: Help"
            ]
        elif mode == "calendar_world_environment_day":
            lines = [
                "MODE: ENVIRONMENT DAY",
                "- Click anywhere to start.",
                "- Move to plant grass.",
                "- CAUTION: You cannot step on grass or trash",
                "  until 80% coverage is reached.",
                "- Loop around trash to destroy it!",
                "- Reach the Tree of Life to win.",
                "",
                "ESC / P: Pause | H: Help"
            ]
        elif mode == "calendar_world_oceans_day":
            lines = [
                "MODE: OCEANS DAY",
                "- High Tide: Reefs are safe,",
                "Trenches are deadly.",
                "- Low Tide: Trenches are safe,",
                "Reefs are solid.",
                "- Beware: Random currents can sweep you away!",
                "- Rescue all 4 turtles and reach the Whirlpool.",
                "- TAB/S: Skip turn (Advance Tide)",
                "",
                "ESC / P: Pause | H: Help"
            ]
        elif mode == "calendar_juneteenth":
            lines = [
                "MODE: JUNETEENTH",
                "- Explore to find the 3 Freedom Bells.",
                "- Ringing a Bell shatters ",
                "specific Shadow Walls.",
                "- Collect the 3 trapped Freedom Stars.",
                "- The exit opens once all Stars are collected.",
                "",
                "ESC / P: Pause | H: Help"
            ]
        elif mode == "calendar_fathers_day":
            lines = [
                "MODE: FATHER'S DAY",
                "- Collect the 3 scattered Dad Lore items:",
                "  The Grill, The Tie, and The Mug.",
                "- Keep Energy up! Stepping reduces Energy.",
                "- Drink Coffee Cups to restore 30% Energy.",
                "- Reach the Lawn Chair exit to win.",
                "- Avoid Lawn Gnomes, Bushes, and Hoses!",
                "",
                "ESC / P: Pause | H: Help"
            ]
        elif mode == "calendar_world_music_day":
            lines = [
                "MODE: WORLD MUSIC DAY",
                "- Step on the notes in the HUD sequence",
                "- Obstacles: Drums, Mics, Speakers.",
                "- Every 4 moves, Speakers emit a Sonic Blast",
                "  spreading 3 tiles cardinally.",
                "- Hit by blast or wrong note resets sequence",
                "  and pushes you back!",
                "- Reach the Treble Clef exit to win.",
                "",
                "ESC / P: Pause | H: Help"
            ]
        else:
            lines = [
                "Goal: Collect all stones",
                "Day: Walk on Light paths.",
                "Night: Walk on Shadow paths.",
                "",
                "CONTROLS:",
                "Arrow Keys: Move | Spacebar: Wait",
                "TAB / S: Skip Day or Night",
                "ESC / P: Pause | H: Help"
            ]
        
        y = 70
        for line in lines:
            color = (255, 215, 0) if "CONTROLS" in line else config.COLOR_TEXT
            font_to_use = config.fonts['hud_title'] if "CONTROLS" in line else config.fonts['game_text']
            txt = font_to_use.render(line, True, color)
            pane_surf.blit(txt, (190 - txt.get_width() // 2, y))
            y += 24 if "CONTROLS" not in line else 35
            
        btn_rect = pygame.Rect(90, 380, 200, 40)
        pygame.draw.rect(pane_surf, (255, 180, 50), btn_rect, border_radius=8)
        txt_btn = config.fonts['button'].render("GOT IT", True, (0, 0, 0))
        pane_surf.blit(txt_btn, (190 - txt_btn.get_width() // 2, 385))
        
        config.screen.blit(pane_surf, (config.WIDTH // 2 - 190, config.HEIGHT // 2 - 220))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    config.toggle_fullscreen()
                elif event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_h, pygame.K_SPACE):
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                pane_x, pane_y = config.WIDTH // 2 - 190, config.HEIGHT // 2 - 220
                if btn_rect.collidepoint(x - pane_x, y - pane_y):
                    return
        config.clock.tick(config.FPS)
        await asyncio.sleep(0)

async def show_under_construction_popup(mode_name):
    background_copy = config.screen.copy()
    overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    
    pane_surf = pygame.Surface((300, 200), pygame.SRCALPHA)
    
    while True:
        config.screen.blit(background_copy, (0, 0))
        config.screen.blit(overlay, (0, 0))
        
        pane_surf.fill((0, 0, 0, 0))
        pygame.draw.rect(pane_surf, (25, 30, 50, 240), (0, 0, 300, 200), border_radius=12)
        pygame.draw.rect(pane_surf, (255, 100, 100), (0, 0, 300, 200), 2, border_radius=12)
        
        txt_title = config.fonts['game_large'].render("COMING SOON", True, (255, 100, 100))
        pane_surf.blit(txt_title, (150 - txt_title.get_width() // 2, 25))
        
        lines = [
            f"{mode_name}",
            "is currently locked.",
            "Please play Standard Mode!"
        ]
        y_offset = 70
        for line in lines:
            txt_line = config.fonts['hud_text'].render(line, True, config.COLOR_TEXT)
            pane_surf.blit(txt_line, (150 - txt_line.get_width() // 2, y_offset))
            y_offset += 22
            
        btn_rect = pygame.Rect(100, 145, 100, 35)
        pygame.draw.rect(pane_surf, (255, 100, 100), btn_rect, border_radius=6)
        txt_btn = config.fonts['button'].render("OK", True, (0, 0, 0))
        pane_surf.blit(txt_btn, (150 - txt_btn.get_width() // 2, 148))
        
        config.screen.blit(pane_surf, (config.WIDTH // 2 - 150, config.HEIGHT // 2 - 100))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_SPACE):
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    pane_x, pane_y = config.WIDTH // 2 - 150, config.HEIGHT // 2 - 100
                    if btn_rect.collidepoint(mx - pane_x, my - pane_y):
                        return
        config.clock.tick(config.FPS)
        await asyncio.sleep(0)
