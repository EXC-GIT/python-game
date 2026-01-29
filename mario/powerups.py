import pygame
from utils.constants import *


class PowerUp:
    """Base power-up class"""
    def __init__(self, x, y, power_type="mushroom"):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.power_type = power_type
        self.vel_y = 0
        self.gravity = 0.6
        self.on_ground = False
        self.bob = 0
        self.active = True
    
    def update(self):
        """Update power-up state"""
        # Apply gravity
        if not self.on_ground:
            self.vel_y += self.gravity
            self.vel_y = min(self.vel_y, 15)
        
        self.y += self.vel_y
        
        # Bobbing animation
        self.bob += 0.1
        
        # Remove if fallen off screen
        if self.y > SCREEN_HEIGHT:
            self.active = False
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface):
        """Draw power-up with animation"""
        bob_offset = int(3 * abs(pygame.math.Vector2(1, 0).rotate(self.bob).y))
        draw_y = self.y - bob_offset
        
        if self.power_type == "mushroom":
            # Red mushroom with spots
            # Stem
            pygame.draw.rect(surface, (100, 80, 60), (int(self.x + 8), int(draw_y + 12), 4, 8))
            # Cap
            pygame.draw.circle(surface, (255, 0, 0), (int(self.x + 10), int(draw_y + 8)), 10)
            # Spots
            pygame.draw.circle(surface, (255, 200, 200), (int(self.x + 5), int(draw_y + 6)), 2)
            pygame.draw.circle(surface, (255, 200, 200), (int(self.x + 15), int(draw_y + 6)), 2)
            pygame.draw.circle(surface, (255, 200, 200), (int(self.x + 10), int(draw_y + 12)), 2)
        
        elif self.power_type == "star":
            # Golden star that rotates
            angle = self.bob
            points = []
            for i in range(10):
                radius = 8 if i % 2 == 0 else 4
                x = self.x + 10 + radius * pygame.math.Vector2(1, 0).rotate(angle + i * 36).x
                y = draw_y + 10 + radius * pygame.math.Vector2(1, 0).rotate(angle + i * 36).y
                points.append((x, y))
            pygame.draw.polygon(surface, (255, 255, 0), points)
            # Star outline
            pygame.draw.polygon(surface, (200, 200, 0), points, 2)
        
        elif self.power_type == "shield":
            # Blue shield
            pygame.draw.circle(surface, (0, 150, 255), (int(self.x + 10), int(draw_y + 10)), 10)
            pygame.draw.circle(surface, (100, 200, 255), (int(self.x + 10), int(draw_y + 10)), 8)
            pygame.draw.circle(surface, (0, 150, 255), (int(self.x + 10), int(draw_y + 10)), 10, 2)
            # Shield letter
            pygame.draw.line(surface, WHITE, (int(self.x + 10), int(draw_y + 5)), 
                           (int(self.x + 10), int(draw_y + 15)), 2)
