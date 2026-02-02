extends TileMapLayer
class_name SnakeLayer

var cycle_duration : float
var cycle_timer : Timer

@onready var camera : Camera2D = $Camera2D
@onready var line2D : Line2D = $Line2D


## Current position of the head in the grid
var head_grid_pos : Vector2i = Vector2i(0,0)
var snake_array : Array[Vector2i] = []

## Camera positions (internal)

## Start position of the camera at the current cycle
## DEPRECATED
#var cam_start_pos : Vector2i = Vector2i(0,0)
#var cam_end_pos : Vector2i = Vector2i(0,0)
#var camera_tween : Tween

func initialise() -> Error : 
	#camera.position_smoothing_speed = 64/cycle_duration
	
	cycle_timer = Timer.new()
	self.add_child(cycle_timer)
	cycle_timer.one_shot = false
	cycle_timer.wait_time = cycle_duration
	cycle_timer.start()
	cycle_timer.timeout.connect(cycle)
	cycle()
	
	return OK

func cycle() -> Error :
	head_grid_pos += direction
	$TestSprite.position = head_grid_pos*64 + Vector2i(32,32)
	camera.global_position = head_grid_pos*64 + Vector2i(32,32)
	return OK

func _input(event:InputEvent) -> void :
	if event.is_action_pressed("ui_left") :
		direction = Vector2i.LEFT
		$TestSprite.rotation_degrees = -90
	if event.is_action_pressed("ui_right") :
		direction = Vector2i.RIGHT
		$TestSprite.rotation_degrees = 90
	if event.is_action_pressed("ui_up") :
		direction = Vector2i.UP
		$TestSprite.rotation_degrees = 0
	if event.is_action_pressed("ui_down") :
		direction = Vector2i.DOWN
		$TestSprite.rotation_degrees = 180
