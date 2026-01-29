import pygame
from utils.constants import *


class Platform:
    """Game platform"""
    def __init__(self, x, y, width, height, platform_type="normal"):
        self.rect = pygame.Rect(x, y, width, height)
        self.platform_type = platform_type  # "normal", "coin", "spike"
        self.coin_collected = False
        self.bounce_timer = 0
    
    def draw(self, surface):
        if self.platform_type == "normal":
            # Base platform color (green-brown)
            base_color = (100, 130, 50)
            pygame.draw.rect(surface, base_color, self.rect)
            
            # Top highlight for depth
            pygame.draw.line(surface, (140, 170, 80), (self.rect.x, self.rect.y), 
                           (self.rect.x + self.rect.width, self.rect.y), 3)
            
            # Bottom shadow
            pygame.draw.line(surface, (60, 80, 20), (self.rect.x, self.rect.y + self.rect.height - 1), 
                           (self.rect.x + self.rect.width, self.rect.y + self.rect.height - 1), 2)
            
            # Wood grain pattern with blocks
            block_width = 16
            for i in range(0, self.rect.width, block_width):
                # Brick pattern
                brick_rect = pygame.Rect(self.rect.x + i, self.rect.y, block_width - 1, self.rect.height)
                pygame.draw.rect(surface, (80, 110, 40), brick_rect, 1)
                
                # Diagonal wood grain lines
                start_x = self.rect.x + i + 2
                end_x = self.rect.x + i + block_width - 2
                start_y = self.rect.y + 2
                end_y = self.rect.y + self.rect.height - 2
                pygame.draw.line(surface, (70, 100, 30), (start_x, start_y), (end_x, end_y), 1)
            
            # Overall border
            pygame.draw.rect(surface, (50, 70, 20), self.rect, 2)
        
        elif self.platform_type == "coin":
            # Coin platform - golden yellow with detail
            platform_color = (200, 150, 0)
            pygame.draw.rect(surface, platform_color, self.rect)
            
            # Top highlight
            pygame.draw.line(surface, (255, 200, 50), (self.rect.x, self.rect.y), 
                           (self.rect.x + self.rect.width, self.rect.y), 3)
            
            # Bottom shadow
            pygame.draw.line(surface, (150, 100, 0), (self.rect.x, self.rect.y + self.rect.height - 1), 
                           (self.rect.x + self.rect.width, self.rect.y + self.rect.height - 1), 2)
            
            # Coin circle in center
            coin_color = (255, 220, 0)
            pygame.draw.circle(surface, coin_color, (self.rect.centerx, self.rect.centery), 10)
            pygame.draw.circle(surface, (200, 170, 0), (self.rect.centerx, self.rect.centery), 10, 1)
            
            # Coin shine
            pygame.draw.circle(surface, (255, 240, 100), (self.rect.centerx - 3, self.rect.centery - 3), 3)
            
            # Border
            pygame.draw.rect(surface, (150, 100, 0), self.rect, 2)
        
        elif self.platform_type == "spike":
            # Spike platform - dark red with menacing spikes
            platform_color = (120, 20, 20)
            pygame.draw.rect(surface, platform_color, self.rect)
            
            # Top shadow under spikes
            pygame.draw.line(surface, (80, 10, 10), (self.rect.x, self.rect.y), 
                           (self.rect.x + self.rect.width, self.rect.y), 2)
            
            # Bottom highlight
            pygame.draw.line(surface, (160, 40, 40), (self.rect.x, self.rect.y + self.rect.height - 1), 
                           (self.rect.x + self.rect.width, self.rect.y + self.rect.height - 1), 2)
            
            # Draw spikes with shading
            spike_spacing = 10
            for i in range(self.rect.x, self.rect.x + self.rect.width, spike_spacing):
                # Outer spike (darker)
                pygame.draw.polygon(surface, (160, 40, 40), [
                    (i, self.rect.y),
                    (i + 5, self.rect.y - 10),
                    (i + 10, self.rect.y)
                ])
                # Inner spike highlight (lighter)
                pygame.draw.polygon(surface, (200, 60, 60), [
                    (i + 2, self.rect.y - 1),
                    (i + 5, self.rect.y - 7),
                    (i + 8, self.rect.y - 1)
                ])
            
            # Border
            pygame.draw.rect(surface, (80, 10, 10), self.rect, 2)
