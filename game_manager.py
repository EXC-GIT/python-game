"""Main game manager that orchestrates all games"""
import pygame
from utils.constants import *
from kof.game import KOFGame
from mario.game import MarioGame
from ui.menu import MenuManager


class GameManager:
    """Central game manager"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Game Collection")
        
        self.state = GAME_STATE_MAIN_MENU
        self.menu = MenuManager()
        
        # Menu state
        self.selected_game = 0
        self.available_games = ["King of Fighters", "Super Mario"]
        
        # KOF state
        self.selected_char_p1 = 0
        self.selected_char_p2 = 0
        self.available_chars = ["Kyo", "Iori", "Mai", "Ryo"]
        self.kof_game = None
        self.game_over_winner = None
        
        # Mario state
        self.mario_game = None
    
    def handle_main_menu(self):
        """Handle main menu navigation"""
        keys = pygame.key.get_pressed()
        
        # Game selection
        if keys[pygame.K_UP] and self.selected_game > 0:
            self.selected_game -= 1
            pygame.time.wait(150)
        if keys[pygame.K_DOWN] and self.selected_game < len(self.available_games) - 1:
            self.selected_game += 1
            pygame.time.wait(150)
        
        # Start selected game
        if keys[pygame.K_RETURN]:
            if self.selected_game == 0:  # King of Fighters
                self.state = GAME_STATE_CHARACTER_SELECT
            elif self.selected_game == 1:  # Super Mario
                self.mario_game = MarioGame()
                self.state = GAME_STATE_MARIO
            pygame.time.wait(200)
    
    def handle_character_select(self):
        """Handle character selection"""
        keys = pygame.key.get_pressed()
        
        # Player 1 selection
        if keys[pygame.K_a] and self.selected_char_p1 > 0:
            self.selected_char_p1 -= 1
            pygame.time.wait(150)
        if keys[pygame.K_d] and self.selected_char_p1 < len(self.available_chars) - 1:
            self.selected_char_p1 += 1
            pygame.time.wait(150)
        
        # Player 2 selection
        if keys[pygame.K_LEFT] and self.selected_char_p2 > 0:
            self.selected_char_p2 -= 1
            pygame.time.wait(150)
        if keys[pygame.K_RIGHT] and self.selected_char_p2 < len(self.available_chars) - 1:
            self.selected_char_p2 += 1
            pygame.time.wait(150)
        
        # Start game
        if keys[pygame.K_RETURN]:
            self.start_kof_fight()
            pygame.time.wait(200)
    
    def start_kof_fight(self):
        """Initialize KOF fight"""
        self.kof_game = KOFGame()
        char1 = self.available_chars[self.selected_char_p1]
        char2 = self.available_chars[self.selected_char_p2]
        self.kof_game.start_fight(char1, char2)
        self.state = GAME_STATE_FIGHTING
    
    def handle_fighting(self):
        """Handle KOF gameplay"""
        keys = pygame.key.get_pressed()
        
        self.kof_game.handle_input(keys)
        self.kof_game.update()
        
        # Check win condition
        if self.kof_game.player1.health <= 0:
            self.game_over_winner = self.kof_game.player2.name
            self.state = GAME_STATE_GAME_OVER
        elif self.kof_game.player2.health <= 0:
            self.game_over_winner = self.kof_game.player1.name
            self.state = GAME_STATE_GAME_OVER
    
    def handle_game_over(self):
        """Handle KOF game over"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.state = GAME_STATE_CHARACTER_SELECT
            pygame.time.wait(200)
    
    def handle_mario(self):
        """Handle Mario gameplay"""
        keys = pygame.key.get_pressed()
        
        self.mario_game.handle_input(keys)
        self.mario_game.update()
        
        # Return to menu
        if keys[pygame.K_ESCAPE]:
            self.state = GAME_STATE_MAIN_MENU
            pygame.time.wait(200)
        
        # Restart on game over or win
        if self.mario_game.game_over or self.mario_game.won:
            if keys[pygame.K_RETURN]:
                self.mario_game = MarioGame()
                pygame.time.wait(200)
            elif keys[pygame.K_ESCAPE]:
                self.state = GAME_STATE_MAIN_MENU
                pygame.time.wait(200)
    
    def update(self):
        """Update game state"""
        if self.state == GAME_STATE_MAIN_MENU:
            self.handle_main_menu()
        elif self.state == GAME_STATE_CHARACTER_SELECT:
            self.handle_character_select()
        elif self.state == GAME_STATE_FIGHTING:
            self.handle_fighting()
        elif self.state == GAME_STATE_GAME_OVER:
            self.handle_game_over()
        elif self.state == GAME_STATE_MARIO:
            self.handle_mario()
    
    def draw(self):
        """Draw current game state"""
        if self.state == GAME_STATE_MAIN_MENU:
            self.menu.draw_main_menu(self.screen, self.selected_game, self.available_games)
        elif self.state == GAME_STATE_CHARACTER_SELECT:
            self.menu.draw_character_select(self.screen, self.selected_char_p1, 
                                           self.selected_char_p2, self.available_chars)
        elif self.state == GAME_STATE_FIGHTING:
            self.kof_game.draw(self.screen)
            # Draw HUD
            font_small = pygame.font.Font(None, 32)
            hud_bg = pygame.Surface((300, 100))
            hud_bg.set_alpha(200)
            hud_bg.fill((0, 0, 0))
            self.screen.blit(hud_bg, (10, 10))
            
            p1_name = font_small.render(f"{self.kof_game.player1.name}", True, (100, 200, 255))
            self.screen.blit(p1_name, (20, 20))
            
            p1_health = font_small.render(f"HP: {int(self.kof_game.player1.health)}", True, (0, 255, 0) if self.kof_game.player1.health > 30 else (255, 100, 0))
            self.screen.blit(p1_health, (20, 50))
            
            p1_energy = font_small.render(f"EN: {int(self.kof_game.player1.energy)}", True, (100, 150, 255))
            self.screen.blit(p1_energy, (20, 80))
            
            p2_hud_x = SCREEN_WIDTH - 170
            hud_bg2 = pygame.Surface((300, 100))
            hud_bg2.set_alpha(200)
            hud_bg2.fill((0, 0, 0))
            self.screen.blit(hud_bg2, (p2_hud_x, 10))
            
            p2_name = font_small.render(f"{self.kof_game.player2.name}", True, (255, 100, 100))
            self.screen.blit(p2_name, (p2_hud_x + 10, 20))
            
            p2_health = font_small.render(f"HP: {int(self.kof_game.player2.health)}", True, (0, 255, 0) if self.kof_game.player2.health > 30 else (255, 100, 0))
            self.screen.blit(p2_health, (p2_hud_x + 10, 50))
            
            p2_energy = font_small.render(f"EN: {int(self.kof_game.player2.energy)}", True, (100, 150, 255))
            self.screen.blit(p2_energy, (p2_hud_x + 10, 80))
        elif self.state == GAME_STATE_GAME_OVER:
            self.menu.draw_game_over(self.screen, self.game_over_winner)
        elif self.state == GAME_STATE_MARIO:
            self.mario_game.draw(self.screen)
            # Instructions
            font_small = pygame.font.Font(None, 24)
            info = font_small.render("ESC: Menu | ENTER: Restart (after game over)", True, WHITE)
            self.screen.blit(info, (10, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()
