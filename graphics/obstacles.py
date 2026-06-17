import pygame
import math
import random

def draw_sun_stone(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size//2, size//2
    r = size//2 - 4
    
    # Outer glow
    for glow_r in range(r+4, r-2, -1):
        alpha = max(0, 100 - (glow_r - r) * 20)
        glow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255,180,50, alpha), (cx,cy), glow_r)
        surf.blit(glow_surf, (0,0))
        
    # Gem coordinates
    top = (cx, cy - r)
    bottom = (cx, cy + r)
    left = (cx - r*0.8, cy - r*0.2)
    right = (cx + r*0.8, cy - r*0.2)
    center = (cx, cy + r*0.1) # Slightly shifted down for perspective
    
    # Facets
    pygame.draw.polygon(surf, (255, 240, 150), [top, left, center]) # Left Top
    pygame.draw.polygon(surf, (255, 210, 80), [top, right, center]) # Right Top
    pygame.draw.polygon(surf, (240, 160, 30), [left, bottom, center]) # Left Bottom
    pygame.draw.polygon(surf, (200, 110, 10), [right, bottom, center]) # Right Bottom
    
    # Edges
    pygame.draw.polygon(surf, (255, 255, 200), [top, right, bottom, left], 1)
    pygame.draw.line(surf, (255, 255, 200), top, center, 1)
    pygame.draw.line(surf, (255, 255, 200), left, center, 1)
    pygame.draw.line(surf, (255, 255, 200), right, center, 1)
    pygame.draw.line(surf, (255, 255, 200), bottom, center, 1)
    
    return surf

def draw_moon_stone(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size//2, size//2
    r = size//2 - 4
    
    # Outer halo
    for glow_r in range(r+4, r-2, -1):
        alpha = max(0, 100 - (glow_r - r) * 20)
        glow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (100,80,255, alpha), (cx,cy), glow_r)
        surf.blit(glow_surf, (0,0))
        
    # Gem coordinates (elongated hex shape)
    top = (cx, cy - r)
    bottom = (cx, cy + r)
    left_top = (cx - r*0.6, cy - r*0.4)
    right_top = (cx + r*0.6, cy - r*0.4)
    left_bot = (cx - r*0.5, cy + r*0.4)
    right_bot = (cx + r*0.5, cy + r*0.4)
    center = (cx, cy)
    
    # Facets
    pygame.draw.polygon(surf, (180, 230, 255), [top, left_top, center])
    pygame.draw.polygon(surf, (140, 200, 255), [top, right_top, center])
    pygame.draw.polygon(surf, (100, 150, 230), [left_top, left_bot, center])
    pygame.draw.polygon(surf, (80, 110, 200), [right_top, right_bot, center])
    pygame.draw.polygon(surf, (60, 80, 160), [left_bot, bottom, center])
    pygame.draw.polygon(surf, (40, 50, 130), [right_bot, bottom, center])
    
    # Edges
    outline = [top, right_top, right_bot, bottom, left_bot, left_top]
    pygame.draw.polygon(surf, (200, 240, 255), outline, 1)
    for pt in outline:
        pygame.draw.line(surf, (200, 240, 255), center, pt, 1)
        
    return surf

def draw_prism(size, color_name):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size//2, size//2
    r = size//2 - 4
    
    color_map = {
        "red": (255, 50, 50),
        "orange": (255, 150, 0),
        "yellow": (255, 230, 0),
        "green": (50, 255, 50),
        "blue": (50, 150, 255),
        "purple": (200, 50, 255)
    }
    base_color = color_map.get(color_name, (255, 255, 255))
    
    # Glow
    for glow_r in range(r+4, r-2, -1):
        alpha = max(0, 80 - (glow_r - r) * 15)
        glow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*base_color, alpha), (cx, cy), glow_r)
        surf.blit(glow_surf, (0, 0))
        
    # Shape: Diamond
    top = (cx, cy - r)
    bottom = (cx, cy + r)
    left = (cx - r*0.7, cy)
    right = (cx + r*0.7, cy)
    center = (cx, cy)
    
    # Highlight color
    hl_color = (min(255, base_color[0]+100), min(255, base_color[1]+100), min(255, base_color[2]+100))
    # Shadow color
    sh_color = (max(0, base_color[0]-100), max(0, base_color[1]-100), max(0, base_color[2]-100))
    
    pygame.draw.polygon(surf, hl_color, [top, left, center])
    pygame.draw.polygon(surf, base_color, [top, right, center])
    pygame.draw.polygon(surf, base_color, [left, bottom, center])
    pygame.draw.polygon(surf, sh_color, [right, bottom, center])
    
    pygame.draw.polygon(surf, (255, 255, 255), [top, right, bottom, left], 1)
    return surf

