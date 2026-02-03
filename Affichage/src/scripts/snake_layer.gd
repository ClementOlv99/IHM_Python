extends Node2D
class_name SnakeLayer

var cycle_duration : float

@onready var camera : Camera2D = $Camera2D
@onready var line2D : Line2D = $Line2D

## Snake positions in grid space (head at index 0, tail at end)
var snake_array : Array[Vector2i] = []:
	set(value):
		snake_array = value
		update_snake_visuals()

func initialise() -> Error : 
	# Initialize with empty snake
	line2D.clear_points()
	return OK

## Updates Line2D and camera based on current snake_array
func update_snake_visuals() -> void:
	if snake_array.is_empty():
		line2D.clear_points()
		return
	
	# Update Line2D points - convert grid positions to world positions
	line2D.clear_points()
	for grid_pos in snake_array:
		var world_pos : Vector2 = Vector2(grid_pos * 64 + Vector2i(32, 32))
		line2D.add_point(world_pos)
	
	# Update camera to follow head (first position in array)
	var head_world_pos : Vector2 = Vector2(snake_array[0] * 64 + Vector2i(32, 32))
	camera.global_position = head_world_pos
