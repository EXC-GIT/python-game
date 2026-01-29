import pygame
import random
from utils.constants import *
from utils.sound_manager import SoundManager
from utils.particle import Particle
from .character import Character


class KOFGame:
    """King of Fighters game"""
    def __init__(self):
        self.player1 = None
        self.player2 = None
        self.particles = []
        self.sound_manager = SoundManager()  # Initialize sound manager
    
    def start_fight(self, char1_name, char2_name):
        """Initialize a new fight"""
        self.player1 = Character(char1_name, 200, GROUND_Y, is_player1=True)
        self.player2 = Character(char2_name, SCREEN_WIDTH - 250, GROUND_Y, is_player1=False)
    
    def handle_input(self, keys):
        """Handle player input"""
        # Player 1 controls (WASD + QER)
        move_p1 = 0
        if keys[pygame.K_d]:
            move_p1 = 1
        if keys[pygame.K_a]:
            move_p1 = -1
        
        self.player1.move(move_p1)
        
        if keys[pygame.K_w]:
            self.player1.jump()
        
        if keys[pygame.K_q]:
            self.player1.punch()
        if keys[pygame.K_e]:
            self.player1.kick()
        if keys[pygame.K_r]:
            self.player1.special_attack()
        
        if keys[pygame.K_LCTRL]:
            self.player1.block()
        else:
            self.player1.unblock()
        
        # Player 2 controls (Arrows + UIO)
        move_p2 = 0
        if keys[pygame.K_LEFT]:
            move_p2 = -1
        if keys[pygame.K_RIGHT]:
            move_p2 = 1
        
        self.player2.move(move_p2)
        
        if keys[pygame.K_UP]:
            self.player2.jump()
        
        if keys[pygame.K_u]:
            self.player2.punch()
        if keys[pygame.K_i]:
            self.player2.kick()
        if keys[pygame.K_o]:
            self.player2.special_attack()
        
        if keys[pygame.K_RCTRL]:
            self.player2.block()
        else:
            self.player2.unblock()
    
    def update(self):
        """Update game state"""
        self.player1.update()
        self.player2.update()
        
        # Check collisions
        self.check_attack_collisions()
        
        # Push characters apart if overlapping
        self.separate_characters()
    
    def check_attack_collisions(self):
        """Check if attacks hit"""
        # Player 1 attack vs Player 2
        if self.player1.current_attack:
            p1_attack_rect = self.player1.get_attack_rect()
            if p1_attack_rect and p1_attack_rect.colliderect(self.player2.get_rect()):
                attack_type, _ = self.player1.current_attack
                damage = 0
                knockback = 0
                
                if attack_type == "punch":
                    damage = PUNCH_DAMAGE
                    knockback = -2
                elif attack_type == "kick":
                    damage = KICK_DAMAGE
                    knockback = -3
                elif attack_type == "special":
                    damage = SPECIAL_DAMAGE
                    knockback = -5
                
                # Apply combo bonus
                if self.player1.combo_counter > 1:
                    damage = int(damage * (1 + self.player1.combo_counter * 0.1))
                
                self.player2.take_damage(damage, knockback)
                self.player1.current_attack = None
                self.sound_manager.play('hit')  # Play hit sound
                
                # Create hit particles
                hit_x = self.player2.x + self.player2.width // 2
                hit_y = self.player2.y + self.player2.height // 2
                for _ in range(8):
                    angle = random.uniform(0, 360)
                    speed = random.uniform(2, 5)
                    vel_x = speed * pygame.math.Vector2(1, 0).rotate(angle).x
                    vel_y = speed * pygame.math.Vector2(1, 0).rotate(angle).y
                    self.particles.append(Particle(hit_x, hit_y, vel_x, vel_y, (255, 100, 0), 20))
        
        # Player 2 attack vs Player 1
        if self.player2.current_attack:
            p2_attack_rect = self.player2.get_attack_rect()
            if p2_attack_rect and p2_attack_rect.colliderect(self.player1.get_rect()):
                attack_type, _ = self.player2.current_attack
                damage = 0
                knockback = 0
                
                if attack_type == "punch":
                    damage = PUNCH_DAMAGE
                    knockback = 2
                elif attack_type == "kick":
                    damage = KICK_DAMAGE
                    knockback = 3
                elif attack_type == "special":
                    damage = SPECIAL_DAMAGE
                    knockback = 5
                
                # Apply combo bonus
                if self.player2.combo_counter > 1:
                    damage = int(damage * (1 + self.player2.combo_counter * 0.1))
                
                self.player1.take_damage(damage, knockback)
                self.player2.current_attack = None
                self.sound_manager.play('hit')  # Play hit sound
                
                # Create hit particles
                hit_x = self.player1.x + self.player1.width // 2
                hit_y = self.player1.y + self.player1.height // 2
                for _ in range(8):
                    angle = random.uniform(0, 360)
                    speed = random.uniform(2, 5)
                    vel_x = speed * pygame.math.Vector2(1, 0).rotate(angle).x
                    vel_y = speed * pygame.math.Vector2(1, 0).rotate(angle).y
                    self.particles.append(Particle(hit_x, hit_y, vel_x, vel_y, (255, 100, 0), 20))
    
    def separate_characters(self):
        """Prevent characters from overlapping"""
        p1_rect = self.player1.get_rect()
        p2_rect = self.player2.get_rect()
        
        if p1_rect.colliderect(p2_rect):
            # Push them apart
            overlap = p1_rect.right - p2_rect.left
            if overlap > 0:
                self.player1.x -= overlap // 2
                self.player2.x += overlap // 2
    
    def draw(self, surface):
        """Draw game with enhanced visuals"""
        # Gradient sky background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(50 + (100 - 50) * color_ratio)
            g = int(70 + (120 - 70) * color_ratio)
            b = int(120 + (180 - 120) * color_ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Distant mountains/scenery
        pygame.draw.polygon(surface, (80, 100, 120), [
            (0, GROUND_Y - 120),
            (300, GROUND_Y - 80),
            (600, GROUND_Y - 100),
            (900, GROUND_Y - 70),
            (SCREEN_WIDTH, GROUND_Y - 100),
            (SCREEN_WIDTH, GROUND_Y - 150),
            (0, GROUND_Y - 150)
        ])
        
        # Arena back wall with detail
        pygame.draw.rect(surface, (60, 60, 80), (0, GROUND_Y - 100, SCREEN_WIDTH, 100))
        
        # Wall pattern
        for x in range(0, SCREEN_WIDTH, 80):
            pygame.draw.line(surface, (100, 100, 130), (x, GROUND_Y - 100), (x, GROUND_Y), 2)
            pygame.draw.line(surface, (40, 40, 50), (x + 40, GROUND_Y - 100), (x + 40, GROUND_Y), 1)
        
        # Horizontal lines for detail
        for y in range(GROUND_Y - 100, GROUND_Y, 20):
            pygame.draw.line(surface, (80, 80, 100), (0, y), (SCREEN_WIDTH, y), 1)
        
        # Fight stage floor with gradient
        floor_color_start = (100, 120, 60)
        floor_color_end = (80, 100, 40)
        stage_height = 70
        
        for y in range(stage_height):
            color_ratio = y / stage_height
            r = int(floor_color_start[0] + (floor_color_end[0] - floor_color_start[0]) * color_ratio)
            g = int(floor_color_start[1] + (floor_color_end[1] - floor_color_start[1]) * color_ratio)
            b = int(floor_color_start[2] + (floor_color_end[2] - floor_color_start[2]) * color_ratio)
            pygame.draw.line(surface, (r, g, b), (0, GROUND_Y + y), (SCREEN_WIDTH, GROUND_Y + y))
        
        # Stage edge highlight
        pygame.draw.line(surface, (150, 170, 100), (0, GROUND_Y), (SCREEN_WIDTH, GROUND_Y), 3)
        
        # Stage edge shadow
        pygame.draw.line(surface, (50, 60, 30), (0, GROUND_Y + 68), (SCREEN_WIDTH, GROUND_Y + 68), 2)
        
        # Decorative arena features
        pygame.draw.rect(surface, (70, 70, 90), (100, GROUND_Y - 80, 30, 80))
        pygame.draw.rect(surface, (70, 70, 90), (SCREEN_WIDTH - 130, GROUND_Y - 80, 30, 80))
        
        # Lighting effects on stage
        light_color = (200, 180, 100, 100)
        pygame.draw.polygon(surface, (200, 180, 100), [
            (SCREEN_WIDTH // 2 - 200, GROUND_Y - 100),
            (SCREEN_WIDTH // 2 + 200, GROUND_Y - 100),
            (SCREEN_WIDTH // 2 + 150, GROUND_Y),
            (SCREEN_WIDTH // 2 - 150, GROUND_Y)
        ])
        
        # Draw shadows under characters (enhanced)
        shadow_width = int(self.player1.width * 1.2)
        shadow_height = 12
        
        # Player 1 shadow with gradient
        p1_shadow_x = self.player1.x + self.player1.width // 2 - shadow_width // 2
        p1_shadow_y = GROUND_Y + self.player1.height - 5
        pygame.draw.ellipse(surface, (30, 30, 40), pygame.Rect(p1_shadow_x, p1_shadow_y, shadow_width, shadow_height))
        pygame.draw.ellipse(surface, (60, 60, 80), pygame.Rect(p1_shadow_x + 2, p1_shadow_y + 2, shadow_width - 4, shadow_height - 4))
        
        # Player 2 shadow
        p2_shadow_x = self.player2.x + self.player2.width // 2 - shadow_width // 2
        p2_shadow_y = GROUND_Y + self.player2.height - 5
        pygame.draw.ellipse(surface, (30, 30, 40), pygame.Rect(p2_shadow_x, p2_shadow_y, shadow_width, shadow_height))
        pygame.draw.ellipse(surface, (60, 60, 80), pygame.Rect(p2_shadow_x + 2, p2_shadow_y + 2, shadow_width - 4, shadow_height - 4))
        
        # Draw characters
        self.player1.draw(surface)
        self.player2.draw(surface)
        
        # Update and draw particles with better effects
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime > 0:
                particle.draw(surface)
            else:
                self.particles.remove(particle)
        
        # Add glow effect around active attack zone
        if self.player1.current_attack:
            p1_attack_rect = self.player1.get_attack_rect()
            if p1_attack_rect:
                pygame.draw.rect(surface, (255, 150, 0), p1_attack_rect, 1)
        
        if self.player2.current_attack:
            p2_attack_rect = self.player2.get_attack_rect()
            if p2_attack_rect:
                pygame.draw.rect(surface, (255, 150, 0), p2_attack_rect, 1)
