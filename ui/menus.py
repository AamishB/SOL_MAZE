import pygame
import sys
import random
import asyncio
import config
from graphics import (
    draw_sun_icon,
    draw_moon_icon,
    draw_leaf_icon,
    draw_wave_icon,
    draw_bell_icon,
    draw_tie_icon,
    draw_music_note_icon,
    draw_rainbow_icon,
    draw_character
)
from ui.screens import (
    screen_transition,
    show_under_construction_popup
)
from ui.game import play_game

async def show_settings_menu():
    background_copy = config.screen.copy()
    overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 12, 25, 180))
    pane_surf = pygame.Surface((320, 310), pygame.SRCALPHA)
    
    options = [
        "Fullscreen: " + ("ON" if config.is_fullscreen else "OFF"),
        "God Rays: " + ("ON" if config.settings_god_rays else "OFF"),
        "BACK"
    ]
    selected = 0
    
    while True:
        config.screen.blit(background_copy, (0, 0))
        config.screen.blit(overlay, (0, 0))
        
        pane_surf.fill((0, 0, 0, 0))
        pygame.draw.rect(pane_surf, (20, 25, 45, 240), (0, 0, 320, 310), border_radius=15)
        pygame.draw.rect(pane_surf, (255, 180, 50), (0, 0, 320, 310), 2, border_radius=15)
        
        txt_title = config.fonts['game_large'].render("SETTINGS", True, (255, 215, 0))
        pane_surf.blit(txt_title, (160 - txt_title.get_width() // 2, 20))
        pygame.draw.line(pane_surf, (80, 80, 110), (40, 55), (280, 55), 1)
        
        options[0] = "Fullscreen: " + ("ON" if config.is_fullscreen else "OFF")
        options[1] = "God Rays: " + ("ON" if config.settings_god_rays else "OFF")
        
        btn_start_y = 85
        btn_w, btn_h = 240, 42
        
        for i, opt in enumerate(options):
            bx = 160 - btn_w // 2
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
            txt_rect = txt.get_rect(center=(160, by + btn_h // 2))
            pane_surf.blit(txt, txt_rect)
            
        config.screen.blit(pane_surf, (config.WIDTH // 2 - 160, config.HEIGHT // 2 - 155))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                pane_x, pane_y = config.WIDTH // 2 - 160, config.HEIGHT // 2 - 155
                for i in range(len(options)):
                    bx = 160 - btn_w // 2
                    by = btn_start_y + i * 60
                    button_rect = pygame.Rect(pane_x + bx, pane_y + by, btn_w, btn_h)
                    if button_rect.collidepoint(mx, my):
                        selected = i
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    pane_x, pane_y = config.WIDTH // 2 - 160, config.HEIGHT // 2 - 155
                    for i, opt in enumerate(options):
                        bx = 160 - btn_w // 2
                        by = btn_start_y + i * 60
                        button_rect = pygame.Rect(pane_x + bx, pane_y + by, btn_w, btn_h)
                        if button_rect.collidepoint(mx, my):
                            selected = i
                            if i == 0:
                                config.toggle_fullscreen()
                            elif i == 1:
                                config.settings_god_rays = not config.settings_god_rays
                            elif i == 2:
                                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    config.toggle_fullscreen()
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        config.toggle_fullscreen()
                    elif selected == 1:
                        config.settings_god_rays = not config.settings_god_rays
                    elif selected == 2:
                        return
                elif event.key == pygame.K_ESCAPE:
                    return
        config.clock.tick(config.FPS)
        await asyncio.sleep(0)

async def show_calendar_hud():
    june_events = {
        1: {"name": "PRIDE MAZE", "icon": draw_rainbow_icon(35), "mode": "calendar_pride_maze"},
        5: {"name": "WORLD ENVIRONMENT DAY", "icon": draw_leaf_icon(35), "mode": "calendar_world_environment_day"},
        8: {"name": "WORLD OCEANS DAY", "icon": draw_wave_icon(35), "mode": "calendar_world_oceans_day"},
        19: {"name": "JUNETEENTH MAZE", "icon": draw_bell_icon(35), "mode": "calendar_juneteenth"},
        20: {"name": "SUMMER SOLSTICE", "icon": draw_sun_icon(35), "mode": "standard"},
        21: {
            "is_split": True,
            "top_left": {"name": "FATHERS DAY", "icon": draw_tie_icon(16), "mode": "calendar_fathers_day"},
            "bottom_right": {"name": "WORLD MUSIC DAY", "icon": draw_music_note_icon(25), "mode": "calendar_world_music_day"}
        }
    }
    
    panel_width = 480
    panel_height = 560
    panel_x = config.WIDTH // 2 - panel_width // 2
    panel_y = config.HEIGHT // 2 - panel_height // 2
    
    cell_w = 60
    cell_h = 60
    grid_x = panel_x + (panel_width - 7 * cell_w) // 2
    grid_y = panel_y + 100
    
    days_of_week = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"]
    
    start_day_idx = 1
    num_days = 30
    
    selected_day = None
    selected_sub = None
    hovered_day = None
    hovered_sub = None

    background_copy = config.screen.copy()
    overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 10, 15, 200))
    
    back_btn_rect = pygame.Rect(panel_x + panel_width//2 - 60, panel_y + panel_height - 55, 120, 40)
    
    while True:
        config.screen.blit(background_copy, (0, 0))
        config.screen.blit(overlay, (0, 0))
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(config.screen, (30, 30, 45, 240), panel_rect, border_radius=15)
        pygame.draw.rect(config.screen, (100, 100, 150), panel_rect, 3, border_radius=15)
        
        txt_title = config.fonts['hud_title'].render("JUNE CELEBRATIONS", True, (255, 215, 0))
        config.screen.blit(txt_title, (config.WIDTH // 2 - txt_title.get_width() // 2, panel_y + 20))
        
        for i, dow in enumerate(days_of_week):
            txt = config.fonts['hud_text'].render(dow, True, (150, 150, 180))
            cx = grid_x + i * cell_w + cell_w//2
            cy = grid_y - 20
            config.screen.blit(txt, (cx - txt.get_width()//2, cy - txt.get_height()//2))
            
        mx, my = pygame.mouse.get_pos()
        hovered_day = None
        hovered_sub = None
        
        for day in range(1, num_days + 1):
            idx = start_day_idx + day - 1
            col = idx % 7
            row = idx // 7
            
            cx = grid_x + col * cell_w
            cy = grid_y + row * cell_h
            cell_rect = pygame.Rect(cx, cy, cell_w, cell_h)
            
            is_hovered = cell_rect.collidepoint(mx, my)
            
            if day in june_events and isinstance(june_events[day], dict) and june_events[day].get("is_split"):
                hl_tl = False
                hl_br = False
                if is_hovered:
                    dx = mx - cx
                    dy = my - cy
                    if dx + dy < cell_w:
                        hl_tl = True
                        hovered_day = day
                        hovered_sub = "top_left"
                    else:
                        hl_br = True
                        hovered_day = day
                        hovered_sub = "bottom_right"
                
                if selected_day == day and selected_sub == "top_left":
                    color_tl = (100, 150, 255, 180)
                    border_color_tl = (200, 220, 255)
                elif hl_tl:
                    color_tl = (80, 100, 150, 150)
                    border_color_tl = (150, 180, 220)
                else:
                    color_tl = (40, 40, 60, 200)
                    border_color_tl = (60, 60, 80)
                    
                if selected_day == day and selected_sub == "bottom_right":
                    color_br = (100, 150, 255, 180)
                    border_color_br = (200, 220, 255)
                elif hl_br:
                    color_br = (80, 100, 150, 150)
                    border_color_br = (150, 180, 220)
                else:
                    color_br = (40, 40, 60, 200)
                    border_color_br = (60, 60, 80)
                
                pygame.draw.polygon(config.screen, color_tl, [(cx, cy), (cx + cell_w, cy), (cx, cy + cell_h)])
                pygame.draw.polygon(config.screen, color_br, [(cx + cell_w, cy), (cx + cell_w, cy + cell_h), (cx, cy + cell_h)])
                
                pygame.draw.polygon(config.screen, border_color_tl, [(cx, cy), (cx + cell_w, cy), (cx, cy + cell_h)], 1)
                pygame.draw.polygon(config.screen, border_color_br, [(cx + cell_w, cy), (cx + cell_w, cy + cell_h), (cx, cy + cell_h)], 1)
                pygame.draw.line(config.screen, (80, 80, 100), (cx, cy + cell_h), (cx + cell_w, cy), 1)
                
                icon_tl = june_events[day]["top_left"]["icon"]
                icon_tl_x = cx + 24
                icon_tl_y = cy + 3
                config.screen.blit(icon_tl, (icon_tl_x, icon_tl_y))
                
                icon_br = june_events[day]["bottom_right"]["icon"]
                icon_br_x = cx + 3 * cell_w // 4 - icon_br.get_width() // 2 - 3
                icon_br_y = cy + 3 * cell_h // 4 - icon_br.get_height() // 2
                config.screen.blit(icon_br, (icon_br_x, icon_br_y))
            else:
                if is_hovered and day in june_events:
                    hovered_day = day
                
                if day == selected_day:
                    pygame.draw.rect(config.screen, (100, 150, 255, 180), cell_rect, border_radius=5)
                    pygame.draw.rect(config.screen, (200, 220, 255), cell_rect, 2, border_radius=5)
                elif is_hovered and day in june_events:
                    pygame.draw.rect(config.screen, (80, 100, 150, 150), cell_rect, border_radius=5)
                    pygame.draw.rect(config.screen, (150, 180, 220), cell_rect, 1, border_radius=5)
                else:
                    pygame.draw.rect(config.screen, (40, 40, 60, 200), cell_rect, border_radius=5)
                    pygame.draw.rect(config.screen, (60, 60, 80), cell_rect, 1, border_radius=5)
                    
                if day in june_events:
                    icon = june_events[day]["icon"]
                    config.screen.blit(icon, (cx + cell_w//2 - icon.get_width()//2, cy + cell_h//2 - icon.get_height()//2 + 5))
                
            num_color = (255, 255, 255) if day in june_events else (100, 100, 100)
            txt_num = config.fonts['hud_numbers'].render(str(day), True, num_color)
            config.screen.blit(txt_num, (cx + 5, cy + 5))
                
        info_y = grid_y + 6 * cell_h + 10
        display_day = hovered_day or selected_day
        display_sub = hovered_sub or (selected_sub if (not hovered_day and selected_day == 21) else None)
        
        if display_day and display_day in june_events:
            event_data = june_events[display_day]
            if isinstance(event_data, dict) and event_data.get("is_split"):
                name = event_data[display_sub]["name"] if display_sub else "FATHERS DAY / MUSIC DAY"
                info_txt = config.fonts['button'].render(name, True, (255, 215, 0))
            else:
                info_txt = config.fonts['button'].render(event_data["name"], True, (255, 215, 0))
            config.screen.blit(info_txt, (config.WIDTH // 2 - info_txt.get_width() // 2, info_y))
        else:
            info_txt = config.fonts['hud_text'].render("Select a highlighted date", True, (150, 150, 150))
            config.screen.blit(info_txt, (config.WIDTH // 2 - info_txt.get_width() // 2, info_y + 5))
            
        is_back_hovered = back_btn_rect.collidepoint(mx, my)
        btn_color = (200, 50, 50) if is_back_hovered else (150, 40, 40)
        pygame.draw.rect(config.screen, btn_color, back_btn_rect, border_radius=8)
        pygame.draw.rect(config.screen, (255, 100, 100), back_btn_rect, 2, border_radius=8)
        b_txt = config.fonts['button'].render("BACK", True, config.COLOR_TEXT)
        config.screen.blit(b_txt, (back_btn_rect.centerx - b_txt.get_width()//2, back_btn_rect.centery - b_txt.get_height()//2))

        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "back"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_btn_rect.collidepoint(mx, my):
                        return "back"
                    if hovered_day:
                        event_data = june_events[hovered_day]
                        if isinstance(event_data, dict) and event_data.get("is_split"):
                            if selected_day == hovered_day and selected_sub == hovered_sub:
                                return event_data[hovered_sub]["mode"]
                            else:
                                selected_day = hovered_day
                                
                                selected_sub = hovered_sub
                        else:
                            if selected_day == hovered_day:
                                return event_data["mode"]
                            else:
                                selected_day = hovered_day
                                selected_sub = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "back"
                elif event.key == pygame.K_RETURN and selected_day:
                    event_data = june_events[selected_day]
                    if isinstance(event_data, dict) and event_data.get("is_split"):
                        if selected_sub:
                            return event_data[selected_sub]["mode"]
                    else:
                        return event_data["mode"]
        config.clock.tick(config.FPS)
        await asyncio.sleep(0)

async def show_mode_selection_hud():
    background_copy = config.screen.copy()
    overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
    overlay.fill((10, 12, 25, 180))
    
    pane_surf = pygame.Surface((320, 355), pygame.SRCALPHA)
    
    options = ["STANDARD MODE", "SOLSTICE SHIFT", "CELEBRATION CALENDAR", "BACK"]
    selected = 0
    
    descriptions = {
        "STANDARD MODE": "The classic Solstice Duality maze.",
        "CELEBRATION CALENDAR": "Play seasonal themed challenge mazes.",
        "SOLSTICE SHIFT": "Fast-paced Day/Night forced shifts.",
        "BACK": "Return to the main menu screen."
    }
    
    while True:
        config.screen.blit(background_copy, (0, 0))
        config.screen.blit(overlay, (0, 0))
        
        pane_surf.fill((0, 0, 0, 0))
        pygame.draw.rect(pane_surf, (20, 25, 45, 240), (0, 0, 320, 355), border_radius=15)
        pygame.draw.rect(pane_surf, (255, 180, 50), (0, 0, 320, 355), 2, border_radius=15)
        
        txt_title = config.fonts['game_large'].render("SELECT MODE", True, (255, 215, 0))
        pane_surf.blit(txt_title, (160 - txt_title.get_width() // 2, 20))
        pygame.draw.line(pane_surf, (80, 80, 110), (40, 55), (280, 55), 1)
        
        btn_start_y = 75
        btn_w, btn_h = 250, 42
        
        for i, opt in enumerate(options):
            bx = 160 - btn_w // 2
            by = btn_start_y + i * 55
            btn_rect = pygame.Rect(bx, by, btn_w, btn_h)
            
            if i == selected:
                pygame.draw.rect(pane_surf, (255, 180, 50), btn_rect, border_radius=8)
                color = (0, 0, 0)
            else:
                pygame.draw.rect(pane_surf, (35, 40, 65), btn_rect, border_radius=8)
                pygame.draw.rect(pane_surf, (80, 80, 110), btn_rect, 1, border_radius=8)
                color = config.COLOR_TEXT
                
            txt = config.fonts['mode_button'].render(opt, True, color)
            txt_rect = txt.get_rect(center=(160, by + btn_h // 2))
            pane_surf.blit(txt, txt_rect)
            
        hovered_mode = options[selected]
        if hovered_mode in descriptions:
            desc_text = descriptions[hovered_mode]
            desc_surf = config.fonts['instructions'].render(desc_text, True, (180, 180, 200))
            pane_surf.blit(desc_surf, (160 - desc_surf.get_width() // 2, 305))
            
        config.screen.blit(pane_surf, (config.WIDTH // 2 - 160, config.HEIGHT // 2 - 177))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "back"
            elif event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                pane_x, pane_y = config.WIDTH // 2 - 160, config.HEIGHT // 2 - 177
                for i in range(len(options)):
                    bx = 160 - btn_w // 2
                    by = btn_start_y + i * 55
                    button_rect = pygame.Rect(pane_x + bx, pane_y + by, btn_w, btn_h)
                    if button_rect.collidepoint(mx, my):
                        selected = i
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    pane_x, pane_y = config.WIDTH // 2 - 160, config.HEIGHT // 2 - 177
                    for i, opt in enumerate(options):
                        bx = 160 - btn_w // 2
                        by = btn_start_y + i * 55
                        button_rect = pygame.Rect(pane_x + bx, pane_y + by, btn_w, btn_h)
                        if button_rect.collidepoint(mx, my):
                            selected = i
                            if opt == "STANDARD MODE":
                                return "standard"
                            elif opt == "CELEBRATION CALENDAR":
                                res = await show_calendar_hud()
                                if res != "back": return res
                            elif opt == "SOLSTICE SHIFT":
                                return "solstice_shift"
                            elif opt == "BACK":
                                return "back"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    config.toggle_fullscreen()
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    opt = options[selected]
                    if opt == "STANDARD MODE":
                        return "standard"
                    elif opt == "CELEBRATION CALENDAR":
                        res = await show_calendar_hud()
                        if res != "back": return res
                    elif opt == "SOLSTICE SHIFT":
                        return "solstice_shift"
                    elif opt == "BACK":
                        return "back"
                elif event.key == pygame.K_ESCAPE:
                    return "back"
        config.clock.tick(config.FPS)
        await asyncio.sleep(0)

async def main_menu():
    def get_skin_name(name):
        return "Father" if name == "fathers_day" else name.capitalize()
    selected = 0
    skin_selected = 0
    skins = ["solstice", "pride", "juneteenth", "eclipse", "fathers_day", "rockstar"]
    
    # Force alignment of current skin
    if config.current_skin in skins:
        skin_selected = skins.index(config.current_skin)
        
    options = ["PLAY", "SKIN: " + get_skin_name(skins[skin_selected]), "SETTINGS", "QUIT"]
    
    float_offset = 0
    float_direction = 1
    
    stars = [{'x': random.randint(0, config.WIDTH), 'y': random.randint(0, config.HEIGHT), 'speed': random.uniform(0.1, 0.5), 'size': random.randint(1, 2)} for _ in range(60)]
    
    menu_bg = config.get_menu_background()
    while True:
        config.screen.blit(menu_bg, (0, 0))
        
        for star in stars:
            star['y'] += star['speed']
            if star['y'] > config.HEIGHT:
                star['y'] = 0
                star['x'] = random.randint(0, config.WIDTH)
            pygame.draw.circle(config.screen, (255, 255, 200, 150), (int(star['x']), int(star['y'])), star['size'])
        
        overlay = pygame.Surface((config.WIDTH, config.HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        config.screen.blit(overlay, (0, 0))
        
        float_offset += 0.05 * float_direction
        if float_offset > 5 or float_offset < -5:
            float_direction *= -1
        
        title_icon = draw_sun_icon(70)
        icon_y = 40 + float_offset
        config.screen.blit(title_icon, (config.WIDTH // 2 - 35, icon_y))
        
        title_text = config.fonts['title'].render("SOL MAZE", True, (255, 215, 0))
        title_shadow = config.fonts['title'].render("SOL MAZE", True, (100, 80, 0))
        config.screen.blit(title_shadow, (config.WIDTH // 2 - title_text.get_width() // 2 + 2, 122))
        config.screen.blit(title_text, (config.WIDTH // 2 - title_text.get_width() // 2, 120))
        
        subtitle = config.fonts['subtitle'].render("Solstice Duality", True, config.COLOR_TEXT)
        config.screen.blit(subtitle, (config.WIDTH // 2 - subtitle.get_width() // 2, 178))
  
        button_width = 200
        button_height = 50
        start_y = 235
        
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
            
        preview_y = start_y + len(options) * 65 + 30
        
        glow_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
        for radius in range(45, 30, -5):
            alpha = 80 - (45 - radius) * 10
            pygame.draw.circle(glow_surf, (255, 200, 50, max(0, alpha)), (50, 50), radius)
        config.screen.blit(glow_surf, (config.WIDTH // 2 - 50, preview_y))
        
        previewChar = draw_character(80, config.current_skin, 0)
        config.screen.blit(previewChar, (config.WIDTH // 2 - 40, preview_y + 5))
        
        skin_label = config.fonts['game_text'].render("Current Skin", True, (200, 200, 220))
        config.screen.blit(skin_label, (config.WIDTH // 2 - skin_label.get_width() // 2, preview_y + 85))
        
        instructions = config.fonts['instructions'].render("Use ↑ / ↓ to navigate | Enter to select", True, (180, 180, 200))
        config.screen.blit(instructions, (config.WIDTH // 2 - instructions.get_width() // 2, config.HEIGHT - 25))
        
        pygame.display.flip()
  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
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
                            if opt == "PLAY":
                                mode = await show_mode_selection_hud()
                                if mode in ["standard", "solstice_shift"] or mode.startswith("calendar_"):
                                    await screen_transition()
                                    await play_game(mode)
                                    await screen_transition()
                            elif opt.startswith("SKIN:"):
                                skin_selected = (skin_selected + 1) % len(skins)
                                config.current_skin = skins[skin_selected]
                                options[1] = "SKIN: " + get_skin_name(config.current_skin)
                            elif opt == "SETTINGS":
                                await show_settings_menu()
                            elif opt == "QUIT":
                                pygame.quit()
                                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    config.toggle_fullscreen()
                elif event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "PLAY":
                        mode = await show_mode_selection_hud()
                        if mode in ["standard", "solstice_shift"] or mode.startswith("calendar_"):
                            await screen_transition()
                            await play_game(mode)
                            await screen_transition()
                    elif options[selected].startswith("SKIN:"):
                        skin_selected = (skin_selected + 1) % len(skins)
                        config.current_skin = skins[skin_selected]
                        options[1] = "SKIN: " + get_skin_name(config.current_skin)
                    elif options[selected] == "SETTINGS":
                        await show_settings_menu()
                    elif options[selected] == "QUIT":
                        pygame.quit()
                        return
        config.clock.tick(config.FPS)
        await asyncio.sleep(0)
