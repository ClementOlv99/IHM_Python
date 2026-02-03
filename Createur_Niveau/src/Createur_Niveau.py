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
        self.layout = None
        self.elements = None

    # outputs
    @property
    def LevelO(self):
        return self._LevelO

    @LevelO.setter
    def LevelO(self, value):
        self._LevelO = value
        if self._LevelO is not None:
            igs.output_set_data("level", value)    
    
    @layout.setter
    def layout(self, value):
        self.layout = value
        print("layout setter")
        if self.elements is not None:
            self.Compute()

    @elements.setter
    def elements(self, value):
        self.element = value
        print("elements setter")
        if self.layout is not None:
            self.Compute()

    def Compute(self):
        print("computing")
        level = np.array(self.layout)
        apple = self.elements[0]
        trap = self.elements[1]
        possibles_indices = np.where(layout == 0)
        print(possibles_indices.tolist())


