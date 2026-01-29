import pygame
from utils.constants import *


class Enemy:
    """Enemy base class - Goomba, Koopa, Flying variants"""
    def __init__(self, x, y, direction=1, enemy_type="goomba"):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 24
        self.vel_x = direction * (2 if enemy_type == "goomba" else 3 if enemy_type == "koopa" else 4)
        self.vel_y = 0
        self.gravity = 0.6
        self.on_ground = False
        self.direction = direction
        self.enemy_type = enemy_type
        self.anim_frame = 0
        self.bob_offset = 0  # For flying enemies
    
    def update(self):
        # Apply gravity (flying enemies don't use gravity the same way)
        if self.enemy_type != "flying":
            if not self.on_ground:
                self.vel_y += self.gravity
                self.vel_y = min(self.vel_y, 15)
        else:
            # Flying enemy bobbing
            self.bob_offset += 0.1
        
        # Move
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Animation
        self.anim_frame += 0.2
        if self.anim_frame > 6:
            self.anim_frame = 0
        
        # Die if off screen
        if self.x < -50 or self.x > SCREEN_WIDTH + 500 or self.y > SCREEN_HEIGHT:
            return False
        
        return True
        
        return True
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface):
        """Draw enemy based on type"""
        if self.enemy_type == "goomba":
            self._draw_goomba(surface)
        elif self.enemy_type == "koopa":
            self._draw_koopa(surface)
        elif self.enemy_type == "flying":
            self._draw_flying(surface)
    
    def _draw_goomba(self, surface):
        """Draw Goomba enemy"""
        rect = self.get_rect()
        
        # Draw shadow
        shadow_width = int(self.width * 1.1)
        pygame.draw.ellipse(surface, (40, 40, 60), pygame.Rect(
            self.x + self.width // 2 - shadow_width // 2, 
            self.y + self.height + 1, 
            shadow_width, 5
        ))
        
        # Body base color (brown with gradient effect)
        body_color = (139, 69, 19)
        pygame.draw.rect(surface, body_color, rect)
        
        # Body shading (darker bottom)
        dark_body_color = (100, 50, 10)
        pygame.draw.rect(surface, dark_body_color, (rect.x, rect.y + rect.height // 2, rect.width, rect.height // 2), 0)
        
        # Body top highlight (lighter brown)
        light_body_color = (180, 100, 40)
        pygame.draw.line(surface, light_body_color, (rect.x, rect.y), (rect.x + rect.width, rect.y), 2)
        
        # Head section with ridge
        head_y = rect.y + 6
        pygame.draw.line(surface, (100, 50, 10), (rect.x, head_y), (rect.x + rect.width, head_y), 1)
        
        # Eyes
        left_eye_x = int(self.x + 10)
        right_eye_x = int(self.x + 22)
        eye_y = int(self.y + 8)
        
        # Eye whites
        pygame.draw.circle(surface, WHITE, (left_eye_x, eye_y), 3)
        pygame.draw.circle(surface, WHITE, (right_eye_x, eye_y), 3)
        
        # Eye pupils
        pupil_offset = 2 if self.direction > 0 else -2
        pygame.draw.circle(surface, BLACK, (left_eye_x + pupil_offset, eye_y), 2)
        pygame.draw.circle(surface, BLACK, (right_eye_x + pupil_offset, eye_y), 2)
        
        # Eyebrows
        pygame.draw.line(surface, (80, 30, 0), (left_eye_x - 2, eye_y - 3), (left_eye_x + 2, eye_y - 3), 1)
        pygame.draw.line(surface, (80, 30, 0), (right_eye_x - 2, eye_y - 3), (right_eye_x + 2, eye_y - 3), 1)
        
        # Mouth
        pygame.draw.line(surface, (80, 30, 0), (int(self.x + 14), int(self.y + 16)), (int(self.x + 18), int(self.y + 16)), 1)
        
        # Feet (shoes)
        foot_color = (60, 30, 10)
        pygame.draw.rect(surface, foot_color, (rect.x + 6, rect.y + rect.height - 3, 8, 3))
        pygame.draw.rect(surface, foot_color, (rect.x + 18, rect.y + rect.height - 3, 8, 3))
        
        # Feet highlights
        pygame.draw.line(surface, (100, 50, 10), (rect.x + 8, rect.y + rect.height - 4), (rect.x + 14, rect.y + rect.height - 4), 1)
        pygame.draw.line(surface, (100, 50, 10), (rect.x + 20, rect.y + rect.height - 4), (rect.x + 26, rect.y + rect.height - 4), 1)
        
        # Body border
        pygame.draw.rect(surface, (80, 30, 0), rect, 2)
    
    def _draw_koopa(self, surface):
        """Draw Koopa Troopa (faster enemy with shell)"""
        rect = self.get_rect()
        
        # Shadow
        shadow_width = int(self.width * 1.1)
        pygame.draw.ellipse(surface, (40, 40, 60), pygame.Rect(
            self.x + self.width // 2 - shadow_width // 2, 
            self.y + self.height + 1, 
            shadow_width, 5
        ))
        
        # Shell (green)
        shell_color = (0, 150, 0)
        pygame.draw.ellipse(surface, shell_color, pygame.Rect(rect.x + 4, rect.y + 2, rect.width - 8, 16))
        pygame.draw.line(surface, (50, 200, 50), (rect.x + 4, rect.y + 10), (rect.x + rect.width - 4, rect.y + 10), 2)
        
        # Head
        head_color = (100, 180, 100)
        pygame.draw.rect(surface, head_color, (rect.x + 8, rect.y - 2, rect.width - 16, 6))
        
        # Eyes
        left_eye_x = int(self.x + 12)
        right_eye_x = int(self.x + 20)
        eye_y = int(self.y + 0)
        
        pygame.draw.circle(surface, WHITE, (left_eye_x, eye_y), 2)
        pygame.draw.circle(surface, WHITE, (right_eye_x, eye_y), 2)
        pygame.draw.circle(surface, BLACK, (left_eye_x, eye_y), 1)
        pygame.draw.circle(surface, BLACK, (right_eye_x, eye_y), 1)
        
        # Feet
        foot_color = (100, 50, 10)
        pygame.draw.rect(surface, foot_color, (rect.x + 6, rect.y + rect.height - 3, 6, 3))
        pygame.draw.rect(surface, foot_color, (rect.x + 20, rect.y + rect.height - 3, 6, 3))
        
        pygame.draw.rect(surface, (0, 100, 0), rect, 2)
    
    def _draw_flying(self, surface):
        """Draw Flying enemy (Bullet Bill style)"""
        rect = self.get_rect()
        
        # Add bobbing motion
        bob_y = int(2 * abs(pygame.math.Vector2(1, 0).rotate(self.bob_offset).y))
        draw_rect = pygame.Rect(rect.x, rect.y - bob_y, rect.width, rect.height)
        
        # Shadow
        shadow_width = int(self.width * 0.9)
        pygame.draw.ellipse(surface, (40, 40, 60), pygame.Rect(
            self.x + self.width // 2 - shadow_width // 2, 
            self.y + self.height + 1, 
            shadow_width, 4
        ))
        
        # Body (black bullet shape)
        body_color = (30, 30, 30)
        pygame.draw.rect(surface, body_color, (draw_rect.x + 2, draw_rect.y + 4, draw_rect.width - 4, draw_rect.height - 8))
        
        # Nose point
        nose_points = [
            (draw_rect.x + draw_rect.width, draw_rect.y + draw_rect.height // 2),
            (draw_rect.x + draw_rect.width - 6, draw_rect.y + 4),
            (draw_rect.x + draw_rect.width - 6, draw_rect.y + draw_rect.height - 4)
        ]
        pygame.draw.polygon(surface, body_color, nose_points)
        
        # Eye
        eye_x = int(self.x + 12)
        eye_y = int(self.y - bob_y + 12)
        pygame.draw.circle(surface, WHITE, (eye_x, eye_y), 2)
        pygame.draw.circle(surface, BLACK, (eye_x, eye_y), 1)
        
        # Speed lines
        line_y = draw_rect.y + draw_rect.height // 2
        pygame.draw.line(surface, (100, 100, 100), (draw_rect.x - 4, line_y), (draw_rect.x, line_y), 1)
        pygame.draw.line(surface, (100, 100, 100), (draw_rect.x - 8, line_y + 4), (draw_rect.x - 2, line_y + 4), 1)
        
        pygame.draw.rect(surface, (50, 50, 50), draw_rect, 1)
