import pygame
import math
import random

def draw_gradient(surface, color1, color2, vertical=True):
    """Fill surface with a vertical or horizontal gradient."""
    width, height = surface.get_size()
    for y in range(height):
        ratio = y / height if vertical else 1.0
        r = int(color1[0] * (1-ratio) + color2[0] * ratio)
        g = int(color1[1] * (1-ratio) + color2[1] * ratio)
        b = int(color1[2] * (1-ratio) + color2[2] * ratio)
        pygame.draw.line(surface, (r,g,b), (0,y), (width,y))

def draw_starfield(surface, num_stars=150):
    """Draw random white dots for night background."""
    width, height = surface.get_size()
    for _ in range(num_stars):
        x = random.randint(0, width)
        y = random.randint(0, height)
        pygame.draw.circle(surface, (220,220,255), (x, y), 1)

def draw_god_rays(surface, angle_deg, intensity=30):
    width, height = surface.get_size()
    rad = math.radians(angle_deg)
    dx = math.cos(rad)
    dy = math.sin(rad)
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    for i in range(0, width+height, 20):
        if abs(dx) > 0.5:
            x = i
            y = 0
        else:
            x = 0
            y = i
        end_x = x + width * dx * 2
        end_y = y + height * dy * 2
        pygame.draw.line(overlay, (255,240,180), (x,y), (end_x,end_y), 6)
        overlay.set_alpha(intensity)
    surface.blit(overlay, (0,0), special_flags=pygame.BLEND_ADD)

