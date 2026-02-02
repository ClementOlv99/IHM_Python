import os, random
import numpy as np

DirLayout = "../Layouts/"

# Level indicate the chosen layout : 0 = Tutorial, 1 = CheckItUp, 2 = Cave, 3 = Maze.

def select(level):
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


