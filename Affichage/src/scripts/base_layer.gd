extends TileMapLayer
class_name BaseLayer

func change_layout(new_layout:Array[Array]) -> void:
	for x in len(new_layout) :
		for y in len(new_layout[x]) :
			var cell_pos := Vector2i(x, y)
			match new_layout[x][y] :
				0 : # Floor (1,0)
					set_cell(cell_pos, 0, Vector2i(1, 0))
				1 : # Wall (4,0)
					set_cell(cell_pos, 0, Vector2i(4, 0))
				2 : # Start (7,0)
					set_cell(cell_pos, 0, Vector2i(7, 0))
				3 : # Down stairs (8,0)
					set_cell(cell_pos, 0, Vector2i(8, 0))
				4 : # Apple, managed by itemlayer, put floor here
					set_cell(cell_pos, 0, Vector2i(1, 0))
				5 : # Trap, managed by itemlayer, put floor here
					set_cell(cell_pos, 0, Vector2i(1, 0))
				_ : # Void (0,0)
					set_cell(cell_pos, 0, Vector2i(0, 0))
