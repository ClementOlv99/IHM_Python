extends Node2D
class_name SnakeLayer

var cycle_duration : float = 1.0

@onready var camera : Camera2D = $Camera2D
@onready var line2D : Line2D = $Line2D
@onready var light : PointLight2D = $PointLight2D

## Snake positions in grid space (head at index 0, tail at end)
var snake_array : Array[Vector2i] = []:
	set(value):
		if value != snake_array:
			# Store previous positions for interpolation
			previous_snake_array = snake_array.duplicate()
			snake_array = value
			# Reset interpolation
			interpolation_progress = 0.0
			is_interpolating = true
			update_snake_visuals()

## Previous snake positions for interpolation
var previous_snake_array : Array[Vector2i] = []

## Interpolation progress (0.0 to 1.0)
var interpolation_progress : float = 0.0

## Whether we're currently interpolating
var is_interpolating : bool = false

func _ready() -> void:
	# Enable processing for smooth interpolation
	set_process(true)

func _process(delta: float) -> void:
	if is_interpolating and cycle_duration > 0:
		# Advance interpolation
		interpolation_progress += delta / cycle_duration
		
		if interpolation_progress >= 1.0:
			interpolation_progress = 1.0
			is_interpolating = false
		
		# Update visuals with interpolated positions
		update_snake_visuals()

func initialise() -> Error : 
	# Initialize with empty snake
	line2D.clear_points()
	previous_snake_array.clear()
	snake_array.clear()
	interpolation_progress = 0.0
	is_interpolating = false
	return OK

## Updates Line2D and camera based on current snake_array with interpolation
func update_snake_visuals() -> void:
	if snake_array.is_empty():
		line2D.clear_points()
		return
	
	# Calculate interpolated positions
	var interpolated_positions : Array = []
	
	for i in range(snake_array.size()):
		var current_grid_pos : Vector2i = snake_array[i]
		var current_world_pos : Vector2 = Vector2(current_grid_pos * 64 + Vector2i(32, 32))
		
		# If we have previous positions and are interpolating, blend between old and new
		if is_interpolating and len(previous_snake_array) > 0 and (i == len(previous_snake_array)-1 or i == 0):
			var previous_grid_pos : Vector2i = previous_snake_array[i]
			var previous_world_pos : Vector2 = Vector2(previous_grid_pos * 64 + Vector2i(32, 32))
			
			# Smooth interpolation with easing
			var t : float = ease(interpolation_progress, -2.0)  # Ease out for smooth arrival
			var interpolated_pos : Vector2 = previous_world_pos.lerp(current_world_pos, t)
			interpolated_positions.append(interpolated_pos)
		else:
			# No interpolation, use current position
			interpolated_positions.append(current_world_pos)
		
	interpolated_positions = snake_array.map(
		func (i:Vector2) :
			return i * 64 + Vector2(32,32)
	) as Array[Vector2]
	# Update Line2D with interpolated points
	line2D.clear_points()
	for pos in interpolated_positions:
		line2D.add_point(pos)
	
	# Update camera to follow interpolated head position
	if interpolated_positions.size() > 0:
		camera.global_position = interpolated_positions[0]
		light.global_position = interpolated_positions[0]
