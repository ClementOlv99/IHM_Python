#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Createur_Niveau
#
#  Created by Ingenuity i/o on 2026/01/30
#
#  Copyright © 2025 Ingenuity i/o. All rights reserved.
#
import ingescape as igs
import json
import random
import numpy as np

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Createur_Niveau(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.Element_ArrayI = None
        self.LayoutI = None

        # outputs
        self._LevelO = None

        #local state related attributes
        self._layout = None
        self._elements = None
        self.layout_set = False
        self.element_set = False

    # outputs
    @property
    def LevelO(self):
        return self._LevelO

    @LevelO.setter
    def LevelO(self, value):
        self._LevelO = value
        if self._LevelO is not None:
            igs.output_set_data("level", value)  
  
    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, value):
        self._layout = value
        self.layout_set = True
        if self.element_set:
            self.Compute()

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, value):
        self._elements = value
        self.element_set = True
        if self.layout_set:
            self.Compute()

    def Compute(self):
        self.layout_set = False
        self.element_set = False
        level = np.array(self.layout)
        apple = self.elements[0]
        trap = self.elements[1]
        possibles_indices = np.asarray(level == 0).nonzero()
        x = possibles_indices[0]
        y = possibles_indices[1]
        cases = random.sample(range(len(possibles_indices[0])), apple + trap)
        random.shuffle(cases)
        for i in range(apple):
            level[x[cases[i]]][y[cases[i]]] = 4
        for i in range(trap):
            level[x[cases[apple + i]]][y[cases[apple + i]]] = 5
        print(level)
        self.LevelO = json.dumps(level.tolist()).encode()


