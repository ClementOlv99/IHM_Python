import os, random
import numpy as np
DirFrag = "../Fragments/"

def center():
	fragCen = random.choice(os.listdir(DirFrag+"Center"))
	input = np.loadtxt(DirFrag+"Center/"+fragCen, dtype='i', delimiter=' ')
	nbRot = random.choice([0, 1, 2, 3])
	center = np.rot90(input, nbRot)
	return center

#num indicate wich border we want : 0 = North, 1 = West, 2 = South, 3 = East.
def border(num):
	fragBor = random.choice(os.listdir(DirFrag+"Border"))
	border = np.loadtxt(DirFrag+"Border/"+fragBor, dtype='i', delimiter=' ')
	if random.randrange(2) == 1 :
		border = np.fliplr(border)
	border = np.rot90(border, num)
	return border

#num indicate wich border we want : 0 = NorthWest, 1 = SouthWest, 2 = SouthEast, 3 = NorthEast.
def corner(num):
	fragCor = random.choice(os.listdir(DirFrag+"Corner"))
	corner = np.loadtxt(DirFrag+"Corner/"+fragCor, dtype='i', delimiter=' ')
	if random.randrange(2) == 1:
		corner = np.transpose(corner)
	corner = np.rot90(corner, num)
	return corner

def Print_Test(seed):
	random.seed(seed)
	NorthThird = np.hstack((corner(0), border(0), corner(3)))
	CenterThird = np.hstack((border(1), center(), border(3)))
	SouthThird = np.hstack((corner(1), border(2), corner(2)))
	Layout = np.vstack((NorthThird, CenterThird, SouthThird))
	print("Layout")
	print(Layout)

Print_Test(10)


