extends TileMapLayer
class_name ItemLayer

func change_layout(new_layout:Array[Array]) -> void:
	for x in len(new_layout) :
		for y in len(new_layout[x]) :
			var cell_pos := Vector2i(x, y)
			var current_atlas := get_cell_atlas_coords(cell_pos)
			
			match new_layout[x][y] :
				0 : # Floor, ignore
					if current_atlas != Vector2i(-1, -1):  # Only erase if cell exists
						erase_cell(cell_pos)
				1 : # Wall, ignore
					if current_atlas != Vector2i(-1, -1):
						erase_cell(cell_pos)
				2 : # Start, ignore
					if current_atlas != Vector2i(-1, -1):
						erase_cell(cell_pos)
				3 : # Down stairs, ignore
					if current_atlas != Vector2i(-1, -1):
						erase_cell(cell_pos)
				4 : # Apple (0,0)
					if current_atlas != Vector2i(0, 0):  # Only set if different
						set_cell(cell_pos, 0, Vector2i(0, 0))
				5 : # Trap (0,1)
					if current_atlas != Vector2i(0, 1):  # Only set if different
						set_cell(cell_pos, 0, Vector2i(0, 1))
				_ : # Void, ignore
					if current_atlas != Vector2i(-1, -1):
						erase_cell(cell_pos)
