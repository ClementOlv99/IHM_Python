# Godot Rendererer for S.N.A.K.E

The renderer receives HTTP input from the main engine through Ingescape, and uses the inputs to render the game scene.

## Project Overview

This is a **Godot 4.5 renderer** for the S.N.A.K.E game, designed to receive HTTP commands from an external game engine via Ingescape and render the game state in real-time. This is **NOT** a standalone game - it's a visualization client in a distributed architecture.

**Key Architecture Pattern**: HTTP-driven renderer  
- External engine sends game state via HTTP → Godot HTTP server processes → Renderer updates visuals
- Main logic is in the game engine, NOT here. This project only handles visualization.

## Project Structure

- [scripts/main.gd](scripts/main.gd) - Root node that coordinates HTTP server and rendering layers
- [scripts/snake_layer.gd](scripts/snake_layer.gd) - Manages snake rendering, camera, and movement visualization
- `addons/godottpd/` - Third-party HTTP server plugin ([bit-garden/godottpd](https://github.com/bit-garden/godottpd))
- Scene files: [main.tscn](main.tscn) (root), [snake.tscn](snake.tscn) (snake layer)

## Critical Patterns

### 1. HTTP Server Integration
The HttpServer node (from godottpd addon) runs on port 8080. Register routers in [main.gd](scripts/main.gd):
```gdscript
@onready var server : HttpServer = $HttpServer
server.port = 5670
# Add routers via server.register_router() to handle game state updates
```

### 2. Cycle-Based Rendering
Snake movement uses a timer-based cycle system, NOT physics:
```gdscript
# In snake_layer.gd
cycle_duration : float = 0.2  # Game tick duration
cycle_timer.timeout.connect(cycle)  # Called every cycle
```
When adding features, respect the cycle timing - don't use `_process()` for game logic.

### 3. Grid Coordinates
Everything uses 64-pixel tile grid. Position conversions:
```gdscript
head_grid_pos : Vector2i  # Grid coordinates (0,0), (1,0), etc.
world_pos = head_grid_pos * 64 + Vector2i(32, 32)  # Center of tile
```

### 4. Layer Architecture
Three TileMapLayer nodes for rendering (see [main.tscn](main.tscn)):
- `BaseLayer` - Static background/walls
- `SnakeLayer` - Snake body and head (custom class)
- `ItemLayer` - Food/items

## Development Workflows

### Running the Project
Open in **Godot 4.5+** editor and press F5. The HTTP server starts automatically on port 8080.
There's no CLI build command in this project - use Godot's export features for deployment.

### Testing HTTP Integration
Currently uses keyboard input for testing (`ui_left/right/up/down` actions in [snake_layer.gd](scripts/snake_layer.gd#L51-L60)).  
Production: Remove `_input()` method and implement HTTP endpoints to receive direction commands.

### Debugging
- Check [project.godot](project.godot#L22) - rendering method is "mobile" (lightweight)
- Camera follows `head_grid_pos` automatically (see [snake_layer.gd](scripts/snake_layer.gd#L44))
- HTTP server logs available if enabled: `HttpServer.new(true)` for logging mode

## Key Conventions

- **GDScript 2.0 style**: Use type hints (`var x : int = 5`), `@onready`, `@export`
- **Scene-based architecture**: Main logic in scene tree, minimal global state
- **Custom classes**: Use `class_name SnakeLayer` for reusable node types
- **Grid-first design**: All positions in grid coordinates, convert to pixels for rendering only

## External Dependencies

- **godottpd addon**: HTTP server functionality - API docs at https://github.com/bit-garden/godottpd/tree/dc7b9f45efebc48c3588980926752a7a7d8c5e8d/docs/api
- **Ingescape**: External integration platform (referenced above) - communication layer not yet implemented

## What's Missing (Future Work)

- HTTP endpoints for receiving game state from external engine
- Proper snake body segment rendering (currently only head with TestSprite)
- Food/item spawning logic
- Wall collision detection
- Score/UI overlay

