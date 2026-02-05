extends TileMapLayer
class_name ItemLayer

func _ready() -> void:
	change_layout([[1,1,1,1,1],[1,4,0,5,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]])

func change_layout(new_layout:Array) -> void:
	print("ItemLayer: Processing layout...")
	var item_count = 0
	for y in len(new_layout) :
		for x in len(new_layout[y]) :
			var cell_pos := Vector2i(x, y)
			var current_atlas := get_cell_atlas_coords(cell_pos)
			
			# Convert to int (Godot JSON parser converts all numbers to floats)
			match int(new_layout[y][x]) :
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
						set_cell(cell_pos, 2, Vector2i(0, 0))
						item_count += 1
						print("  Set apple at ", cell_pos)
				5 : # Trap (0,1)
					if current_atlas != Vector2i(0, 1):  # Only set if different
						set_cell(cell_pos, 2, Vector2i(0, 1))
						item_count += 1
						print("  Set trap at ", cell_pos)
				_ : # Void, ignore
					if current_atlas != Vector2i(-1, -1):
						erase_cell(cell_pos)
	print("ItemLayer: Set ", item_count, " items")
