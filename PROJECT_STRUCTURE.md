# Project Structure

## Overview
This is a modularized game collection platform written in Python using Pygame. The code is organized into separate modules by functionality and game type, making it easy to maintain and extend.

## Directory Structure

```
kof/
├── __init__.py          # KOF module initialization
├── character.py         # Character class for KOF fighting
└── game.py              # KOFGame class for managing fights

mario/
├── __init__.py          # Mario module initialization
├── game.py              # MarioGame class (main game logic)
├── player.py            # MarioPlayer class (Mario character)
├── enemies.py           # Enemy class (Goombas)
├── platforms.py         # Platform class (level platforms)
└── items.py             # Coin class (collectible items)

ui/
├── __init__.py          # UI module initialization
└── menu.py              # MenuManager class (all menu screens)

utils/
├── __init__.py          # Utils module initialization
├── constants.py         # All game constants
└── particle.py          # Particle class (visual effects)

Main Files:
├── main.py              # Entry point for the application
└── game_manager.py      # GameManager class (orchestrates all games)
```

## Module Descriptions

### `kof/` - King of Fighters Game Module
Handles all KOF fighting game logic.

**Key Classes:**
- `Character`: Fighter with health, energy, attacks, combos, and blocking
- `KOFGame`: Manages fight state, collision detection, and rendering

**Features:**
- 4 playable characters (Kyo, Iori, Mai, Ryo)
- Punch, kick, and special attacks
- Blocking system
- Combo damage multiplier
- Particle effects on hit

### `mario/` - Super Mario Game Module
Handles all Mario platformer logic, separated into focused submodules.

**Key Classes:**
- `MarioGame`: Main game controller and level manager
- `MarioPlayer`: Mario character with jump and movement
- `Enemy`: Goomba enemies with basic AI
- `Platform`: Static platforms with different types (normal, coin, spike)
- `Coin`: Collectible items with bobbing animation

**Features:**
- Level design with multiple platform types
- Enemy patrolling and jumping on mechanics
- Coin collection with win condition
- Lives system
- Invincibility frames after damage

### `ui/` - User Interface Module
Centralized UI management for all menus and screens.

**Key Classes:**
- `MenuManager`: Handles all menu rendering (main menu, character select, game over)

**Menus:**
- Main game selection menu
- KOF character selection (dual player)
- KOF game over screen

### `utils/` - Utilities Module
Shared utilities and constants used across the project.

**Key Classes:**
- `Particle`: Visual particle effects with physics

**Constants:**
- Screen dimensions (1280x720)
- Game states (Main Menu, Character Select, Fighting, Mario, etc.)
- Colors for UI and rendering
- Physics values (gravity, jump strength)
- Combat values (damage amounts, ranges)

### `game_manager.py` - Central Game Manager
Orchestrates all games and state transitions.

**Responsibilities:**
- Game state management
- Input handling for all game modes
- Rendering orchestration
- State transitions between games

## Design Patterns

### Separation of Concerns
- Each game (KOF, Mario) is isolated in its own module
- UI logic is separated from game logic
- Constants and utilities are centralized

### Module Hierarchy
```
GameManager (main orchestrator)
├── MenuManager (UI rendering)
├── KOFGame (game logic)
│   └── Character
├── MarioGame (game logic)
│   ├── MarioPlayer
│   ├── Enemy
│   ├── Platform
│   └── Coin
└── Shared: Constants, Particles
```

## Adding a New Game

To add a new game (e.g., "Pac-Man"):

1. Create `pacman/` directory with submodules:
   ```
   pacman/
   ├── __init__.py
   ├── game.py
   ├── player.py
   ├── enemies.py
   └── levels.py
   ```

2. Create a main game class: `class PacManGame:`

3. Update `game_manager.py`:
   ```python
   # Add to available_games list
   self.available_games = ["King of Fighters", "Super Mario", "Pac-Man"]
   
   # Add to handle_main_menu
   elif self.selected_game == 2:
       self.pacman_game = PacManGame()
       self.state = GAME_STATE_PACMAN
   
   # Add state handling in handle_mario section
   elif self.state == GAME_STATE_PACMAN:
       self.handle_pacman()
   ```

4. Add game state constant to `utils/constants.py`:
   ```python
   GAME_STATE_PACMAN = 6
   ```

5. Implement `handle_pacman()` and drawing logic in `game_manager.py`

## Code Organization Benefits

1. **Maintainability**: Changes to one game don't affect others
2. **Scalability**: Easy to add new games without modifying core logic
3. **Testability**: Each module can be tested independently
4. **Readability**: Clear separation between different game systems
5. **Reusability**: Shared utilities can be used by all games

## Dependencies

- `pygame-ce` (pygame community edition) - Game framework
- Python 3.8+

## Running the Game

```bash
python main.py
```

The game will start with the main menu where you can select between available games.
