import os, random
import numpy as np
DirFrag = "../Fragments/"

def center(dep, fin):
	fragCen = random.choice(os.listdir(DirFrag+"Center"))
	input = np.loadtxt(DirFrag+"Center/"+fragCen, dtype='i', delimiter=' ')
	nbRot = random.choice([0, 1, 2, 3])
	center = np.rot90(input, nbRot)
	print(str(dep) + " " + str(fin))
	if not dep :
		center = np.where(center==2, 0, center)
	if not fin :
		center = np.where(center==3, 0, center)
	return center

#num indicate wich border we want : 0 = North, 1 = West, 2 = South, 3 = East.
def border(num, dep, fin):
	fragBor = random.choice(os.listdir(DirFrag+"Border"))
	border = np.loadtxt(DirFrag+"Border/"+fragBor, dtype='i', delimiter=' ')
	if random.randrange(2) == 1 :
		border = np.fliplr(border)
	border = np.rot90(border, num)
	print(str(dep) + " " + str(fin))
	if not dep :
		border = np.where(border==2, 0, border)
	if not fin :
		border = np.where(border==3, 0, border)
	return border

#num indicate wich border we want : 0 = NorthWest, 1 = SouthWest, 2 = SouthEast, 3 = NorthEast.
def corner(num, dep, fin):
	fragCor = random.choice(os.listdir(DirFrag+"Corner"))
	corner = np.loadtxt(DirFrag+"Corner/"+fragCor, dtype='i', delimiter=' ')
	if random.randrange(2) == 1:
		corner = np.transpose(corner)
	corner = np.rot90(corner, num)
	print(str(dep) + " " + str(fin))
	if not dep :
		print("ayayo!")
		corner = np.where(corner==2, 0, corner)
	if not fin :
		print("ayaya!")
		corner = np.where(corner==3, 0, corner)
	return corner

def Print_Test(seed):
	random.seed(seed)
	depart = random.choice([0,1,2,3,4,5,6,7,8])
	print(depart)
	finish = 8-depart
	NorthThird = np.hstack((corner(0, depart == 0, finish == 0), border(0, depart == 1, finish == 1), corner(3, depart == 2, finish == 2)))
	CenterThird = np.hstack((border(1, depart == 3, finish == 3), center(depart == 4, finish == 4), border(3, depart == 5, finish == 5)))
	SouthThird = np.hstack((corner(1, depart == 6, finish == 6), border(2, depart == 7, finish == 7), corner(2, depart == 8, finish == 8)))
	Layout = np.vstack((NorthThird, CenterThird, SouthThird))
	Layout

Print_Test(4)


