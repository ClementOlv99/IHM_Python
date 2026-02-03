extends Node2D

@onready var snakeLayer : SnakeLayer = $SnakeLayer
@onready var itemLayer : ItemLayer = $ItemLayer
@onready var baseLayer : BaseLayer = $BaseLayer

@onready var server : HttpServer = $HttpServer

@export var cycle_duration : float = 1

# Game state tracking
var current_score : int = 0
var current_level : int = 1
var current_length : int = 3
var is_paused : bool = false

func _ready() -> void:
	print("Initializing S.N.A.K.E Renderer...")
	
	# Configure HTTP server port (matches Affichage.py)
	server.port = 5671
	
	# Initialize snake layer
	snakeLayer.initialise()

	# Create and register the game data router
	var game_router = GameDataRouter.new("/game_data")
	game_router.data_received.connect(_on_game_data_received)
	server.register_router(game_router)
	
	# Start the HTTP server (CRITICAL - without this, port is not bound!)
	server.start()
	
	print("S.N.A.K.E Renderer initialized")
	print("Ready to receive game data on port 5671")

# Main data handler - called when game state is received
func _on_game_data_received(data: Dictionary) -> void:
	# The data is already parsed as a dictionary from GameDataRouter
	
	# Update snake positions
	if data.has("snake"):
		snake_array_changed(data["snake"])
	
	# Update level layout
	if data.has("layout"):
		layout_changed(data["layout"])
		items_changed(data["layout"])
	
	# Update game timing
	if data.has("cycle_duration"):
		cycle_duration_changed(data["cycle_duration"])
	
	# Update game state (score, level, etc.)
	if data.has("game_state"):
		game_state_changed(data["game_state"])
	
	# Update pause state
	if data.has("paused"):
		is_paused = data["paused"]

# Individual update functions

func cycle_duration_changed(new_duration: float) -> void:
	cycle_duration = new_duration
	snakeLayer.cycle_duration = new_duration

func snake_array_changed(new_snake_array: Array) -> void:
	# Convert Array to Array[Vector2i]
	var typed_array : Array[Vector2i] = []
	for pos in new_snake_array:
		if pos is Array and pos.size() >= 2:
			typed_array.append(Vector2i(pos[0], pos[1]))
	
	snakeLayer.snake_array = typed_array

func layout_changed(new_layout: Array[Array]) -> void:
	baseLayer.change_layout(new_layout)

func items_changed(new_layout: Array[Array]) -> void:
	itemLayer.change_layout(new_layout)

func game_state_changed(game_state: Dictionary) -> void:
	"""
	Update game state display.
	game_state contains: {score, level, cycle_duration, length}
	"""
	if game_state.has("score"):
		current_score = game_state["score"]
	
	if game_state.has("level"):
		current_level = game_state["level"]
	
	if game_state.has("length"):
		current_length = game_state["length"]
	
	# Log state changes for debugging
	print("Score: %d | Level: %d | Length: %d" % [current_score, current_level, current_length])

