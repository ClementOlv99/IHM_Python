extends Node2D

@onready var snakeLayer : SnakeLayer = $SnakeLayer
@onready var itemLayer : ItemLayer = $ItemLayer
@onready var baseLayer : BaseLayer = $BaseLayer

@onready var server : HttpServer = $HttpServer

@export var cycle_duration : float = 1

func _ready() -> void:
	# Server setup
	server.port = 5670

	# On iniitialise le snake
	snakeLayer.initialise()

	# Create and register the game data router
	var game_router = GameDataRouter.new()
	game_router.data_received.connect(_on_game_data_received)
	server.register_router(game_router)

# Handler function
func _on_game_data_received(data: Dictionary) -> void:
	# The data is already parsed as a dictionary
	if data.has("snake"):
		snake_array_changed(data["snake"])
	if data.has("layout"):
		layout_changed(data["layout"])
		items_changed(data["layout"])
	if data.has("cycle_duration"):
		cycle_duration_changed(data["cycle_duration"])


# Gestion des inputs HTTP - fonctions appelées par le serveur HTTP

func cycle_duration_changed(new_duration: float) -> void:
	cycle_duration = new_duration
	snakeLayer.cycle_duration = new_duration

func snake_array_changed(new_snake_array: Array[Vector2i]) -> void:
	snakeLayer.snake_array = new_snake_array

func layout_changed(new_layout: Array[Array]) -> void:
	baseLayer.change_layout(new_layout)

func items_changed(new_layout: Array[Array]) -> void:
	itemLayer.change_layout(new_layout)
