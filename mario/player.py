import pygame
from utils.constants import *


class MarioPlayer:
    """Mario character"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_y = 0
        self.vel_x = 0
        self.width = 32
        self.height = 48
        self.on_ground = False
        self.direction = 1  # 1 for right, -1 for left
        self.speed = 4
        self.jump_power = -12
        self.gravity = 0.6
        self.score = 0
        self.coins = 0
        self.lives = 3
        self.is_jumping = False
        self.anim_frame = 0
        self.invincible_timer = 0
        self.is_powered_up = False  # Powered-up state
        self.powerup_timer = 0  # Timer for power-up duration
        self.shield_timer = 0  # Timer for shield protection
    
    def move_left(self):
        self.vel_x = -self.speed
        self.direction = -1
    
    def move_right(self):
        self.vel_x = self.speed
        self.direction = 1
    
    def stop(self):
        self.vel_x = 0
    
    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False
            self.is_jumping = True
    
    def update(self):
        # Apply gravity
        if not self.on_ground:
            self.vel_y += self.gravity
            self.vel_y = min(self.vel_y, 15)
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Allow going off-screen to the right (for scrolling levels)
        # Only prevent going too far left
        if self.x < 0:
            self.x = 0
        
        # Fall death
        if self.y > SCREEN_HEIGHT:
            self.lives -= 1
            self.reset_position()
        
        # Animation
        if self.vel_x != 0:
            self.anim_frame += 0.2
            if self.anim_frame > 6:
                self.anim_frame = 0
        else:
            self.anim_frame = 0
        
        # Invincibility
        # Power-up timer
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
        else:
            self.is_powered_up = False
        
        if self.shield_timer > 0:
            self.shield_timer -= 1
        
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
    
    def reset_position(self, checkpoint_x=50):
        self.x = checkpoint_x
        self.y = GROUND_Y - self.height
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.is_powered_up = False
        self.powerup_timer = 0
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self, surface):
        # Flash when invincible
        if self.invincible_timer > 0 and self.invincible_timer % 10 < 5:
            return
        
        # Draw shield effect if shield is active
        if self.shield_timer > 0:
            shield_radius = int(self.width * 0.7)
            pygame.draw.circle(surface, (0, 150, 255), 
                              (int(self.x + self.width // 2), int(self.y + self.height // 2)), 
                              shield_radius, 2)
        
        # Draw power-up glow if powered up
        if self.is_powered_up:
            glow_radius = int(self.width * 0.8)
            pygame.draw.circle(surface, (255, 200, 0), 
                              (int(self.x + self.width // 2), int(self.y + self.height // 2)), 
                              glow_radius, 1)
        
        # Draw shadow
        shadow_width = int(self.width * 1.2)
        pygame.draw.ellipse(surface, (40, 40, 60), pygame.Rect(
            self.x + self.width // 2 - shadow_width // 2, 
            self.y + self.height + 2, 
            shadow_width, 8
        ))
        
        # Draw shoes (black with detail)
        shoe_color = (0, 0, 0)
        shoe_width = 8
        shoe_height = 6
        
        # Left shoe with highlight
        pygame.draw.rect(surface, shoe_color, (self.x + 6, self.y + self.height - shoe_height, shoe_width, shoe_height))
        pygame.draw.rect(surface, (50, 50, 50), (self.x + 6, self.y + self.height - shoe_height, shoe_width, 2))
        
        # Right shoe with highlight
        pygame.draw.rect(surface, shoe_color, (self.x + self.width - shoe_width - 6, self.y + self.height - shoe_height, shoe_width, shoe_height))
        pygame.draw.rect(surface, (50, 50, 50), (self.x + self.width - shoe_width - 6, self.y + self.height - shoe_height, shoe_width, 2))
        
        # Draw pants (blue with detail)
        pants_color = (0, 40, 140)
        pants_height = 12
        pygame.draw.rect(surface, pants_color, (self.x + 4, self.y + self.height - 18, self.width - 8, pants_height))
        # Pants highlight
        pygame.draw.line(surface, (0, 80, 200), (self.x + 6, self.y + self.height - 18), (self.x + self.width - 6, self.y + self.height - 18), 1)
        
        # Draw torso/body (red with detail)
        body_color = (200, 40, 40)
        body_height = 16
        pygame.draw.rect(surface, body_color, (self.x + 4, self.y + 14, self.width - 8, body_height))
        # Body highlight
        pygame.draw.line(surface, (255, 100, 100), (self.x + 6, self.y + 16), (self.x + self.width - 6, self.y + 16), 1)
        
        # Draw arms (enhanced)
        arm_color = (220, 160, 100)
        arm_width = 6
        arm_height = 14
        
        # Left arm
        pygame.draw.rect(surface, arm_color, (self.x - 2, self.y + 16, arm_width, arm_height))
        pygame.draw.circle(surface, arm_color, (int(self.x + 2), int(self.y + 30)), 3)
        pygame.draw.line(surface, (240, 180, 120), (self.x + 1, self.y + 17), (self.x + 3, self.y + 17), 1)
        
        # Right arm
        pygame.draw.rect(surface, arm_color, (self.x + self.width - 4, self.y + 16, arm_width, arm_height))
        pygame.draw.circle(surface, arm_color, (int(self.x + self.width - 2), int(self.y + 30)), 3)
        pygame.draw.line(surface, (240, 180, 120), (self.x + self.width - 3, self.y + 17), (self.x + self.width - 1, self.y + 17), 1)
        
        # Draw head (skin with detail)
        head_color = (220, 160, 100)
        head_radius = 8
        pygame.draw.circle(surface, head_color, (int(self.x + self.width // 2), int(self.y + 10)), head_radius)
        # Head highlight
        pygame.draw.circle(surface, (240, 180, 120), (int(self.x + self.width // 2 - 2), int(self.y + 6)), 2)
        
        # Draw cap (M logo hat - red)
        cap_color = (200, 40, 40)
        pygame.draw.polygon(surface, cap_color, [
            (self.x + 6, self.y + 2),
            (self.x + self.width - 6, self.y + 2),
            (self.x + self.width - 4, self.y + 8),
            (self.x + 8, self.y + 8)
        ])
        # Cap highlight
        pygame.draw.line(surface, (255, 100, 100), (self.x + 8, self.y + 3), (self.x + self.width - 8, self.y + 3), 1)
        
        # Draw M on cap
        m_color = (255, 200, 50)
        # M letter
        pygame.draw.line(surface, m_color, (self.x + self.width // 2 - 3, self.y + 4), (self.x + self.width // 2 - 3, self.y + 7), 2)
        pygame.draw.line(surface, m_color, (self.x + self.width // 2 - 3, self.y + 4), (self.x + self.width // 2, self.y + 6), 2)
        pygame.draw.line(surface, m_color, (self.x + self.width // 2, self.y + 6), (self.x + self.width // 2 + 3, self.y + 4), 2)
        pygame.draw.line(surface, m_color, (self.x + self.width // 2 + 3, self.y + 4), (self.x + self.width // 2 + 3, self.y + 7), 2)
        
        # Eyes (animated blink)
        eye_color = (0, 0, 0)
        if (int(self.y) // 30) % 2 == 0:  # Simple blink animation
            pygame.draw.circle(surface, eye_color, (int(self.x + self.width // 2 - 2), int(self.y + 8)), 1)
            pygame.draw.circle(surface, eye_color, (int(self.x + self.width // 2 + 2), int(self.y + 8)), 1)
