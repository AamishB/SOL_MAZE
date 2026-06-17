import pygame
import math

def draw_sun_icon(size, angle_deg=0):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size//2
    radius = size//3
    # Glow
    for r in range(radius+2, radius-2, -2):
        alpha = max(0, min(255, 255 - (r - radius) * 60))
        glow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(glow_surf, (255,200,100), (center,center), r)
        glow_surf.set_alpha(alpha)
        surf.blit(glow_surf, (0,0))
    # Core
    pygame.draw.circle(surf, (255,180,40), (center,center), radius)
    # Rays
    rad_angle = math.radians(angle_deg)
    for i in range(12):
        a = rad_angle + i * math.pi/6
        dx = math.cos(a) * (radius+4)
        dy = math.sin(a) * (radius+4)
        pygame.draw.line(surf, (255,220,80), (center,center), (center+dx, center+dy), 2)
    return surf

def draw_moon_icon(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    center = size//2
    radius = size//3
    # Glow
    glow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.circle(glow_surf, (180,180,220), (center,center), radius+6)
    glow_surf.set_alpha(80)
    surf.blit(glow_surf, (0,0))
    # Crescent: draw full circle then overlay shadow
    pygame.draw.circle(surf, (220,220,255), (center,center), radius)
    shadow_rect = (center - radius//2, center - radius, radius, radius*2)
    shadow_surf = pygame.Surface((size, size), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surf, (0,0,0), shadow_rect)
    shadow_surf.set_alpha(180)
    surf.blit(shadow_surf, (0,0))
    return surf

def draw_leaf_icon(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size//2, size//2
    pts = [
        (cx, cy - size*0.3),
        (cx + size*0.25, cy),
        (cx, cy + size*0.3),
        (cx - size*0.25, cy)
    ]
    pygame.draw.polygon(surf, (50, 200, 80), pts)
    pygame.draw.polygon(surf, (100, 255, 120), pts, 2)
    pygame.draw.line(surf, (20, 100, 40), (cx, cy + size*0.3), (cx, cy - size*0.2), 2)
    return surf

def draw_wave_icon(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size//2, size//2
    pts1 = [(x, cy - size*0.1 + math.sin(x*0.3)*size*0.1) for x in range(int(size*0.2), int(size*0.8))]
    pts2 = [(x, cy + size*0.1 + math.sin(x*0.3 + 1)*size*0.1) for x in range(int(size*0.2), int(size*0.8))]
    if len(pts1) > 1: pygame.draw.lines(surf, (50, 150, 255), False, pts1, 3)
    if len(pts2) > 1: pygame.draw.lines(surf, (100, 200, 255), False, pts2, 3)
    return surf

def draw_music_note_icon(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size//2, size//2
    color = (255, 100, 150)
    pygame.draw.circle(surf, color, (cx - size*0.15, cy + size*0.15), size*0.1)
    pygame.draw.circle(surf, color, (cx + size*0.15, cy + size*0.05), size*0.1)
    pygame.draw.line(surf, color, (cx - size*0.05, cy + size*0.15), (cx - size*0.05, cy - size*0.2), 2)
    pygame.draw.line(surf, color, (cx + size*0.25, cy + size*0.05), (cx + size*0.25, cy - size*0.3), 2)
    pygame.draw.line(surf, color, (cx - size*0.05, cy - size*0.2), (cx + size*0.25, cy - size*0.3), 3)
    return surf

def draw_rainbow_icon(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size//2, size*0.7
    colors = [(228,3,3),(255,140,0),(255,237,0),(0,128,38),(36,64,142),(115,41,130)]
    radius = size * 0.4
    thickness = max(1, int(radius / len(colors)))
    for i, col in enumerate(colors):
        r = radius - i*thickness
        if r > 0:
            rect = (cx - r, cy - r, r*2, r*2)
            pygame.draw.arc(surf, col, rect, 0, math.pi, thickness+1)
    return surf

def draw_bell_icon(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size//2, size//2
    color = (200, 180, 50)
    pts = [(cx, cy - size*0.2), (cx + size*0.2, cy + size*0.2), (cx - size*0.2, cy + size*0.2)]
    pygame.draw.polygon(surf, color, pts)
    pygame.draw.circle(surf, color, (cx, cy - size*0.2), size*0.1)
    pygame.draw.circle(surf, color, (cx, cy + size*0.25), size*0.05)
    return surf

def draw_tie_icon(size):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    cx, cy = size//2, size//2
    color = (50, 100, 200)
    pygame.draw.polygon(surf, color, [(cx-4, cy-size*0.2), (cx+4, cy-size*0.2), (cx+3, cy-size*0.1), (cx-3, cy-size*0.1)])
    pygame.draw.polygon(surf, color, [(cx-3, cy-size*0.1), (cx+3, cy-size*0.1), (cx+6, cy+size*0.2), (cx, cy+size*0.3), (cx-6, cy+size*0.2)])
    return surf
