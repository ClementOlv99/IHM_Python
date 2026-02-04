extends TileMapLayer
class_name BaseLayer

func _ready() -> void:
	change_layout([[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]])

func change_layout(new_layout:Array) -> void:
	print("Layout type :", type_string(typeof(new_layout)))
	print("Changing layout... dimensions: ", len(new_layout), "x", len(new_layout[0]) if len(new_layout) > 0 else 0)
	var tile_counts = {}
	for y in len(new_layout) :
		for x in len(new_layout[y]) :
			var cell_pos := Vector2i(x, y)
			var tile_type = int(new_layout[y][x])
			tile_counts[tile_type] = tile_counts.get(tile_type, 0) + 1
			match tile_type :
				0 : # Floor (1,0)
					print("Set floor down at ", cell_pos)
					set_cell(
						cell_pos, 
						1, 
						Vector2i(0,0))
				1 : # Wall (4,0)
					print("Set wall at ", cell_pos)
					#if (y >= 1) and (y < len(new_layout)) and new_layout[y-1][x] == 0 : #If tile above is floor, put floor (wall in toplayer)
						#set_cell(
						#cell_pos, 
						#1, 
						#Vector2i(0,0))
					#elif (y >= 0) and (y < len(new_layout) - 1) and new_layout[y+1][x] == 0 : #If tile under is floor, put full wall
						#set_cell(
							#cell_pos, 
							#1, 
							#Vector2i(0,5))
					#elif (x >= 0) and (x < len(new_layout[y]) - 1) and new_layout[y][x+1] == 0 : #If tile on right is floor, put half wall right
						#set_cell(cell_pos, 1, Vector2i(2,9))
					#elif (x >= 1) and (x < len(new_layout[y])) and new_layout[y][x-1] == 0 : #If tile on left is floor, put half wall left
						#set_cell(cell_pos, 1, Vector2i(12,9))
					#elif (x >= 1) and (x < len(new_layout[y])) and (y >= 0) and (y < len(new_layout) - 1) and new_layout[y+1][x-1] == 0 : #If tile on diag down-left is floor, put connector wall down left
						#set_cell(cell_pos, 1, Vector2i(4,9))
					#elif (x >= 0) and (x < len(new_layout[y]) -1) and (y >= 0) and (y < len(new_layout) - 1) and new_layout[y+1][x+1] == 0 : #If tile on diag down-right is floor, put connector wall down right
						#set_cell(cell_pos, 1, Vector2i(3,9))
						#
					#elif (x >= 1) and (x < len(new_layout[y])) and (y >= 1) and (y < len(new_layout)) and new_layout[y-1][x-1] == 0 : #If tile on diag down-left is floor, put connector wall down left
						#set_cell(cell_pos, 1, Vector2i(8,9))
					#elif (x >= 0) and (x < len(new_layout[y]) -1) and (y >= 1) and (y < len(new_layout)) and new_layout[y-1][x+1] == 0 : #If tile on diag down-right is floor, put connector wall down right
						#set_cell(cell_pos, 1, Vector2i(1,9))
						#
					#else : #Else, empty tile
						#set_cell(cell_pos, 1, Vector2i(-1,-1))
					
					set_cell(cell_pos, 1, Vector2i(0,3))
				2 : # Start (7,0)
					set_cell(cell_pos, 1, Vector2i(0, 1))
				3 : # Down stairs (8,0)
					set_cell(cell_pos, 1, Vector2i(1, 1))
				4 : # Apple, managed by itemlayer, put floor here
					set_cell(cell_pos, 1, Vector2i(1, 0))
				5 : # Trap, managed by itemlayer, put floor here
					set_cell(cell_pos, 1, Vector2i(1, 0))
				_ : # Void (0,0)
					set_cell(cell_pos, 1, Vector2i(0, 0))
	print("Layout set complete. Tile counts: ", tile_counts)
