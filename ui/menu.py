import pygame
from utils.constants import *


class MenuManager:
    """Manages main menu and character selection"""
    def __init__(self):
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
    
    def draw_main_menu(self, surface, selected_game, available_games):
        """Draw main menu with game selection"""
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(30 + (100 - 30) * color_ratio)
            g = int(10 + (60 - 10) * color_ratio)
            b = int(60 + (150 - 60) * color_ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Main title
        title_box = pygame.Surface((800, 180))
        title_box.set_alpha(230)
        title_box.fill((0, 0, 30))
        surface.blit(title_box, (SCREEN_WIDTH // 2 - 400, 40))
        pygame.draw.rect(surface, (100, 150, 255), (SCREEN_WIDTH // 2 - 400, 40, 800, 180), 3)
        
        title = self.font_large.render("GAME COLLECTION", True, (100, 200, 255))
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 70))
        
        subtitle = self.font_medium.render("SELECT A GAME", True, (200, 220, 255))
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 160))
        
        # Game selection area
        selection_start_y = 320
        game_spacing = 120
        
        for i, game in enumerate(available_games):
            y = selection_start_y + i * game_spacing
            box_width = 500
            box_height = 100
            box_x = SCREEN_WIDTH // 2 - box_width // 2
            
            # Game box
            box = pygame.Surface((box_width, box_height))
            
            if i == selected_game:
                # Highlight selected game
                box.set_alpha(240)
                box.fill((30, 60, 100))
                surface.blit(box, (box_x, y))
                pygame.draw.rect(surface, (100, 200, 255), (box_x, y, box_width, box_height), 4)
                pygame.draw.rect(surface, (150, 220, 255), (box_x - 5, y - 5, box_width + 10, box_height + 10), 2)
                
                # Glow effect
                for glow in range(3):
                    pygame.draw.rect(surface, (100 - glow * 20, 200 - glow * 30, 255 - glow * 30),
                                   (box_x - 10 - glow, y - 10 - glow, box_width + 20 + glow * 2, box_height + 20 + glow * 2), 1)
                
                game_text = self.font_medium.render(game, True, (100, 200, 255))
            else:
                box.set_alpha(180)
                box.fill((20, 40, 60))
                surface.blit(box, (box_x, y))
                pygame.draw.rect(surface, (80, 120, 180), (box_x, y, box_width, box_height), 2)
                
                game_text = self.font_medium.render(game, True, (150, 180, 220))
            
            surface.blit(game_text, (SCREEN_WIDTH // 2 - game_text.get_width() // 2, y + 35))
        
        # Instructions
        info_box = pygame.Surface((600, 60))
        info_box.set_alpha(220)
        info_box.fill((0, 0, 20))
        surface.blit(info_box, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 90))
        pygame.draw.rect(surface, (100, 150, 255), (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 90, 600, 60), 2)
        
        keys_text = self.font_small.render("UP/DOWN to select | ENTER to play", True, (100, 200, 255))
        surface.blit(keys_text, (SCREEN_WIDTH // 2 - keys_text.get_width() // 2, SCREEN_HEIGHT - 75))
    
    def draw_character_select(self, surface, selected_char_p1, selected_char_p2, available_chars):
        """Draw character selection screen with better graphics"""
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(20 + (80 - 20) * color_ratio)
            g = int(10 + (40 - 10) * color_ratio)
            b = int(40 + (100 - 40) * color_ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Title box
        title_box = pygame.Surface((600, 140))
        title_box.set_alpha(220)
        title_box.fill((0, 0, 0))
        surface.blit(title_box, (SCREEN_WIDTH // 2 - 300, 30))
        
        title = self.font_large.render("KING OF FIGHTERS", True, (255, 200, 0))
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 50))
        
        subtitle = self.font_medium.render("SELECT YOUR CHARACTER", True, (200, 200, 255))
        surface.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 120))
        
        # Player 1
        p1_label = pygame.Surface((160, 40))
        p1_label.set_alpha(200)
        p1_label.fill((0, 0, 80))
        surface.blit(p1_label, (20, 220))
        
        p1_text = self.font_small.render("PLAYER 1", True, (100, 200, 255))
        surface.blit(p1_text, (30, 230))
        
        for i, char in enumerate(available_chars):
            x = 80 + i * 250
            y = 300
            
            # Character box
            box_width = 180
            box_height = 120
            box_rect = pygame.Rect(x - box_width // 2, y, box_width, box_height)
            
            if i == selected_char_p1:
                pygame.draw.rect(surface, (100, 200, 255), box_rect, 4)
                pygame.draw.rect(surface, (200, 255, 255), box_rect, 1)
                glow_rect = pygame.Rect(x - box_width // 2 - 5, y - 5, box_width + 10, box_height + 10)
                pygame.draw.rect(surface, (100, 200, 255), glow_rect, 1)
                text_color = (100, 200, 255)
            else:
                pygame.draw.rect(surface, (80, 80, 100), box_rect, 2)
                text_color = WHITE
            
            # Character name
            char_text = self.font_small.render(char, True, text_color)
            surface.blit(char_text, (x - char_text.get_width() // 2, y + 45))
        
        # Player 2
        p2_label = pygame.Surface((160, 40))
        p2_label.set_alpha(200)
        p2_label.fill((80, 0, 0))
        surface.blit(p2_label, (SCREEN_WIDTH - 180, 220))
        
        p2_text = self.font_small.render("PLAYER 2", True, (255, 100, 100))
        surface.blit(p2_text, (SCREEN_WIDTH - 170, 230))
        
        for i, char in enumerate(available_chars):
            x = 80 + i * 250
            y = 480
            
            # Character box
            box_width = 180
            box_height = 120
            box_rect = pygame.Rect(x - box_width // 2, y, box_width, box_height)
            
            if i == selected_char_p2:
                pygame.draw.rect(surface, (255, 100, 100), box_rect, 4)
                pygame.draw.rect(surface, (255, 200, 200), box_rect, 1)
                glow_rect = pygame.Rect(x - box_width // 2 - 5, y - 5, box_width + 10, box_height + 10)
                pygame.draw.rect(surface, (255, 100, 100), glow_rect, 1)
                text_color = (255, 100, 100)
            else:
                pygame.draw.rect(surface, (100, 80, 80), box_rect, 2)
                text_color = WHITE
            
            # Character name
            char_text = self.font_small.render(char, True, text_color)
            surface.blit(char_text, (x - char_text.get_width() // 2, y + 45))
        
        # Instructions
        info_box = pygame.Surface((600, 50))
        info_box.set_alpha(200)
        info_box.fill((0, 0, 0))
        surface.blit(info_box, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 70))
        
        info = self.font_small.render("Press ENTER to fight!", True, (0, 255, 0))
        surface.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, SCREEN_HEIGHT - 60))
    
    def draw_game_over(self, surface, winner_name):
        """Draw game over screen"""
        # Gradient background
        for y in range(SCREEN_HEIGHT):
            color_ratio = y / SCREEN_HEIGHT
            r = int(30 * color_ratio)
            g = int(0)
            b = int(40 * color_ratio)
            pygame.draw.line(surface, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Game over box
        box_width = 600
        box_height = 300
        box_x = SCREEN_WIDTH // 2 - box_width // 2
        box_y = SCREEN_HEIGHT // 2 - box_height // 2
        
        box = pygame.Surface((box_width, box_height))
        box.set_alpha(230)
        box.fill((20, 0, 40))
        surface.blit(box, (box_x, box_y))
        pygame.draw.rect(surface, (255, 100, 0), (box_x, box_y, box_width, box_height), 3)
        
        title = self.font_large.render("GAME OVER", True, RED)
        surface.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, box_y + 40))
        
        winner = self.font_medium.render(f"{winner_name} WINS!", True, (0, 255, 0))
        surface.blit(winner, (SCREEN_WIDTH // 2 - winner.get_width() // 2, box_y + 130))
        
        info = self.font_small.render("Press ENTER to continue", True, (200, 200, 255))
        surface.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, box_y + 220))
