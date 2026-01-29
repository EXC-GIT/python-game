import pygame
import sys
from game_manager import GameManager
from utils.constants import FPS


def main():
    pygame.init()
    
    # Create game manager
    game_manager = GameManager()
    
    # Game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and game_manager.state != 5:  # Not in Mario
                    running = False
        
        # Update game state
        game_manager.update()
        
        # Draw everything
        game_manager.draw()
        
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

