#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Generateur_Aleatoire
#
#  Created by Ingenuity i/o on 2026/01/30
#
#  Copyright © 2025 Ingenuity i/o. All rights reserved.
#
import ingescape as igs
import os, random
import numpy as np
import json

DirFrag = "../Fragments/"

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Generateur_Aleatoire(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.SeedI = None

        # outputs
        self._LayoutO = None

    # outputs
    @property
    def LayoutO(self):
        return self._LayoutO

    @LayoutO.setter
    def LayoutO(self, value):
        self._LayoutO = value
        if self._LayoutO is not None:
            igs.output_set_data("layout", value)

    def center(self, dep, fin):
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
    def border(self, num, dep, fin):
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
    def corner(self, num, dep, fin):
        fragCor = random.choice(os.listdir(DirFrag+"Corner"))
        corner = np.loadtxt(DirFrag+"Corner/"+fragCor, dtype='i', delimiter=' ')
        if random.randrange(2) == 1:
            corner = np.transpose(corner)
        corner = np.rot90(corner, num)
        if not dep :
            corner = np.where(corner==2, 0, corner)
        if not fin :
            corner = np.where(corner==3, 0, corner)
        return corner
