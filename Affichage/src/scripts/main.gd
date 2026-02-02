extends Node2D

@onready var snakeLayer : SnakeLayer = $SnakeLayer
@onready var itemLayer : TileMapLayer = $ItemLayer
@onready var baseLayer : TileMapLayer = $BaseLayer

@onready var server : HttpServer = $HttpServer

@export var cycle_duration : float = 1

func _ready() -> void:
	# Server setup
	server.port = 5670

	# On iniitialise le snake
	snakeLayer.initialise()


# Gestion des inputs HTTP - fonctions appelées par le serveur HTTP

func cycle_duration_changed(new_duration: float) -> void:
	cycle_duration = new_duration
	snakeLayer.cycle_duration = new_duration

func snake_array_changed(new_snake_array: Array[Vector2i]) -> void:
	snakeLayer.snake_array = new_snake_array

func layout_changed(new_layout: Array[Array]) -> void:
	baseLayer.change_layout(new_layout)

func items_changed(new_items: Array[Array]) -> void:
	itemLayer.change_items(new_items)
