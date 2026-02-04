#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Generateur_Manuel
#
#  Created by Ingenuity i/o on 2026/01/30
#
#  Copyright © 2025 Ingenuity i/o. All rights reserved.
#
import ingescape as igs
import os
import numpy as np
import json


DirLayout = "../Layouts/"

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Generateur_Manuel(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.Level_NumberI = None

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
	
    
# Level indicate the chosen layout : 0 = Tutorial, 1 = CheckItUp, 2 = Cave, 3 = Maze.
    def select_level(self, level):
        match level:
            case 0:
                choice="start.txt"
            case 1:
                choice="CheckItUp.txt"
            case 2:
                choice="Cave.txt"
            case 3:
                choice="Maze.txt"
            case _:
                choice="Maze.txt"
        layout = np.loadtxt(DirLayout+choice, dtype='i', delimiter=' ')
        return layout



