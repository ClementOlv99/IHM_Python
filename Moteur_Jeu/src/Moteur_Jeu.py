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
    DIR_UP = 1
    DIR_RIGHT = 2
    DIR_DOWN = 3
    DIR_LEFT = 4
    
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
        self.cycle_duration = 1.0      # Seconds per game tick
        self.last_cycle_time = 0.0
        
        # Special positions
        self.entry_position = None     # (x, y) spawn point
        self.exit_position = None      # (x, y) level exit
        
        print("✅ Moteur_Jeu initialized - ready to receive level data")
    
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
            level_data (array): [[tile, ...], ...],  # 2D array with items included

        
        Layout tiles: 0=floor, 1=wall, 2=entry, 3=exit, 4=apple, 5=trap
        """
        try:
            print(f"🎮 Initializing level with data: {json.dumps(level_data)[:200]}...")
            
            # Extract layout array from level data (level data IS layout array)
            self.layout = level_data
            
            # Extract cycle duration if provided
            if "cycle_duration" in level_data:
                self.cycle_duration = level_data["cycle_duration"]
                print(f"⏱️  Cycle duration set to {self.cycle_duration}s")

            # Create working copy (will be modified as items are eaten)
            self.current_layout = [row[:] for row in self.layout]
            
            # Scan for special tiles
            self.entry_position = None
            self.exit_position = None
            
            height = len(self.layout)
            width = len(self.layout[0]) if height > 0 else 0
            
            print(f"📏 Level dimensions: {width}x{height}")
            
            for y in range(height):
                for x in range(width):
                    tile = self.layout[y][x]
                    if tile == self.TILE_ENTRY:
                        self.entry_position = (x, y)
                        print(f"🚪 Found entry at ({x}, {y})")
                    elif tile == self.TILE_EXIT:
                        self.exit_position = (x, y)
                        print(f"🏁 Found exit at ({x}, {y})")
            
            # Initialize snake at entry position
            if self.entry_position:
                x, y = self.entry_position
                
                # Determine safe direction to place snake tail based on available space
                # Try: right, left, down, up
                tail_offsets = [
                    [(0, 0), (-1, 0), (-2, 0)],  # Head, tail going left
                    [(0, 0), (1, 0), (2, 0)],    # Head, tail going right
                    [(0, 0), (0, -1), (0, -2)],  # Head, tail going up
                    [(0, 0), (0, 1), (0, 2)],    # Head, tail going down
                ]
                
                initial_directions = [self.DIR_RIGHT, self.DIR_LEFT, self.DIR_DOWN, self.DIR_UP]
                
                snake_placed = False
                for tail_pattern, direction in zip(tail_offsets, initial_directions):
                    # Check if all positions are valid
                    positions = [(x + dx, y + dy) for dx, dy in tail_pattern]
                    valid = True
                    
                    for px, py in positions:
                        if px < 0 or px >= width or py < 0 or py >= height:
                            valid = False
                            break
                        tile = self.layout[py][px]
                        if tile == self.TILE_WALL:
                            valid = False
                            break
                    
                    if valid:
                        self.snake_body = positions
                        self.current_direction = direction
                        snake_placed = True
                        print(f"🐍 Snake placed: {self.snake_body}, facing direction {direction}")
                        break
                
                if not snake_placed:
                    print("❌ Cannot place snake - no valid space near entry!")
                    self.snake_body = [(x, y)]  # At least place head
                    self.current_direction = self.DIR_RIGHT
                
                self.snake_length = len(self.snake_body)
                self.pending_direction = None
            else:
                print("❌ Level has no entry point (tile 2)!")
                self.snake_body = []
            
            # Reset game state
            self.score = 0
            self.growth_pending = 0
            self.paused = False
            self.game_over = False
            self.level_complete = False
            self.last_cycle_time = time.time()
            
            print(f"✅ Level initialized: {width}x{height}, snake at {self.entry_position}, length={self.snake_length}")
            print(f"🐍 Snake body: {self.snake_body}")
            
            # Send initial state to renderer
            self.send_display_update()
            
        except Exception as e:
            print(f"❌ Failed to initialize level: {e}")
            import traceback
            print(traceback.format_exc())
    
    # Input Handling
    
    def set_pending_direction(self, new_direction):
        """
        Buffer a direction change (applied next cycle).
        Prevents invalid 180-degree turns.
        
        Args:
            new_direction (int): DIR_UP, DIR_RIGHT, DIR_DOWN, or DIR_LEFT
        """
        print(f"🔄 set_pending_direction called with {new_direction}")
        
        if new_direction not in [self.DIR_UP, self.DIR_RIGHT, self.DIR_DOWN, self.DIR_LEFT]:
            print(f"❌ Invalid direction: {new_direction}")
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
            print(f"✅ Pending direction set to {new_direction}")
        else:
            print(f"❌ Cannot reverse direction: {new_direction} is opposite to {self.current_direction}")
    
    # Game Loop
    
    def game_cycle(self):
        """
        Main game tick - called every cycle_duration seconds.
        Handles snake movement, collision detection, and item collection.
        """
        # Skip if paused, game over, or level complete
        if self.paused:
            return
        if self.game_over:
            return
        if self.level_complete:
            return
        
        # Skip if no snake (invalid level)
        if not self.snake_body:
            print("⚠️  No snake body - level not initialized?")
            return
        
        print(f"🎮 Game cycle: snake at {self.snake_body[0]}, direction={self.current_direction}, pending={self.pending_direction}")
        
        # 1. Apply pending direction change
        if self.pending_direction is not None:
            old_direction = self.current_direction
            self.current_direction = self.pending_direction
            self.pending_direction = None
            print(f"➡️  Direction changed: {old_direction} → {self.current_direction}")
        
        # 2. Calculate new head position
        head_x, head_y = self.snake_body[0]
        dx, dy = self.DIRECTION_VECTORS[self.current_direction]
        new_head = (head_x + dx, head_y + dy)
        
        # 3. Check self collision
        if new_head in self.snake_body:
            # Add collision position to snake for visual feedback
            self.snake_body.insert(0, new_head)
            self.trigger_game_over("Collision with self")
            return
        
        new_x, new_y = new_head
        
        # 4. Boundary check
        height = len(self.current_layout)
        width = len(self.current_layout[0]) if height > 0 else 0
        
        if new_y < 0 or new_y >= height or new_x < 0 or new_x >= width:
            # Add out-of-bounds position to snake for visual feedback
            self.snake_body.insert(0, new_head)
            self.trigger_game_over("Out of bounds")
            return
        
        # 5. Get tile at new position
        tile = self.current_layout[new_y][new_x]
        
        # 6. Handle tile interactions
        if tile == self.TILE_WALL:
            # Add collision position to snake for visual feedback
            self.snake_body.insert(0, new_head)
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
            print(f"🍎 Apple eaten! Score: {self.score}")
        
        elif tile == self.TILE_TRAP_APPLE:
            # Trap apple: grow but no score
            self.growth_pending += 1
            # Replace trap with floor
            self.current_layout[new_y][new_x] = self.TILE_FLOOR
            print("💀 Trap apple eaten (no score)")
        
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
        print(f"🔴 GAME OVER: {reason} | Score: {self.score} | Length: {self.snake_length}")
        
        # Send impulse to other agents
        self.set_Game_OverO()
        
        # Send final display state
        self.send_display_update()
    
    def trigger_level_complete(self):
        """Handle level completion."""
        self.level_complete = True
        print(f"🎉 Level {self.level_number} complete! Score: {self.score}")
        
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
            snake_positions = [[x, y] for x, y in self.snake_body]
            
            display_data = {
                "snake": snake_positions,
                "layout": self.current_layout,
                "paused": self.paused,
                "game_state": {
                    "score": self.score,
                    "level": self.level_number,
                    "cycle_duration": self.cycle_duration,
                    "length": self.snake_length
                }
            }
            
            print(f"📡 Sending display update: snake={snake_positions[:3]}{'...' if len(snake_positions) > 3 else ''}, score={self.score}, length={self.snake_length}")
            
            # Convert to bytes for DATA output
            self.DisplayO = json.dumps(display_data).encode()
            
        except Exception as e:
            print(f"❌ Failed to send display update: {e}")