def draw_celestial_medallion(size, angle_deg=0):
    """Draw a composite celestial medallion combining sun and moon features, rotating based on angle_deg."""
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size // 2, size // 2
    r_medallion = size // 3
    
    # Outer golden glow
    for glow_r in range(r_medallion + 8, r_medallion - 2, -2):
        alpha = max(0, min(100, 100 - (glow_r - r_medallion) * 10))
        glow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (218, 165, 32, alpha), (cx, cy), glow_r)
        surf.blit(glow_surf, (0, 0))
        
    # Main gold ring
    pygame.draw.circle(surf, (218, 165, 32), (cx, cy), r_medallion, 3)
    
    # Inner dark blue background
    pygame.draw.circle(surf, (15, 20, 35), (cx, cy), r_medallion - 3)
    
    # Radiating golden sun rays (rotated by angle_deg)
    rad_angle = math.radians(angle_deg)
    num_rays = 8
    for i in range(num_rays):
        a = rad_angle + i * (2 * math.pi / num_rays)
        # Main ray tip
        dx_tip = math.cos(a) * (r_medallion + 6)
        dy_tip = math.sin(a) * (r_medallion + 6)
        # Base of the ray (thick triangle)
        a_left = a - 0.15
        a_right = a + 0.15
        dx_l = math.cos(a_left) * (r_medallion - 4)
        dy_l = math.sin(a_left) * (r_medallion - 4)
        dx_r = math.cos(a_right) * (r_medallion - 4)
        dy_r = math.sin(a_right) * (r_medallion - 4)
        
        pygame.draw.polygon(surf, (255, 215, 0), [
            (cx + dx_tip, cy + dy_tip),
            (cx + dx_l, cy + dy_l),
            (cx + dx_r, cy + dy_r)
        ])
        
    # Inner crescent moon in silver overlaying a golden core
    inner_r = r_medallion - 8
    pygame.draw.circle(surf, (255, 200, 50), (cx, cy), inner_r) # Golden core
    
    # Crescent moon overlay (drawn in silver/light-blue on top of core)
    crescent_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(crescent_surf, (220, 225, 255), (cx, cy), inner_r)
    # Cut out half of the circle to make a crescent by subtracting alpha
    mask_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(mask_surf, (255, 255, 255, 255), (cx - 6, cy), inner_r)
    crescent_surf.blit(mask_surf, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
    surf.blit(crescent_surf, (0, 0))
    
    # Small silver stars in the corners/inside the ring
    for i in range(4):
        a = rad_angle + (i * 2 + 1) * (math.pi / 4)
        sx = cx + math.cos(a) * (r_medallion * 0.6)
        sy = cy + math.sin(a) * (r_medallion * 0.6)
        pygame.draw.circle(surf, (255, 255, 255), (int(sx), int(sy)), 2)
        
    return surf

def draw_character(size, skin="solstice", animation_offset=0):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx = size // 2
    cy = size // 2
    
    # Bobbing floating motion
    bob = math.sin(animation_offset) * 3
    
    cape_top_w = size * 0.25
    cape_bot_w = size * 0.6
    cape_h = size * 0.55
    
    top_y = cy - cape_h//2 + bob + size * 0.1
    bot_y = cy + cape_h//2 + bob + size * 0.1
    
    cape_points = [
        (cx - cape_top_w//2, top_y),
        (cx + cape_top_w//2, top_y),
        (cx + cape_bot_w//2, bot_y),
        (cx - cape_bot_w//2, bot_y)
    ]
    
    head_r = size * 0.22
    head_y = top_y - head_r * 0.5
    
    if skin == "solstice":
        # Golden Cape
        pygame.draw.polygon(surf, (240, 160, 40), cape_points)
        pygame.draw.polygon(surf, (255, 220, 100), cape_points, 2)
        # Cape trim
        pygame.draw.line(surf, (255, 220, 100), (cx - cape_bot_w//2, bot_y - 5), (cx + cape_bot_w//2, bot_y - 5), 2)
        
        # Floating Sun Orb Head
        pygame.draw.circle(surf, (255, 240, 150), (cx, head_y), head_r)
        pygame.draw.circle(surf, (255, 255, 255), (cx, head_y), head_r * 0.6)
        
        # Sun rays
        for i in range(8):
            angle = math.radians(i * 45 + animation_offset*50) 
            r_in = head_r + 2
            r_out = head_r + 6
            pygame.draw.line(surf, (255, 200, 50), 
                (cx + r_in*math.cos(angle), head_y + r_in*math.sin(angle)),
                (cx + r_out*math.cos(angle), head_y + r_out*math.sin(angle)), 2)

    elif skin == "pride":
        # Rainbow Cape
        colors = [(228,3,3),(255,140,0),(255,237,0),(0,128,38),(36,64,142),(115,41,130)]
        # Draw cape mask
        cape_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(cape_surf, (255,255,255,255), cape_points)
        
        # Color surf
        color_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        stripe_h = cape_h / len(colors)
        for i, col in enumerate(colors):
            pygame.draw.rect(color_surf, col, (0, top_y + i*stripe_h, size, stripe_h + 1))
        
        # Masking (multiplicative)
        color_surf.blit(cape_surf, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
        surf.blit(color_surf, (0,0))
        pygame.draw.polygon(surf, (255, 255, 255), cape_points, 2)
        
        # Head orb
        pygame.draw.circle(surf, (240, 240, 245), (cx, head_y), head_r)
        pygame.draw.circle(surf, (255, 255, 255), (cx, head_y), head_r * 0.6)
        
        # Little prism glow
        pygame.draw.circle(surf, (255, 0, 255), (cx - 4, head_y), 2)
        pygame.draw.circle(surf, (0, 255, 255), (cx + 4, head_y), 2)

    elif skin == "juneteenth":
        # Black, green, red cape
        pygame.draw.polygon(surf, (20, 20, 20), cape_points)
        # Red top half
        red_points = [
            (cx - cape_top_w//2, top_y),
            (cx + cape_top_w//2, top_y),
            (cx + cape_bot_w//3, bot_y - cape_h//2),
            (cx - cape_bot_w//3, bot_y - cape_h//2)
        ]
        pygame.draw.polygon(surf, (200, 30, 30), red_points)
        pygame.draw.polygon(surf, (0, 160, 60), cape_points, 2)
        
        # Freedom star
        for i in range(5):
            angle = math.radians(i*72 - 90)
            x = cx + 5 * math.cos(angle)
            y = top_y + cape_h//2.5 + 5 * math.sin(angle)
            pygame.draw.circle(surf, (255, 215, 0), (int(x), int(y)), 2)
            
        # Head
        pygame.draw.circle(surf, (90, 45, 25), (cx, head_y), head_r)
        pygame.draw.circle(surf, (150, 85, 45), (cx, head_y), head_r * 0.5)

    elif skin == "eclipse":
        # Vantablack cape with silver rim
        pygame.draw.polygon(surf, (5, 5, 8), cape_points)
        pygame.draw.polygon(surf, (180, 200, 220), cape_points, 1)
        
        # Corona glow behind head
        glow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (220, 230, 255, 100), (cx, head_y), head_r + 4 + math.sin(animation_offset*4)*2)
        surf.blit(glow_surf, (0,0))
        
        # Pitch black head
        pygame.draw.circle(surf, (0, 0, 0), (cx, head_y), head_r)
        # Crescent sliver
        pygame.draw.arc(surf, (255, 255, 255), (cx - head_r + 1, head_y - head_r + 1, head_r*2-2, head_r*2-2), math.pi/2, math.pi*1.5, 2)
        
    elif skin == "fathers_day":
        # Checkered flannel cape (blue & green plaid pattern)
        pygame.draw.polygon(surf, (30, 80, 50), cape_points)
        # Draw blue plaid lines
        grid_lines = 4
        for i in range(1, grid_lines):
            t = i / grid_lines
            top_x = (cx - cape_top_w//2) * (1 - t) + (cx + cape_top_w//2) * t
            bot_x = (cx - cape_bot_w//2) * (1 - t) + (cx + cape_bot_w//2) * t
            pygame.draw.line(surf, (30, 60, 150), (top_x, top_y), (bot_x, bot_y), 2)
            
            ly = top_y + t * cape_h
            lx_left = (cx - cape_top_w//2) * (1 - t) + (cx - cape_bot_w//2) * t
            lx_right = (cx + cape_top_w//2) * (1 - t) + (cx + cape_bot_w//2) * t
            pygame.draw.line(surf, (30, 60, 150), (lx_left, ly), (lx_right, ly), 2)
            
        pygame.draw.polygon(surf, (50, 120, 80), cape_points, 2)
        
        # Skin colored head
        pygame.draw.circle(surf, (240, 200, 160), (cx, head_y), head_r)
        
        # Mustache
        mustache_y = head_y + 2
        pygame.draw.polygon(surf, (70, 45, 30), [
            (cx - 6, mustache_y), (cx - 2, mustache_y - 1), (cx, mustache_y + 1),
            (cx + 2, mustache_y - 1), (cx + 6, mustache_y), (cx + 4, mustache_y + 3),
            (cx, mustache_y + 1), (cx - 4, mustache_y + 3)
        ])
        
        # Red baseball cap dome
        cap_points = []
        for angle_deg in range(180, 361, 15):
            angle_rad = math.radians(angle_deg)
            rx = head_r + 1
            ry = head_r
            cap_points.append((cx + rx * math.cos(angle_rad), head_y + ry * math.sin(angle_rad)))
        cap_points.append((cx + head_r + 1, head_y))
        cap_points.append((cx - head_r - 1, head_y))
        pygame.draw.polygon(surf, (200, 30, 30), cap_points)
        
        # Cap brim (visor)
        brim_points = [
            (cx - head_r, head_y),
            (cx + head_r + 4, head_y),
            (cx + head_r + 5, head_y + 2),
            (cx - head_r, head_y + 2)
        ]
        pygame.draw.polygon(surf, (220, 40, 40), brim_points)
        # Button on top
        pygame.draw.circle(surf, (255, 215, 0), (cx, head_y - head_r), 2)
        
    elif skin == "rockstar":
        # Neon purple/indigo cape
        pygame.draw.polygon(surf, (40, 20, 80), cape_points)
        pygame.draw.polygon(surf, (150, 50, 220), cape_points, 2)
        
        # Neon musical notes on cape
        note_y = top_y + cape_h // 2
        pygame.draw.circle(surf, (0, 255, 255), (cx - 4, note_y + 4), 2)
        pygame.draw.line(surf, (0, 255, 255), (cx - 2, note_y + 4), (cx - 2, note_y - 2), 2)
        pygame.draw.circle(surf, (255, 50, 150), (cx + 4, note_y + 6), 2)
        pygame.draw.line(surf, (255, 50, 150), (cx + 6, note_y + 6), (cx + 6, note_y), 2)
        pygame.draw.line(surf, (255, 255, 100), (cx - 2, note_y - 2), (cx + 6, note_y), 2)
        
        # Rockstar Head
        pygame.draw.circle(surf, (200, 200, 220), (cx, head_y), head_r)
        
        # Sunglasses
        pygame.draw.ellipse(surf, (10, 10, 15), (cx - head_r*0.7, head_y - head_r*0.2, head_r*0.5, head_r*0.4))
        pygame.draw.ellipse(surf, (10, 10, 15), (cx + head_r*0.2, head_y - head_r*0.2, head_r*0.5, head_r*0.4))
        pygame.draw.line(surf, (10, 10, 15), (cx - 2, head_y), (cx + 2, head_y), 2)
        
        # Headphones
        pygame.draw.ellipse(surf, (150, 150, 160), (cx - head_r - 2, head_y - head_r*0.4, 4, head_r*0.8))
        pygame.draw.ellipse(surf, (100, 100, 110), (cx - head_r - 2, head_y - head_r*0.4, 4, head_r*0.8), 1)
        pygame.draw.ellipse(surf, (150, 150, 160), (cx + head_r - 2, head_y - head_r*0.4, 4, head_r*0.8))
        pygame.draw.ellipse(surf, (100, 100, 110), (cx + head_r - 2, head_y - head_r*0.4, 4, head_r*0.8), 1)
        pygame.draw.arc(surf, (120, 120, 130), (cx - head_r - 1, head_y - head_r - 2, head_r*2 + 2, head_r*2), 0, math.pi, 2)
        
    return surf
