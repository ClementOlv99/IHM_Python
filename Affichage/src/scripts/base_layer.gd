extends TileMapLayer
class_name BaseLayer

func _ready() -> void:
	change_layout([[1,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]])

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
					set_cell(cell_pos, 1, Vector2i(1, 0))
				1 : # Wall (4,0)
					print("Set wall at ", cell_pos)
					set_cell(cell_pos, 1, Vector2i(4, 0))
				2 : # Start (7,0)
					set_cell(cell_pos, 1, Vector2i(7, 0))
				3 : # Down stairs (8,0)
					set_cell(cell_pos, 1, Vector2i(8, 0))
				4 : # Apple, managed by itemlayer, put floor here
					set_cell(cell_pos, 1, Vector2i(1, 0))
				5 : # Trap, managed by itemlayer, put floor here
					set_cell(cell_pos, 1, Vector2i(1, 0))
				_ : # Void (0,0)
					set_cell(cell_pos, 1, Vector2i(0, 0))
	print("Layout set complete. Tile counts: ", tile_counts)
