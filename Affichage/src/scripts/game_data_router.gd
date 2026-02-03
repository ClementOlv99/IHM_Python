## Custom HTTP Router for receiving game data as JSON
##
## This router handles POST requests containing game state data (level layout,
## snake position, items, etc.) and parses JSON into a dictionary for processing.
##
## Usage:
## [codeblock]
## var router = GameDataRouter.new("/game_data")
## router.data_received.connect(_on_game_data_received)
## server.register_router(router)
##
## func _on_game_data_received(data: Dictionary) -> void:
##     # Process the game data dictionary
##     if data.has("snake_position"):
##         update_snake(data["snake_position"])
## [/codeblock]
class_name GameDataRouter
extends HttpRouter

## Emitted when valid JSON game data is received
signal data_received(data: Dictionary)

## Creates a GameDataRouter instance
## [br]
## [br][param endpoint_path] - The HTTP endpoint path (e.g., "/game_data")
func _init(endpoint_path: String = "/game_data") -> void:
	super._init(endpoint_path, {
		'post': _handle_post_request
	})

## Handles POST requests with JSON game data
func _handle_post_request(request: HttpRequest, response: HttpResponse) -> bool:
	var body = request.body
	print()
	print("Received POST body: ", body)

	if body.is_empty():
		response.send(400, "Empty request body")
		return true
	
	# Parse JSON from request body
	var json = JSON.new()
	var error = json.parse(body)
	
	if error != OK:
		var error_msg = "JSON Parse Error at line %d: %s" % [json.get_error_line(), json.get_error_message()]
		push_error(error_msg)
		response.send(400, error_msg)
		return true
	
	var data = json.get_data()
	
	# Ensure parsed data is a dictionary
	if not data is Dictionary:
		response.send(400, "Expected JSON object, got " + str(typeof(data)))
		return true
	
	# Emit signal with parsed dictionary
	data_received.emit(data)
	
	# Send success response
	response.send(200, "Data received successfully")
	return true
