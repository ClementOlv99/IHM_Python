import os, random
import numpy as np
import json

DirLayout = "../Layouts/"

# Level indicate the chosen layout : 0 = Tutorial, 1 = CheckItUp, 2 = Cave, 3 = Maze.

def select(level):
	f = open("layout.json", "w")
	match level:
		case 0:
			choice="start.txt"
		case 1:
			choice="CheckItUp.txt"
		case 2:
			choice="Cave.txt"
		case 3:
			choice="Maze.txt"
	layout = np.loadtxt(DirLayout+choice, dtype='i', delimiter=' ')
	f.write(json.dumps(layout.tolist()))
	return layout

select(1)

