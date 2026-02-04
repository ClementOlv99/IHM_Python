extends TileMapLayer
class_name TopLayer

func _ready() -> void:
	change_layout([[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,1]])

func change_layout(new_layout:Array) -> void:
	for y in len(new_layout) :
		for x in len(new_layout[y]) :
			var cell_pos := Vector2i(x, y)
			var tile_type = int(new_layout[y][x])
			set_cell(cell_pos, 1, Vector2i(-1,-1))
			match tile_type :
				0 : # Floor (1,0)
					print("Set floor down at ", cell_pos)
					pass
				1 : # Wall (4,0)
					print("Set wall at ", cell_pos)
					if (y >= 1) and (y < len(new_layout)) and new_layout[y-1][x] == 0 :
						set_cell(cell_pos, 1, Vector2i(0,12))
					else :
						pass
				_ : # Void (0,0)
					pass
