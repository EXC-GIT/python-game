import pygame
from utils.constants import *


class Checkpoint:
    """Checkpoint/flag for saving player progress"""
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 100
        self.pole_color = (139, 69, 19)  # Brown
        self.flag_color = (255, 0, 0)    # Red
        self.flag_width = 50
        self.flag_height = 30
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.width // 2, self.y - self.height, self.width, self.height)
    
    def draw(self, surface):
        """Draw checkpoint flag and pole"""
        # Draw pole
        pygame.draw.rect(surface, self.pole_color, 
                        (self.x - 3, self.y - self.height, 6, self.height))
        
        # Draw flag
        pygame.draw.rect(surface, self.flag_color,
                        (self.x + 3, self.y - self.height + 10, self.flag_width, self.flag_height))
        
        # Draw flag outline
        pygame.draw.rect(surface, (200, 0, 0),
                        (self.x + 3, self.y - self.height + 10, self.flag_width, self.flag_height), 2)
