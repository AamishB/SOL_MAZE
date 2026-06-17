import pygame
import sys
import os

CELL_SIZE = 55
HUD_HEIGHT = 100
GRID_SIZE = 10
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE + HUD_HEIGHT
FPS = 60

COLOR_MENU_BG = (15, 20, 35)
COLOR_TEXT = (245, 246, 250)
COLOR_BUTTON = (255, 180, 50)

is_fullscreen = False

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sol Maze - Solstice Duality")
clock = pygame.time.Clock()

# Mutable settings & globals
current_skin = "solstice"
animation_frame = 0
has_seen_help = False
settings_god_rays = True
settings_music = True
settings_sfx = True
settings_particles = True

def setup_fonts():
    fonts = {}
    # Bundled fonts: Orbitron (sci-fi title), Outfit (clean sans-serif body)
    font_configs = {
        'title':        {'file': 'fonts/Orbitron.ttf',       'size': 44},
        'subtitle':     {'file': 'fonts/Outfit-SemiBold.ttf','size': 18},
        'button':       {'file': 'fonts/Outfit-Bold.ttf',    'size': 22},
        'mode_button':  {'file': 'fonts/Outfit-Bold.ttf',    'size': 17},
        'hud_title':    {'file': 'fonts/Outfit-Bold.ttf',    'size': 20},
        'hud_text':     {'file': 'fonts/Outfit-SemiBold.ttf','size': 18},
        'hud_numbers':  {'file': 'fonts/Outfit-Bold.ttf',    'size': 20},
        'game_text':    {'file': 'fonts/Outfit-SemiBold.ttf','size': 18},
        'game_large':   {'file': 'fonts/Outfit-Bold.ttf',    'size': 24},
        'instructions': {'file': 'fonts/Outfit-SemiBold.ttf','size': 14}
    }
    for key, cfg in font_configs.items():
        try:
            fonts[key] = pygame.font.Font(cfg['file'], cfg['size'])
        except Exception:
            # Fallback: pygame's built-in default font (works everywhere incl. WASM)
            fonts[key] = pygame.font.Font(None, cfg['size'])
    return fonts

fonts = setup_fonts()
font = fonts['game_text']
font_large = fonts['game_large']

# Lazy loader references to avoid circular imports during setup
_menu_background = None
_finish_background = None

def load_background_image():
    from graphics import draw_sun_icon
    try:
        bg_image = pygame.image.load('assets/menu_bg.png')
        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
        return bg_image
    except Exception as e:
        bg_surface = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(20 * (1 - ratio) + 40 * ratio)
            g = int(15 * (1 - ratio) + 20 * ratio)
            b = int(50 * (1 - ratio) + 80 * ratio)
            pygame.draw.line(bg_surface, (r, g, b), (0, y), (WIDTH, y))
        
        sun_surf = draw_sun_icon(200)
        sun_surf.set_alpha(30)
        bg_surface.blit(sun_surf, (WIDTH//2 - 100, HEIGHT//2 - 100))
        return bg_surface

def load_finish_background():
    try:
        bg_image = pygame.image.load('assets/finish_bg.png')
        bg_image = pygame.transform.scale(bg_image, (WIDTH, HEIGHT))
        return bg_image
    except Exception as e:
        bg_surface = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(10 * (1 - ratio) + 20 * ratio)
            g = int(8 * (1 - ratio) + 15 * ratio)
            b = int(30 * (1 - ratio) + 50 * ratio)
            pygame.draw.line(bg_surface, (r, g, b), (0, y), (WIDTH, y))
        return bg_surface

def get_menu_background():
    global _menu_background
    if _menu_background is None:
        _menu_background = load_background_image()
    return _menu_background

def get_finish_background():
    global _finish_background
    if _finish_background is None:
        _finish_background = load_finish_background()
    return _finish_background

def toggle_fullscreen():
    global is_fullscreen
    try:
        is_fullscreen = not is_fullscreen
        pygame.display.toggle_fullscreen()
    except Exception:
        is_fullscreen = not is_fullscreen  # revert on failure (e.g. web)
