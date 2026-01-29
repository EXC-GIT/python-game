import pygame


class Particle:
    """Visual particle effect"""
    def __init__(self, x, y, vel_x, vel_y, color, lifetime=30):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
    
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += 0.3  # Gravity
        self.lifetime -= 1
    
    def draw(self, surface):
        alpha = self.lifetime / self.max_lifetime
        size = max(2, int(4 * alpha))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), size)