def draw_rainbow_bridge(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size//2, size//2
    colors = [(228,3,3),(255,140,0),(255,237,0),(0,128,38),(36,64,142),(115,41,130)]
    
    # Outer glow
    pygame.draw.circle(surf, (255, 255, 255, 50), (cx, cy), size//2)
    pygame.draw.circle(surf, (255, 255, 255, 100), (cx, cy), size//2 - 5)
    
    # Rainbow bands
    r_outer = size//2 - 2
    r_inner = size//4
    band_width = (r_outer - r_inner) / len(colors)
    
    for i, col in enumerate(colors):
        r = r_outer - i * band_width
        pygame.draw.circle(surf, col, (cx, cy), int(r))
        
    # Hollow center
    pygame.draw.circle(surf, (0, 0, 0, 0), (cx, cy), int(r_inner))
    
    # Add star sparkles
    for _ in range(5):
        sx = random.randint(0, size)
        sy = random.randint(0, size)
        pygame.draw.circle(surf, (255, 255, 255), (sx, sy), 1)
        
    return surf

def draw_gate(size, color_name):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    
    color_map = {
        "red": (255, 50, 50),
        "orange": (255, 150, 0),
        "yellow": (255, 230, 0),
        "green": (50, 255, 50),
        "blue": (50, 150, 255)
    }
    base_color = color_map.get(color_name, (255, 255, 255))
    
    # Background fill
    margin = 4
    pygame.draw.rect(surf, (*base_color, 80), (margin, margin, size-2*margin, size-2*margin))
    
    # Vertical laser beams
    for x in range(margin + 6, size - margin, 12):
        pygame.draw.line(surf, base_color, (x, margin), (x, size-margin), 2)
        pygame.draw.line(surf, (255, 255, 255), (x, margin), (x, size-margin), 1)
        
    # Glowing Border
    pygame.draw.rect(surf, base_color, (margin, margin, size-2*margin, size-2*margin), 3)
    pygame.draw.rect(surf, (255, 255, 255, 150), (margin, margin, size-2*margin, size-2*margin), 1)
    
    return surf

def draw_trash(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    # Draw a crumpled trash bag
    pygame.draw.circle(surf, (60, 60, 60), (cx, cy + size//8), size//3)
    pygame.draw.polygon(surf, (60, 60, 60), [(cx - size//4, cy), (cx + size//4, cy), (cx, cy - size//3)])
    # Tie string
    pygame.draw.line(surf, (200, 50, 50), (cx - 8, cy - size//4 + 2), (cx + 8, cy - size//4 + 2), 2)
    # Highlights
    pygame.draw.arc(surf, (100, 100, 105), (cx - size//4, cy, size//2, size//2), 3.14/2, 3.14, 2)
    return surf

def draw_tree_of_life(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    # Trunk
    pygame.draw.polygon(surf, (101, 67, 33), [
        (cx - size//10, cy + size//2),
        (cx + size//10, cy + size//2),
        (cx + size//12, cy - size//6),
        (cx - size//12, cy - size//6)
    ])
    # Canopy (overlapping circles forming a fluffy cloud-like shape)
    pygame.draw.circle(surf, (34, 139, 34), (cx, cy - size//4), size//3)
    pygame.draw.circle(surf, (40, 160, 40), (cx - size//6, cy - size//3), size//4)
    pygame.draw.circle(surf, (40, 160, 40), (cx + size//6, cy - size//3), size//4)
    pygame.draw.circle(surf, (50, 205, 50), (cx, cy - size//2 + 5), size//4)
    pygame.draw.circle(surf, (34, 139, 34), (cx - size//4, cy - size//6), size//5)
    pygame.draw.circle(surf, (34, 139, 34), (cx + size//4, cy - size//6), size//5)
    
    # Glow
    pygame.draw.circle(surf, (200, 255, 200, 80), (cx, cy), size//2 - 2, 3)
    return surf

def draw_boat(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    # Boat Hull
    pygame.draw.polygon(surf, (139, 69, 19), [
        (cx - size//3, cy),
        (cx + size//3, cy),
        (cx + size//4, cy + size//4),
        (cx - size//4, cy + size//4)
    ])
    # Mast
    pygame.draw.line(surf, (101, 67, 33), (cx, cy), (cx, cy - size//2), 3)
    # Sail
    pygame.draw.polygon(surf, (240, 240, 240), [
        (cx, cy - size//2),
        (cx, cy - size//6),
        (cx + size//3, cy - size//4)
    ])
    return surf

def draw_coral_reef(size, is_high_tide):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    # Base color depending on tide
    alpha = 100 if is_high_tide else 255
    color = (255, 120, 100, alpha)
    
    # Simple cluster of circles
    pygame.draw.circle(surf, color, (cx, cy), size//3)
    pygame.draw.circle(surf, (255, 150, 100, alpha), (cx - size//6, cy + size//6), size//4)
    pygame.draw.circle(surf, (255, 150, 100, alpha), (cx + size//6, cy - size//6), size//4)
    
    return surf

def draw_trench(size, is_high_tide):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    if is_high_tide:
        # Simple dark swirling water
        pygame.draw.circle(surf, (0, 20, 60, 220), (cx, cy), size//2 - 4)
        pygame.draw.arc(surf, (100, 200, 255, 150), (cx - size//3, cy - size//3, size//1.5, size//1.5), 0, 3.14, 2)
    else:
        # Calm, just deep water
        pygame.draw.circle(surf, (0, 40, 90, 150), (cx, cy), size//2 - 4)
        
    return surf

def draw_turtle(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    # Shell
    pygame.draw.ellipse(surf, (0, 100, 0), (cx - size//3, cy - size//4, size//1.5, size//2))
    pygame.draw.ellipse(surf, (34, 139, 34), (cx - size//4, cy - size//5, size//2, size//2.5))
    # Head
    pygame.draw.circle(surf, (0, 128, 0), (cx + size//3, cy), size//6)
    # Flippers
    pygame.draw.ellipse(surf, (0, 128, 0), (cx - size//4, cy - size//2, size//6, size//3))
    pygame.draw.ellipse(surf, (0, 128, 0), (cx + size//4, cy - size//2, size//6, size//3))
    pygame.draw.ellipse(surf, (0, 128, 0), (cx - size//4, cy + size//6, size//6, size//3))
    pygame.draw.ellipse(surf, (0, 128, 0), (cx + size//4, cy + size//6, size//6, size//3))
    return surf

def draw_whirlpool(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    # Draw spirals
    for radius in range(size//2, 5, -5):
        rect = pygame.Rect(cx - radius, cy - radius, radius*2, radius*2)
        pygame.draw.arc(surf, (100, 200, 255), rect, 0, 3.14, 3)
        pygame.draw.arc(surf, (50, 150, 255), rect, 3.14, 6.28, 3)
    return surf

def draw_pillar(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    margin = 4
    rect = pygame.Rect(margin, margin, size-2*margin, size-2*margin)
    pygame.draw.rect(surf, (90,77,65), rect)
    pygame.draw.rect(surf, (120,105,90), rect, 2)
    inner = rect.inflate(-8, -8)
    pygame.draw.rect(surf, (50,40,35), inner)
    pygame.draw.line(surf, (150,130,110), (rect.x+4, rect.y+2), (rect.x+rect.width-4, rect.y+2), 2)
    return surf

def draw_freedom_bell(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    # Outer glow
    pygame.draw.circle(surf, (255, 215, 0, 100), (cx, cy), size//2 - 2)
    
    # Bell Shape (Bronze/Gold)
    pygame.draw.polygon(surf, (218, 165, 32), [
        (cx - size//6, cy - size//4),
        (cx + size//6, cy - size//4),
        (cx + size//4, cy + size//4),
        (cx - size//4, cy + size//4)
    ])
    
    # Top curved part
    pygame.draw.ellipse(surf, (218, 165, 32), (cx - size//6, cy - size//4 - size//10, size//3, size//5))
    
    # Bottom curved part
    pygame.draw.ellipse(surf, (218, 165, 32), (cx - size//4, cy + size//4 - size//10, size//2, size//5))
    
    # Clapper
    pygame.draw.circle(surf, (184, 134, 11), (cx, cy + size//4 + size//12), size//10)
    
    # Liberty Crack
    pygame.draw.lines(surf, (100, 70, 10), False, [
        (cx - size//10, cy + size//4),
        (cx - size//16, cy + size//8),
        (cx, cy - size//16)
    ], 2)
    
    return surf

def draw_freedom_star(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    # Glowing aura
    pygame.draw.circle(surf, (255, 255, 100, 80), (cx, cy), size//2 - 4)
    
    # 5-pointed star
    points = []
    outer_r = size // 3
    inner_r = size // 6
    for i in range(10):
        angle = math.radians(i * 36 - 90)
        r = outer_r if i % 2 == 0 else inner_r
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
        
    pygame.draw.polygon(surf, (255, 230, 50), points)
    pygame.draw.polygon(surf, (255, 255, 200), points, 2)
    
    # Shine line
    pygame.draw.line(surf, (255, 255, 255), (cx, cy - outer_r), (cx, cy + outer_r), 1)
    
    return surf

def draw_shadow_wall(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Dense dark block
    pygame.draw.rect(surf, (10, 10, 15, 240), (0, 0, size, size))
    
    # Swirling mist effect
    for _ in range(5):
        cx = random.randint(size//4, size*3//4)
        cy = random.randint(size//4, size*3//4)
        r = random.randint(size//8, size//4)
        pygame.draw.circle(surf, (30, 30, 40, 150), (cx, cy), r)
        
    # jagged sharp obsidian edges
    for i in range(0, size, 10):
        pygame.draw.line(surf, (5, 5, 10), (i, 0), (i + 5, 10), 2)
        pygame.draw.line(surf, (5, 5, 10), (0, i), (10, i + 5), 2)
        
    return surf

def draw_grill(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    # Legs (silver-gray lines)
    pygame.draw.line(surf, (150, 150, 150), (cx, cy + size//8), (cx - size//4, cy + size//2.5), 3)
    pygame.draw.line(surf, (150, 150, 150), (cx, cy + size//8), (cx + size//4, cy + size//2.5), 3)
    pygame.draw.line(surf, (150, 150, 150), (cx, cy + size//8), (cx, cy + size//2.3), 3)
    
    # Triangle brace
    pygame.draw.line(surf, (120, 120, 120), (cx - size//6, cy + size//3), (cx + size//6, cy + size//3), 2)
    
    # Wheels
    pygame.draw.circle(surf, (30, 30, 30), (cx - size//4, cy + size//2.5), 4)
    pygame.draw.circle(surf, (30, 30, 30), (cx + size//4, cy + size//2.5), 4)
    
    # Bowl
    bowl_pts = []
    for angle_deg in range(0, 181, 10):
        angle_rad = math.radians(angle_deg)
        rx = size // 3
        ry = size // 4
        bowl_pts.append((cx + rx * math.cos(angle_rad), cy + ry * math.sin(angle_rad)))
    pygame.draw.polygon(surf, (40, 40, 40), bowl_pts)
    pygame.draw.polygon(surf, (10, 10, 10), bowl_pts, 2)
    
    # Glow / Hot Coals
    pygame.draw.ellipse(surf, (100, 10, 10), (cx - size//3.2, cy - size//12, size//1.6, size//6))
    for _ in range(8):
        offset_x = random.randint(-size//4, size//4)
        offset_y = random.randint(-size//16, size//16)
        r = random.randint(2, 4)
        pygame.draw.circle(surf, random.choice([(255, 69, 0), (255, 140, 0), (255, 50, 50)]), (cx + offset_x, cy + offset_y), r)
        
    # Grate bar
    pygame.draw.line(surf, (200, 200, 200), (cx - size//3, cy), (cx + size//3, cy), 2)
    pygame.draw.line(surf, (160, 160, 160), (cx - size//3.5, cy - 3), (cx + size//3.5, cy - 3), 1)
    
    # Handle
    pygame.draw.arc(surf, (150, 150, 150), (cx - size//3.5, cy + 2, size//1.8, size//4), math.pi, 2*math.pi, 2)
    
    return surf

def draw_tie_item(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    color_base = (200, 40, 40)
    color_stripe = (40, 60, 150)
    
    knot_pts = [(cx - 4, cy - size//2.5), (cx + 4, cy - size//2.5), (cx + 3, cy - size//4), (cx - 3, cy - size//4)]
    pygame.draw.polygon(surf, color_base, knot_pts)
    
    body_pts = [
        (cx - 3, cy - size//4),
        (cx + 3, cy - size//4),
        (cx + 6, cy + size//4),
        (cx, cy + size//2.2),
        (cx - 6, cy + size//4)
    ]
    pygame.draw.polygon(surf, color_base, body_pts)
    
    mask = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.polygon(mask, (255, 255, 255, 255), body_pts)
    pygame.draw.polygon(mask, (255, 255, 255, 255), knot_pts)
    
    stripes_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    for d in range(-size, size, 8):
        pygame.draw.line(stripes_surf, color_stripe, (cx - size, cy + d), (cx + size, cy + d + size), 3)
        
    stripes_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    surf.blit(stripes_surf, (0, 0))
    
    pygame.draw.polygon(surf, (120, 20, 20), body_pts, 1)
    pygame.draw.polygon(surf, (120, 20, 20), knot_pts, 1)
    
    return surf

def draw_mug(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    steam_color = (200, 200, 220, 150)
    for dx in [-4, 0, 4]:
        offset = math.sin(pygame.time.get_ticks() * 0.005 + dx) * 2
        pygame.draw.lines(surf, steam_color, False, [
            (cx + dx, cy - size//4),
            (cx + dx + offset, cy - size//3),
            (cx + dx - offset, cy - size//2.2)
        ], 1)
        
    mug_color = (30, 100, 200)
    pygame.draw.rect(surf, mug_color, (cx - size//4, cy - size//6, size//2, size//2.2), border_radius=4)
    pygame.draw.rect(surf, (20, 70, 160), (cx - size//4, cy - size//6, size//2, size//2.2), 2, border_radius=4)
    
    pygame.draw.arc(surf, mug_color, (cx - size//2.5, cy - size//8, size//4, size//3), math.pi/2, math.pi*1.5, 4)
    pygame.draw.arc(surf, (20, 70, 160), (cx - size//2.5, cy - size//8, size//4, size//3), math.pi/2, math.pi*1.5, 1)
    
    pygame.draw.circle(surf, (255, 215, 0), (cx, cy + 2), size//8)
    pygame.draw.circle(surf, (255, 255, 200), (cx, cy + 2), size//8, 1)
    
    pygame.draw.line(surf, (150, 100, 10), (cx - 2, cy + 4), (cx - 2, cy - 1), 2)
    pygame.draw.line(surf, (150, 100, 10), (cx + 2, cy + 4), (cx + 2, cy - 2), 2)
    
    return surf

def draw_coffee_cup(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    pygame.draw.line(surf, (200, 200, 200, 100), (cx, cy - 2), (cx - 2, cy - 8), 1)
    pygame.draw.line(surf, (200, 200, 200, 100), (cx + 3, cy - 2), (cx + 1, cy - 8), 1)
    
    pygame.draw.ellipse(surf, (240, 240, 245), (cx - size//6, cy - size//12, size//3, size//5))
    pygame.draw.ellipse(surf, (180, 180, 190), (cx - size//6, cy - size//12, size//3, size//5), 1)
    
    pygame.draw.ellipse(surf, (220, 220, 225), (cx - size//4, cy + size//16, size//2, size//10))
    pygame.draw.ellipse(surf, (170, 170, 180), (cx - size//4, cy + size//16, size//2, size//10), 1)
    
    pygame.draw.arc(surf, (240, 240, 245), (cx + size//8, cy - size//16, size//8, size//8), -math.pi/2, math.pi/2, 2)
    
    return surf

def draw_lawn_chair(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    frame_color = (200, 200, 210)
    pygame.draw.line(surf, frame_color, (cx - size//4, cy - size//3), (cx - size//4, cy + size//4), 3)
    pygame.draw.line(surf, frame_color, (cx + size//4, cy - size//3), (cx + size//4, cy + size//4), 3)
    pygame.draw.line(surf, frame_color, (cx - size//4, cy + size//4), (cx + size//4, cy + size//4), 3)
    pygame.draw.line(surf, frame_color, (cx - size//4, cy - size//3), (cx + size//4, cy - size//3), 3)
    
    pygame.draw.line(surf, frame_color, (cx - size//4, cy + size//4), (cx - size//5, cy + size//2.3), 3)
    pygame.draw.line(surf, frame_color, (cx + size//4, cy + size//4), (cx + size//5, cy + size//2.3), 3)
    pygame.draw.line(surf, frame_color, (cx - size//5, cy + size//2.3), (cx + size//5, cy + size//2.3), 3)
    
    web_g = (46, 139, 87)
    web_w = (245, 245, 245)
    
    web_y_start = cy - size//3 + 4
    web_y_end = cy + size//4 - 2
    step_y = (web_y_end - web_y_start) // 5
    for i in range(5):
        wy = web_y_start + i * step_y
        color = web_g if i % 2 == 0 else web_w
        pygame.draw.rect(surf, color, (cx - size//4 + 2, wy, size//2 - 4, step_y - 1))
        
    step_x = (size//2 - 4) // 4
    for i in range(4):
        wx = cx - size//4 + 2 + i * step_x
        for j in range(5):
            if (i + j) % 2 == 0:
                color = web_g if (i + j) % 4 == 0 else web_w
                pygame.draw.rect(surf, color, (wx, web_y_start + j * step_y, step_x - 1, step_y))
                
    pygame.draw.line(surf, (50, 50, 55), (cx - size//4 - 3, cy - size//10), (cx - size//4 + 2, cy + size//10), 4)
    pygame.draw.line(surf, (50, 50, 55), (cx + size//4 - 2, cy - size//10), (cx + size//4 + 3, cy + size//10), 4)
    
    glow = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(glow, (255, 255, 150, 60), (cx, cy), size//2)
    surf.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    
    return surf

def draw_lawn_gnome(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    pygame.draw.polygon(surf, (240, 240, 245), [
        (cx - 6, cy + 2), (cx + 6, cy + 2),
        (cx + 4, cy + size//4), (cx, cy + size//3), (cx - 4, cy + size//4)
    ])
    
    pygame.draw.circle(surf, (250, 210, 180), (cx, cy), size//6)
    pygame.draw.circle(surf, (255, 170, 150), (cx, cy + 1), size//12)
    
    pygame.draw.polygon(surf, (220, 30, 30), [
        (cx - size//5, cy - size//12),
        (cx + size//5, cy - size//12),
        (cx - 2, cy - size//2.2)
    ])
    pygame.draw.line(surf, (240, 40, 40), (cx - size//5, cy - size//12), (cx + size//5, cy - size//12), 2)
    
    pygame.draw.rect(surf, (30, 80, 180), (cx - size//5, cy + size//5, size//2.5, size//4), border_radius=3)
    pygame.draw.line(surf, (10, 10, 10), (cx - size//5, cy + size//3 + 2), (cx + size//5, cy + size//3 + 2), 2)
    pygame.draw.rect(surf, (255, 215, 0), (cx - 2, cy + size//3 + 1, 4, 3))
    
    pygame.draw.circle(surf, (30, 30, 30), (cx - 3, cy - 2), 1)
    pygame.draw.circle(surf, (30, 30, 30), (cx + 3, cy - 2), 1)
    
    return surf

def draw_lawn_bush(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    pygame.draw.circle(surf, (20, 70, 30), (cx, cy), size//2.2)
    pygame.draw.circle(surf, (34, 139, 34), (cx - 4, cy - 4), size//3)
    pygame.draw.circle(surf, (46, 139, 87), (cx + 6, cy - 2), size//3.2)
    pygame.draw.circle(surf, (50, 205, 50), (cx - 2, cy + 6), size//3.5)
    pygame.draw.circle(surf, (124, 252, 0), (cx + 3, cy + 2), size//4.5)
    
    flower_positions = [
        (cx - 8, cy - 6), (cx + 8, cy - 4),
        (cx - 2, cy + 8), (cx + 6, cy + 6),
        (cx - 6, cy + 2), (cx + 2, cy - 8)
    ]
    for fx, fy in flower_positions:
        pygame.draw.circle(surf, (255, 105, 180), (fx, fy), 2)
        pygame.draw.circle(surf, (255, 255, 255), (fx, fy), 1)
        
    return surf

def draw_garden_hose(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    hose_green = (34, 177, 76)
    pygame.draw.ellipse(surf, hose_green, (cx - size//2.5, cy - size//3.5, size//1.25, size//1.75), 3)
    pygame.draw.ellipse(surf, (20, 120, 50), (cx - size//2.5, cy - size//3.5, size//1.25, size//1.75), 1)
    
    pygame.draw.ellipse(surf, hose_green, (cx - size//3.2, cy - size//4.5, size//1.6, size//2.25), 3)
    pygame.draw.ellipse(surf, (20, 120, 50), (cx - size//3.2, cy - size//4.5, size//1.6, size//2.25), 1)
    
    pygame.draw.ellipse(surf, hose_green, (cx - size//4.5, cy - size//6, size//2.25, size//3), 3)
    pygame.draw.ellipse(surf, (20, 120, 50), (cx - size//4.5, cy - size//6, size//2.25, size//3), 1)
    
    pygame.draw.line(surf, hose_green, (cx - size//3, cy - size//4), (cx + size//3, cy + size//3), 3)
    pygame.draw.line(surf, (20, 120, 50), (cx - size//3, cy - size//4), (cx + size//3, cy + size//3), 1)
    
    pygame.draw.rect(surf, (30, 30, 30), (cx + size//3 - 3, cy + size//3 - 3, 5, 5))
    
    nozzle_pts = [
        (cx + size//3 - 1, cy + size//3 + 1),
        (cx + size//3 + 5, cy + size//3 + 7),
        (cx + size//3 + 8, cy + size//3 + 4),
        (cx + size//3 + 2, cy + size//3 - 2)
    ]
    pygame.draw.polygon(surf, (255, 215, 0), nozzle_pts)
    pygame.draw.polygon(surf, (180, 140, 10), nozzle_pts, 1)
    
    return surf

def draw_musical_note(size, color):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    # Glow around the note
    for r in range(size // 3 + 4, size // 3 - 2, -2):
        alpha = max(0, 80 - (r - (size // 3)) * 15)
        glow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (*color, alpha), (cx, cy), r)
        surf.blit(glow_surf, (0, 0))

    # Note head (slanted ellipse)
    head_w, head_h = int(size * 0.28), int(size * 0.2)
    head_x = cx - head_w // 2 - int(size * 0.05)
    head_y = cy + int(size * 0.15) - head_h // 2
    
    pygame.draw.ellipse(surf, color, (head_x, head_y, head_w, head_h))
    pygame.draw.ellipse(surf, (255, 255, 255), (head_x, head_y, head_w, head_h), 1)

    # Stem
    stem_x = head_x + head_w - 2
    stem_y_top = cy - int(size * 0.25)
    stem_y_bottom = head_y + head_h // 2
    pygame.draw.line(surf, color, (stem_x, stem_y_top), (stem_x, stem_y_bottom), 3)
    pygame.draw.line(surf, (255, 255, 255), (stem_x + 1, stem_y_top), (stem_x + 1, stem_y_bottom - 2), 1)

    # Flag
    flag_pts = [
        (stem_x, stem_y_top),
        (stem_x + int(size * 0.2), stem_y_top + int(size * 0.1)),
        (stem_x + int(size * 0.15), stem_y_top + int(size * 0.25)),
        (stem_x, stem_y_top + int(size * 0.15))
    ]
    pygame.draw.polygon(surf, color, flag_pts)
    pygame.draw.polygon(surf, (255, 255, 255), flag_pts, 1)

    return surf

def draw_speaker_obstacle(size, is_pulsing=False):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    margin = 3
    
    # Speaker cabinet (black/dark-gray box)
    rect = pygame.Rect(margin, margin, size - 2*margin, size - 2*margin)
    pygame.draw.rect(surf, (30, 30, 35), rect, border_radius=4)
    pygame.draw.rect(surf, (10, 10, 12), rect, 3, border_radius=4)
    
    # Inner grille background
    grille_rect = rect.inflate(-6, -6)
    pygame.draw.rect(surf, (15, 15, 18), grille_rect, border_radius=2)
    
    # Subtly draw grill lines
    for y in range(grille_rect.top + 2, grille_rect.bottom, 4):
        pygame.draw.line(surf, (25, 25, 30), (grille_rect.left, y), (grille_rect.right, y), 1)

    # Tweeter (small top circle)
    tweeter_y = grille_rect.top + int(grille_rect.height * 0.28)
    pygame.draw.circle(surf, (50, 50, 55), (cx, tweeter_y), int(size * 0.12))
    pygame.draw.circle(surf, (160, 160, 170), (cx, tweeter_y), int(size * 0.06))
    
    # Woofer (large bottom circle)
    woofer_y = grille_rect.top + int(grille_rect.height * 0.7)
    base_woofer_r = int(size * 0.22)
    
    # Pulsing animation if is_pulsing is True
    pulse = 0
    if is_pulsing:
        pulse = math.sin(pygame.time.get_ticks() * 0.015) * 2
        
    woofer_r = max(4, int(base_woofer_r + pulse))
    pygame.draw.circle(surf, (40, 40, 45), (cx, woofer_y), base_woofer_r)
    pygame.draw.circle(surf, (80, 80, 90), (cx, woofer_y), woofer_r, 2)
    pygame.draw.circle(surf, (200, 50, 50) if is_pulsing else (100, 100, 110), (cx, woofer_y), max(2, int(woofer_r * 0.4)))
    
    # Protective corner caps
    corner_size = 4
    for px, py in [(rect.left, rect.top), (rect.right - corner_size, rect.top),
                  (rect.left, rect.bottom - corner_size), (rect.right - corner_size, rect.bottom - corner_size)]:
        pygame.draw.rect(surf, (60, 60, 65), (px, py, corner_size, corner_size), border_radius=1)
        
    return surf

def draw_drum_obstacle(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    # Bass/Snare drum cylinder
    drum_w = int(size * 0.75)
    drum_h = int(size * 0.5)
    drum_x = cx - drum_w // 2
    drum_y = cy - drum_h // 2 + 3
    
    # Drum shell (deep red/burgundy cylinder)
    shell_color = (150, 20, 30)
    pygame.draw.rect(surf, shell_color, (drum_x, drum_y, drum_w, drum_h), border_radius=2)
    pygame.draw.rect(surf, (100, 10, 15), (drum_x, drum_y, drum_w // 3, drum_h), border_radius=2)
    
    # Drum heads
    top_rect = (drum_x, drum_y - int(drum_h * 0.15), drum_w, int(drum_h * 0.3))
    pygame.draw.ellipse(surf, (240, 240, 230), top_rect)
    pygame.draw.ellipse(surf, (200, 200, 190), top_rect, 2)
    
    bot_rect = (drum_x, drum_y + drum_h - int(drum_h * 0.15), drum_w, int(drum_h * 0.3))
    pygame.draw.ellipse(surf, (180, 180, 180), bot_rect)
    pygame.draw.ellipse(surf, (200, 200, 190), bot_rect, 2)
    
    # Tension rods
    for offset in range(10, drum_w, drum_w // 4):
        rx = drum_x + offset
        pygame.draw.line(surf, (220, 220, 230), (rx, drum_y + 2), (rx, drum_y + drum_h - 2), 2)
        pygame.draw.rect(surf, (160, 160, 170), (rx - 2, drum_y + 4, 4, 4))
        pygame.draw.rect(surf, (160, 160, 170), (rx - 2, drum_y + drum_h - 8, 4, 4))

    # Drumsticks
    stick_color = (222, 184, 135)
    pygame.draw.line(surf, stick_color, (cx - int(size * 0.3), cy - int(size * 0.25)), (cx + int(size * 0.25), cy + int(size * 0.05)), 2)
    pygame.draw.line(surf, stick_color, (cx + int(size * 0.3), cy - int(size * 0.25)), (cx - int(size * 0.25), cy + int(size * 0.05)), 2)
    pygame.draw.circle(surf, stick_color, (cx + int(size * 0.25), cy + int(size * 0.05)), 3)
    pygame.draw.circle(surf, stick_color, (cx - int(size * 0.25), cy + int(size * 0.05)), 3)
    
    return surf

def draw_mic_obstacle(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    # Mic stand base
    base_w = int(size * 0.4)
    base_h = int(size * 0.1)
    pygame.draw.ellipse(surf, (80, 80, 85), (cx - base_w//2, cy + int(size*0.35), base_w, base_h))
    pygame.draw.ellipse(surf, (40, 40, 45), (cx - base_w//2, cy + int(size*0.35), base_w, base_h), 2)
    
    # Vertical shaft
    shaft_x = cx
    shaft_top_y = cy - int(size * 0.25)
    shaft_bot_y = cy + int(size * 0.35)
    pygame.draw.line(surf, (180, 180, 190), (shaft_x, shaft_top_y), (shaft_x, shaft_bot_y), 3)
    pygame.draw.line(surf, (100, 100, 105), (shaft_x + 1, shaft_top_y), (shaft_x + 1, shaft_bot_y), 1)
    
    # Clutch
    pygame.draw.rect(surf, (40, 40, 40), (cx - 3, cy, 6, 8), border_radius=1)
    
    # Mic clip
    clip_pts = [
        (cx, shaft_top_y),
        (cx - int(size * 0.1), shaft_top_y - int(size * 0.08)),
        (cx - int(size * 0.08), shaft_top_y - int(size * 0.15)),
        (cx + int(size * 0.02), shaft_top_y - int(size * 0.07))
    ]
    pygame.draw.polygon(surf, (30, 30, 30), clip_pts)
    
    # Microphone
    mic_angle = math.radians(30)
    mic_len = int(size * 0.28)
    mic_w = int(size * 0.08)
    start_x = cx + int(size * 0.05)
    start_y = shaft_top_y - int(size * 0.03)
    end_x = start_x - int(mic_len * math.cos(mic_angle))
    end_y = start_y - int(mic_len * math.sin(mic_angle))
    
    pygame.draw.line(surf, (50, 50, 55), (start_x, start_y), (end_x, end_y), mic_w)
    
    # Grille
    grille_x = end_x - int(size * 0.05 * math.cos(mic_angle))
    grille_y = end_y - int(size * 0.05 * math.sin(mic_angle))
    pygame.draw.circle(surf, (180, 180, 190), (grille_x, grille_y), int(size * 0.09))
    pygame.draw.circle(surf, (220, 220, 230), (grille_x, grille_y), int(size * 0.09), 1)
    pygame.draw.line(surf, (100, 100, 100), (grille_x - 3, grille_y + 3), (grille_x + 3, grille_y - 3), 1)
    pygame.draw.line(surf, (100, 100, 100), (grille_x - 3, grille_y - 3), (grille_x + 3, grille_y + 3), 1)
    
    return surf

def draw_treble_clef(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    
    # Gold glow
    for r in range(size//2 - 2, size//3, -2):
        alpha = max(0, 70 - (r - size//3) * 10)
        glow = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 215, 0, alpha), (cx, cy), r)
        surf.blit(glow, (0, 0))
        
    # Stem
    stem_x = cx + int(size * 0.05)
    stem_top_y = cy - int(size * 0.35)
    stem_bot_y = cy + int(size * 0.3)
    
    pygame.draw.line(surf, (255, 215, 0), (stem_x, stem_top_y), (stem_x, stem_bot_y), 3)
    pygame.draw.line(surf, (255, 255, 200), (stem_x + 1, stem_top_y), (stem_x + 1, stem_bot_y), 1)
    
    # Bottom curl & dot
    pygame.draw.arc(surf, (255, 215, 0), (stem_x - int(size*0.15), stem_bot_y - int(size*0.1), int(size*0.2), int(size*0.2)), 0.5 * math.pi, 2.0 * math.pi, 3)
    pygame.draw.circle(surf, (255, 215, 0), (stem_x - int(size*0.15), stem_bot_y), int(size*0.07))
    pygame.draw.circle(surf, (255, 255, 255), (stem_x - int(size*0.15), stem_bot_y), int(size*0.04))
    
    # Top loop
    top_loop_r = pygame.Rect(stem_x - int(size*0.08), stem_top_y, int(size*0.22), int(size*0.3))
    pygame.draw.arc(surf, (255, 215, 0), top_loop_r, -0.5 * math.pi, 1.0 * math.pi, 3)
    
    # Middle/Bottom loop
    mid_loop_r = pygame.Rect(stem_x - int(size*0.25), cy - int(size*0.1), int(size*0.35), int(size*0.35))
    pygame.draw.arc(surf, (255, 215, 0), mid_loop_r, 0.5 * math.pi, 2.0 * math.pi, 3)
    
    pygame.draw.line(surf, (255, 215, 0), (stem_x - 6, cy + 5), (stem_x + 8, cy - 5), 3)
    pygame.draw.circle(surf, (255, 215, 0), (stem_x - int(size*0.08), stem_top_y + int(size*0.15)), 2)
    
    return surf
