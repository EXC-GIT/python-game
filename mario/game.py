import pygame
from utils.constants import *
from utils.sound_manager import SoundManager
from utils.score_manager import ScoreManager
from .player import MarioPlayer
from .enemies import Enemy
from .platforms import Platform
from .items import Coin
from .powerups import PowerUp
from .checkpoint import Checkpoint


class MarioGame:
    """Super Mario game"""
    def __init__(self):
        self.player = MarioPlayer(50, GROUND_Y - 48)
        self.platforms = []
        self.enemies = []
        self.coins = []
        self.powerups = []
        self.checkpoints = []
        self.level = 1
        self.game_over = False
        self.won = False
        self.camera_x = 0  # Camera position for scrolling
        self.level_width = 2000  # Extended level width for scrolling
        self.score = 0
        self.sound_manager = SoundManager()  # Initialize sound manager
        self.score_manager = ScoreManager("mario")  # Initialize score manager
        self.last_checkpoint_x = 50  # Track last checkpoint position
        self.create_level()
    
    def create_level(self):
        """Create level layout"""
        self.platforms.clear()
        self.enemies.clear()
        self.coins.clear()
        self.powerups.clear()
        self.player.score = 0
        self.player.coins = 0
        
        # Extended ground across entire level
        self.platforms.append(Platform(0, GROUND_Y, self.level_width, 50, "normal"))
        
        # Level 1 layout - Extended horizontally
        if self.level == 1:
            # First section (starting area)
            self.platforms.append(Platform(150, 450, 150, 20, "normal"))
            self.platforms.append(Platform(400, 380, 150, 20, "normal"))
            self.platforms.append(Platform(650, 310, 150, 20, "normal"))
            self.platforms.append(Platform(250, 300, 150, 20, "coin"))
            self.platforms.append(Platform(800, 400, 150, 20, "normal"))
            self.platforms.append(Platform(1000, 450, 150, 20, "normal"))
            self.platforms.append(Platform(600, 200, 200, 20, "normal"))
            
            # Spike platform
            self.platforms.append(Platform(300, 550, 100, 20, "spike"))
            
            # Second section (extended to right)
            self.platforms.append(Platform(1200, 420, 150, 20, "normal"))
            self.platforms.append(Platform(1450, 380, 140, 20, "normal"))
            self.platforms.append(Platform(1700, 340, 150, 20, "coin"))
            self.platforms.append(Platform(1950, 400, 150, 20, "normal"))
            
            # Elevated platforms in second section
            self.platforms.append(Platform(1300, 300, 120, 20, "normal"))
            self.platforms.append(Platform(1550, 250, 140, 20, "normal"))
            self.platforms.append(Platform(1800, 280, 120, 20, "normal"))
            
            # Peak in second section
            self.platforms.append(Platform(1400, 150, 180, 20, "normal"))
            
            # Coins throughout
            self.coins.append(Coin(200, 400))
            self.coins.append(Coin(450, 330))
            self.coins.append(Coin(700, 260))
            self.coins.append(Coin(850, 350))
            self.coins.append(Coin(1050, 400))
            self.coins.append(Coin(1250, 370))
            self.coins.append(Coin(1500, 330))
            self.coins.append(Coin(1750, 290))
            self.coins.append(Coin(1450, 100))
            
            # Power-ups
            self.powerups.append(PowerUp(320, 480, "mushroom"))  # Mushroom for growing
            self.powerups.append(PowerUp(1500, 200, "star"))  # Star for invincibility
            self.powerups.append(PowerUp(700, 140, "shield"))  # Shield for protection
            
            # Mixed enemy types for variety
            self.enemies.append(Enemy(400, 340, 1, "goomba"))
            self.enemies.append(Enemy(700, 270, -1, "goomba"))
            self.enemies.append(Enemy(1000, 400, 1, "koopa"))  # Faster Koopa
            self.enemies.append(Enemy(1250, 370, 1, "goomba"))
            self.enemies.append(Enemy(1400, 100, -1, "flying"))  # Flying enemy on peak
            self.enemies.append(Enemy(1800, 230, 1, "koopa"))
            self.coins.append(Coin(800, 230))
            self.coins.append(Coin(1050, 390))
            self.coins.append(Coin(700, 100))
            
            # More enemies with different patterns
            self.enemies.append(Enemy(300, 370, 1))
            self.enemies.append(Enemy(600, 310, -1))
            self.enemies.append(Enemy(850, 370, 1))
            self.enemies.append(Enemy(400, 130, -1))
            self.enemies.append(Enemy(800, 100, 1))
            
            # Add checkpoints throughout the level
            self.checkpoints.append(Checkpoint(500, GROUND_Y))   # Early checkpoint
            self.checkpoints.append(Checkpoint(1000, GROUND_Y))  # Mid checkpoint
            self.checkpoints.append(Checkpoint(1500, GROUND_Y))  # Late checkpoint
    
    def update(self):
        """Update game state"""
        if self.game_over or self.won:
            return
        
        self.player.update()
        
        # Update camera position to follow player
        # Keep player near center of screen
        self.camera_x = self.player.x - SCREEN_WIDTH // 3
        # Clamp camera to level bounds
        self.camera_x = max(0, min(self.camera_x, self.level_width - SCREEN_WIDTH))
        
        # Check platform collisions
        self.check_platform_collisions()
        
        # Check coin collisions
        for coin in self.coins[:]:
            if self.player.get_rect().colliderect(coin.get_rect()):
                self.coins.remove(coin)
                self.player.score += 100
                self.player.coins += 1
                self.sound_manager.play('coin')  # Play coin sound
            else:
                coin.update()
        
        # Check power-up collisions
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.active and self.player.get_rect().colliderect(powerup.get_rect()):
                self.powerups.remove(powerup)
                self._apply_powerup(powerup.power_type)
                self.sound_manager.play('powerup')  # Play power-up sound
        
        # Update and check enemy collisions
        for enemy in self.enemies[:]:
            if not enemy.update():
                self.enemies.remove(enemy)
                continue
            
            # Wall collision (for non-flying enemies)
            if enemy.enemy_type != "flying":
                if enemy.x < 0 or enemy.x > self.level_width:
                    enemy.vel_x *= -1
            else:
                # Flying enemies bounce around more
                if enemy.x < 0 or enemy.x > self.level_width - 100:
                    enemy.vel_x *= -1
            
            # Platform collision
            enemy.on_ground = False
            for platform in self.platforms:
                if enemy.get_rect().colliderect(platform.rect):
                    if enemy.vel_y > 0:
                        enemy.y = platform.rect.top - enemy.height
                        enemy.vel_y = 0
                        enemy.on_ground = True
            
            # Enemy-player collision
            if self.player.get_rect().colliderect(enemy.get_rect()):
                if self.player.vel_y > 0 and self.player.y + self.player.height < enemy.get_rect().centery:
                    # Jumped on enemy
                    self.enemies.remove(enemy)
                    self.player.score += 200
                    self.player.vel_y = -8
                else:
                    # Hit by enemy
                    if self.player.invincible_timer <= 0 and self.player.shield_timer <= 0:
                        self.player.lives -= 1
                        self.player.invincible_timer = 120
                        if self.player.lives <= 0:
                            self.game_over = True
                    elif self.player.shield_timer > 0:
                        # Shield protects once
                        self.player.shield_timer = 0
        
        # Check checkpoint collisions
        for checkpoint in self.checkpoints:
            if self.player.get_rect().colliderect(checkpoint.get_rect()):
                self.last_checkpoint_x = checkpoint.x
        
        # Check win condition
        if self.player.coins >= 9:
            self.won = True
            self.sound_manager.play('victory')  # Play victory sound
    
    def _apply_powerup(self, power_type):
        """Apply power-up effect to player"""
        if power_type == "mushroom":
            self.player.is_powered_up = True
            self.player.powerup_timer = 300  # 5 seconds
            self.player.score += 500
        elif power_type == "star":
            self.player.invincible_timer = 300  # 5 seconds of invincibility
            self.player.score += 1000
        elif power_type == "shield":
            self.player.shield_timer = 300  # Shield lasts 5 seconds
            self.player.score += 250
    
    def check_platform_collisions(self):
        """Check collision with platforms"""
        self.player.on_ground = False
        
        for platform in self.platforms:
            player_rect = self.player.get_rect()
            
            if player_rect.colliderect(platform.rect):
                # Coming from above
                if self.player.vel_y > 0 and player_rect.bottom > platform.rect.top:
                    self.player.y = platform.rect.top - self.player.height
                    self.player.vel_y = 0
                    self.player.on_ground = True
                    self.player.is_jumping = False
                    
                    # Spike damage
                    if platform.platform_type == "spike" and self.player.invincible_timer <= 0:
                        self.player.lives -= 1
                        self.player.invincible_timer = 120
                        if self.player.lives <= 0:
                            self.game_over = True
    
    def handle_input(self, keys):
        """Handle player input"""
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        else:
            self.player.stop()
        
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player.jump()
    
    def draw(self, surface):
        """Draw game"""
        # Sky gradient (blue) - full screen
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / GROUND_Y
            r = int(135 + (100 - 135) * min(color_ratio, 1.0))
            g = int(206 + (150 - 206) * min(color_ratio, 1.0))
            b = int(250 + (220 - 250) * min(color_ratio, 1.0))
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Clouds in background (parallax effect - scrolls slower)
        cloud_y = 80
        parallax_offset = int(self.camera_x * 0.3)  # Clouds move slower
        for cloud_x in range(-parallax_offset, SCREEN_WIDTH + 200, 300):
            adjusted_x = cloud_x + parallax_offset
            if -100 < adjusted_x < SCREEN_WIDTH + 100:
                # Cloud shadow
                pygame.draw.ellipse(surface, (150, 150, 200), 
                                  pygame.Rect(adjusted_x - 40, cloud_y + 20, 100, 30))
                # Cloud
                pygame.draw.circle(surface, (255, 255, 255), (adjusted_x - 20, cloud_y), 30)
                pygame.draw.circle(surface, (255, 255, 255), (adjusted_x, cloud_y), 35)
                pygame.draw.circle(surface, (255, 255, 255), (adjusted_x + 20, cloud_y), 30)
        
        # Ground/grass transition
        for y in range(GROUND_Y, GROUND_Y + 20):
            color_ratio = (y - GROUND_Y) / 20
            r = int(100 + (50 - 100) * color_ratio)
            g = int(150 + (100 - 150) * color_ratio)
            b = int(220 + (50 - 220) * color_ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Ground (brown)
        pygame.draw.rect(surface, (80, 60, 40), (0, GROUND_Y + 20, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_Y - 20))
        
        # Distant mountains/hills (parallax background - slower scroll)
        mountain_color = (100, 120, 100)
        mountain_parallax = int(self.camera_x * 0.2)
        pygame.draw.polygon(surface, mountain_color, [
            (-mountain_parallax, GROUND_Y - 100),
            (300 - mountain_parallax, GROUND_Y - 150),
            (600 - mountain_parallax, GROUND_Y - 80),
            (900 - mountain_parallax, GROUND_Y - 140),
            (SCREEN_WIDTH - mountain_parallax, GROUND_Y - 100),
            (SCREEN_WIDTH, GROUND_Y),
            (0, GROUND_Y)
        ])
        
        # Mountain highlights
        pygame.draw.line(surface, (140, 160, 140), (300 - mountain_parallax, GROUND_Y - 150), 
                        (600 - mountain_parallax, GROUND_Y - 80), 2)
        
        # Draw platforms with camera offset
        for platform in self.platforms:
            platform_screen_x = platform.rect.x - self.camera_x
            # Only draw platforms on screen
            if -100 < platform_screen_x < SCREEN_WIDTH + 100:
                # Draw platform manually with offset
                if platform.platform_type == "normal":
                    base_color = (100, 130, 50)
                    pygame.draw.rect(surface, base_color, 
                                   (platform_screen_x, platform.rect.y, platform.rect.width, platform.rect.height))
                    pygame.draw.line(surface, (140, 170, 80), (platform_screen_x, platform.rect.y), 
                                   (platform_screen_x + platform.rect.width, platform.rect.y), 3)
                    pygame.draw.line(surface, (60, 80, 20), (platform_screen_x, platform.rect.y + platform.rect.height - 1), 
                                   (platform_screen_x + platform.rect.width, platform.rect.y + platform.rect.height - 1), 2)
                    for i in range(0, platform.rect.width, 16):
                        pygame.draw.rect(surface, (80, 110, 40), (platform_screen_x + i, platform.rect.y, 15, platform.rect.height), 1)
                    pygame.draw.rect(surface, (50, 70, 20), (platform_screen_x, platform.rect.y, platform.rect.width, platform.rect.height), 2)
                
                elif platform.platform_type == "coin":
                    platform_color = (200, 150, 0)
                    pygame.draw.rect(surface, platform_color, 
                                   (platform_screen_x, platform.rect.y, platform.rect.width, platform.rect.height))
                    pygame.draw.line(surface, (255, 200, 50), (platform_screen_x, platform.rect.y), 
                                   (platform_screen_x + platform.rect.width, platform.rect.y), 3)
                    pygame.draw.circle(surface, (255, 220, 0), (int(platform_screen_x + platform.rect.width // 2), int(platform.rect.centery)), 10)
                    pygame.draw.rect(surface, (150, 100, 0), (platform_screen_x, platform.rect.y, platform.rect.width, platform.rect.height), 2)
                
                elif platform.platform_type == "spike":
                    platform_color = (120, 20, 20)
                    pygame.draw.rect(surface, platform_color, 
                                   (platform_screen_x, platform.rect.y, platform.rect.width, platform.rect.height))
                    for i in range(platform.rect.x, platform.rect.x + platform.rect.width, 10):
                        spike_x = i - self.camera_x
                        pygame.draw.polygon(surface, (200, 60, 60), [
                            (spike_x, platform.rect.y),
                            (spike_x + 5, platform.rect.y - 10),
                            (spike_x + 10, platform.rect.y)
                        ])
                    pygame.draw.rect(surface, (80, 10, 10), (platform_screen_x, platform.rect.y, platform.rect.width, platform.rect.height), 2)
        
        # Draw coins with camera offset
        for coin in self.coins:
            coin_screen_x = coin.x - self.camera_x
            if -20 < coin_screen_x < SCREEN_WIDTH + 20:
                coin.draw(surface)
                # Adjust coin position for drawing
                original_x = coin.x
                coin.x = coin_screen_x
                coin.draw(surface)
                coin.x = original_x
        
        # Draw power-ups with camera offset
        for powerup in self.powerups:
            powerup_screen_x = powerup.x - self.camera_x
            if -30 < powerup_screen_x < SCREEN_WIDTH + 30:
                original_x = powerup.x
                powerup.x = powerup_screen_x
                powerup.draw(surface)
                powerup.x = original_x
        
        # Draw enemies with camera offset
        for enemy in self.enemies:
            enemy_screen_x = enemy.x - self.camera_x
            if -50 < enemy_screen_x < SCREEN_WIDTH + 50:
                original_x = enemy.x
                enemy.x = enemy_screen_x
                enemy.draw(surface)
                enemy.x = original_x
        
        # Draw checkpoints with camera offset
        for checkpoint in self.checkpoints:
            checkpoint_screen_x = checkpoint.x - self.camera_x
            if -50 < checkpoint_screen_x < SCREEN_WIDTH + 50:
                original_x = checkpoint.x
                checkpoint.x = checkpoint_screen_x
                checkpoint.draw(surface)
                checkpoint.x = original_x
        
        # Draw player with camera offset
        player_screen_x = self.player.x - self.camera_x
        original_x = self.player.x
        self.player.x = player_screen_x
        self.player.draw(surface)
        self.player.x = original_x
        
        # Draw HUD
        self.draw_hud(surface)
    
    def draw_hud(self, surface):
        """Draw heads-up display"""
        font_small = pygame.font.Font(None, 32)
        
        # HUD background
        hud_bg = pygame.Surface((400, 140))
        hud_bg.set_alpha(200)
        hud_bg.fill((0, 0, 0))
        surface.blit(hud_bg, (10, 10))
        
        # Score
        score_text = font_small.render(f"Score: {self.player.score}", True, (255, 255, 0))
        surface.blit(score_text, (20, 20))
        
        # Coins
        coins_text = font_small.render(f"Coins: {self.player.coins}/9", True, (255, 200, 0))
        surface.blit(coins_text, (20, 50))
        
        # Lives
        lives_text = font_small.render(f"Lives: {self.player.lives}", True, (255, 0, 0))
        surface.blit(lives_text, (20, 80))
        
        # Power-up status
        powerup_text = "Power: "
        powerup_color = (100, 100, 100)
        if self.player.is_powered_up and self.player.powerup_timer > 0:
            powerup_text += "MUSHROOM"
            powerup_color = (255, 100, 0)
        elif self.player.invincible_timer > 0:
            powerup_text += "STAR"
            powerup_color = (255, 255, 0)
        elif self.player.shield_timer > 0:
            powerup_text += "SHIELD"
            powerup_color = (100, 150, 255)
        else:
            powerup_text += "NONE"
        
        power_text = font_small.render(powerup_text, True, powerup_color)
        surface.blit(power_text, (220, 20))
        
        # Level progress
        progress_text = font_small.render(f"X: {int(self.player.x)}/2000", True, (150, 255, 150))
        surface.blit(progress_text, (220, 50))
        
        # Game over
        if self.game_over:
            font_large = pygame.font.Font(None, 72)
            game_over_text = font_large.render("GAME OVER", True, RED)
            surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 300))
        
        # Win
        if self.won:
            font_large = pygame.font.Font(None, 72)
            win_text = font_large.render("YOU WIN!", True, GREEN)
            surface.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, 300))
