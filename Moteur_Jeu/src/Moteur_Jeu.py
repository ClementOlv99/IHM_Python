#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Moteur_Jeu - Snake Game Engine
#
#  Created by Ingenuity i/o on 2026/01/30
#
#  Copyright © 2025 Ingenuity i/o. All rights reserved.
#
import ingescape as igs
import json
import time


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Moteur_Jeu(metaclass=Singleton):
    """
    Snake game engine implementing core game logic.
    
    Receives:
        - DirectionI: Integer (0=UP, 1=RIGHT, 2=DOWN, 3=LEFT)
        - PauseI: Boolean (pause state)
        - LevelI: JSON bytes (level layout and configuration)
    
    Sends:
        - DisplayO: JSON bytes (game state for renderer)
        - New_LevelO: Impulsion (request new level)
        - Game_OverO: Impulsion (game over signal)
    """
    
    # Tile type constants
    TILE_FLOOR = 0
    TILE_WALL = 1
    TILE_ENTRY = 2
    TILE_EXIT = 3
    TILE_APPLE = 4
    TILE_TRAP_APPLE = 5
    
    # Direction constants (matching input detector)
    DIR_UP = 0
    DIR_RIGHT = 1
    DIR_DOWN = 2
    DIR_LEFT = 3
    
    # Direction vectors (x, y) for movement
    DIRECTION_VECTORS = {
        DIR_UP: (0, -1),
        DIR_RIGHT: (1, 0),
        DIR_DOWN: (0, 1),
        DIR_LEFT: (-1, 0)
    }
    
    def __init__(self):
        # Ingescape inputs
        self.DirectionI = None
        self.PauseI = None
        self.LevelI = None
        
        # Ingescape outputs
        self._DisplayO = None
        
        # Game state
        self.snake_body = []           # List of (x, y) tuples, head at index 0
        self.current_direction = self.DIR_RIGHT
        self.pending_direction = None  # Buffered direction change
        self.score = 0
        self.level_number = 1
        self.snake_length = 3
        self.growth_pending = 0        # Segments queued to add
        self.paused = False
        self.game_over = False
        self.level_complete = False
        
        # Level data
        self.layout = []               # Immutable base layout
        self.current_layout = []       # Working copy (items removed when eaten)
        self.cycle_duration = 0.2      # Seconds per game tick
        self.last_cycle_time = 0.0
        
        # Special positions
        self.entry_position = None     # (x, y) spawn point
        self.exit_position = None      # (x, y) level exit
        
        igs.info("Moteur_Jeu initialized - ready to receive level data")
    
    # Ingescape outputs
    @property
    def DisplayO(self):
        return self._DisplayO
    
    @DisplayO.setter
    def DisplayO(self, value):
        self._DisplayO = value
        if self._DisplayO is not None:
            igs.output_set_data("display", value)
    
    def set_New_LevelO(self):
        """Request a new level from the supervisor."""
        igs.output_set_impulsion("new_level")
    
    def set_Game_OverO(self):
        """Signal game over to other agents."""
        igs.output_set_impulsion("game_over")
    
    # Level Management
    
    def initialize_level(self, level_data):
        """
        Initialize a new level from received data.
        
        Args:
            level_data (dict): {
                "layout": [[tile, ...], ...],  # 2D array with items included
                "cycle_duration": float
            }
        
        Layout tiles: 0=floor, 1=wall, 2=entry, 3=exit, 4=apple, 5=trap
        """
        try:
            # Store base layout
            self.layout = level_data["layout"]
            self.cycle_duration = level_data.get("cycle_duration", 0.2)
            
            # Create working copy (will be modified as items are eaten)
            self.current_layout = [row[:] for row in self.layout]
            
            # Scan for special tiles
            self.entry_position = None
            self.exit_position = None
            
            height = len(self.layout)
            width = len(self.layout[0]) if height > 0 else 0
            
            for y in range(height):
                for x in range(width):
                    tile = self.layout[y][x]
                    if tile == self.TILE_ENTRY:
                        self.entry_position = (x, y)
                    elif tile == self.TILE_EXIT:
                        self.exit_position = (x, y)
            
            # Initialize snake at entry position
            if self.entry_position:
                x, y = self.entry_position
                # Place snake with head at entry, trailing to the left
                self.snake_body = [(x, y), (x - 1, y), (x - 2, y)]
                self.snake_length = 3
                self.current_direction = self.DIR_RIGHT
                self.pending_direction = None
            else:
                igs.error("Level has no entry point (tile 2)!")
                self.snake_body = []
            
            # Reset game state
            self.score = 0
            self.growth_pending = 0
            self.paused = False
            self.game_over = False
            self.level_complete = False
            self.last_cycle_time = time.time()
            
            igs.info(f"Level initialized: {width}x{height}, spawn at {self.entry_position}")
            
            # Send initial state to renderer
            self.send_display_update()
            
        except Exception as e:
            igs.error(f"Failed to initialize level: {e}")
            import traceback
            igs.error(traceback.format_exc())
    
    # Input Handling
    
    def set_pending_direction(self, new_direction):
        """
        Buffer a direction change (applied next cycle).
        Prevents invalid 180-degree turns.
        
        Args:
            new_direction (int): DIR_UP, DIR_RIGHT, DIR_DOWN, or DIR_LEFT
        """
        if new_direction not in [self.DIR_UP, self.DIR_RIGHT, self.DIR_DOWN, self.DIR_LEFT]:
            return
        
        # Check if trying to reverse direction (invalid)
        opposite_dirs = {
            self.DIR_UP: self.DIR_DOWN,
            self.DIR_DOWN: self.DIR_UP,
            self.DIR_LEFT: self.DIR_RIGHT,
            self.DIR_RIGHT: self.DIR_LEFT
        }
        
        if new_direction != opposite_dirs[self.current_direction]:
            self.pending_direction = new_direction
    
    # Game Loop
    
    def game_cycle(self):
        """
        Main game tick - called every cycle_duration seconds.
        Handles snake movement, collision detection, and item collection.
        """
        # Skip if paused, game over, or level complete
        if self.paused or self.game_over or self.level_complete:
            return
        
        # Skip if no snake (invalid level)
        if not self.snake_body:
            return
        
        # 1. Apply pending direction change
        if self.pending_direction is not None:
            self.current_direction = self.pending_direction
            self.pending_direction = None
        
        # 2. Calculate new head position
        head_x, head_y = self.snake_body[0]
        dx, dy = self.DIRECTION_VECTORS[self.current_direction]
        new_head = (head_x + dx, head_y + dy)
        
        # 3. Check self collision
        if new_head in self.snake_body:
            self.trigger_game_over("Collision with self")
            return
        
        new_x, new_y = new_head
        
        # 4. Boundary check
        height = len(self.current_layout)
        width = len(self.current_layout[0]) if height > 0 else 0
        
        if new_y < 0 or new_y >= height or new_x < 0 or new_x >= width:
            self.trigger_game_over("Out of bounds")
            return
        
        # 5. Get tile at new position
        tile = self.current_layout[new_y][new_x]
        
        # 6. Handle tile interactions
        if tile == self.TILE_WALL:
            self.trigger_game_over("Hit wall")
            return
        
        elif tile == self.TILE_EXIT:
            self.trigger_level_complete()
            return
        
        elif tile == self.TILE_APPLE:
            # Regular apple: grow + score
            self.score += 10
            self.growth_pending += 1
            # Replace apple with floor in working layout
            self.current_layout[new_y][new_x] = self.TILE_FLOOR
            igs.info(f"Apple eaten! Score: {self.score}")
        
        elif tile == self.TILE_TRAP_APPLE:
            # Trap apple: grow but no score
            self.growth_pending += 1
            # Replace trap with floor
            self.current_layout[new_y][new_x] = self.TILE_FLOOR
            igs.info("Trap apple eaten (no score)")
        
        # 7. Move snake - add new head
        self.snake_body.insert(0, new_head)
        
        # 8. Handle growth or remove tail
        if self.growth_pending > 0:
            self.growth_pending -= 1
            self.snake_length += 1
            # Keep tail (don't pop)
        else:
            # Remove tail segment
            self.snake_body.pop()
        
        # 9. Send updated state to renderer
        self.send_display_update()
    
    # Game Events
    
    def trigger_game_over(self, reason):
        """
        Handle game over state.
        
        Args:
            reason (str): Cause of game over
        """
        self.game_over = True
        igs.warn(f"🔴 GAME OVER: {reason} | Score: {self.score} | Length: {self.snake_length}")
        
        # Send impulse to other agents
        self.set_Game_OverO()
        
        # Send final display state
        self.send_display_update()
    
    def trigger_level_complete(self):
        """Handle level completion."""
        self.level_complete = True
        igs.info(f"🎉 Level {self.level_number} complete! Score: {self.score}")
        
        self.level_number += 1
        
        # Request new level from supervisor
        self.set_New_LevelO()
        
        # Send completion state to display
        self.send_display_update()
    
    # Output Formatting
    
    def send_display_update(self):
        """
        Send current game state to renderer.
        
        Output format:
        {
            "snake": [[x, y], ...],           # Head at index 0
            "layout": [[tile, ...], ...],     # Current layout (items removed)
            "paused": bool,
            "game_state": {
                "score": int,
                "level": int,
                "cycle_duration": float,
                "length": int
            }
        }
        """
        try:
            display_data = {
                "snake": [[x, y] for x, y in self.snake_body],
                "layout": self.current_layout,
                "paused": self.paused,
                "game_state": {
                    "score": self.score,
                    "level": self.level_number,
                    "cycle_duration": self.cycle_duration,
                    "length": self.snake_length
                }
            }
            
            # Convert to bytes for DATA output
            self.DisplayO = json.dumps(display_data).encode()
            
        except Exception as e:
            igs.error(f"Failed to send display update: {e}")



