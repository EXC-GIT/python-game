import pygame
from utils.constants import *


class Coin:
    """Collectible coin"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.bob = 0
    
    def update(self):
        self.bob += 0.1
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y - abs(5 * pygame.math.Vector2(1, 0).rotate(self.bob * 10).y), 
                          self.width, self.height)
    
    def draw(self, surface):
        rect = self.get_rect()
        
        # Outer coin ring (dark gold)
        pygame.draw.circle(surface, (200, 150, 0), (int(rect.centerx), int(rect.centery)), 8)
        
        # Main coin body (bright gold with gradient effect)
        pygame.draw.circle(surface, (255, 220, 0), (int(rect.centerx), int(rect.centery)), 7)
        
        # Inner circle (lighter gold)
        pygame.draw.circle(surface, (255, 240, 100), (int(rect.centerx), int(rect.centery)), 5)
        
        # Coin shine highlight (simulates reflection)
        shine_offset = int(2 * pygame.math.Vector2(1, 0).rotate(self.bob * 10).y)
        pygame.draw.circle(surface, (255, 255, 150), 
                          (int(rect.centerx - 2 + shine_offset), int(rect.centery - 3)), 2)
        
        # Coin details - star or design in center
        center_x = int(rect.centerx)
        center_y = int(rect.centery)
        
        # Simple cross pattern
        pygame.draw.line(surface, (200, 150, 0), (center_x - 2, center_y), (center_x + 2, center_y), 1)
        pygame.draw.line(surface, (200, 150, 0), (center_x, center_y - 2), (center_x, center_y + 2), 1)
