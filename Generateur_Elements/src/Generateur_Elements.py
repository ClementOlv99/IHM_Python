#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Generateur_Elements
#
#  Created by Ingenuity i/o on 2026/01/30
#
#  Copyright © 2025 Ingenuity i/o. All rights reserved.
#
import ingescape as igs
import time


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Generateur_Elements(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.Difficulty_LevelI = None

        # outputs
        self._Element_ArrayO = None        

    # outputs
    @property
    def Element_ArrayO(self):
        return self._Element_ArrayO

    @Element_ArrayO.setter
    def Element_ArrayO(self, value):
        self._Element_ArrayO = value
        if self._Element_ArrayO is not None:
            igs.output_set_data("element_array", value)

    def Gen_List(self, difficulty):
        match difficulty:
            case 0:
                return [1, 0]
            case 1:
                return [0, 0]
            case 2:
                return [9, 6]
            case 3: 
                return [4, 1]
            case _:
                return [difficulty, difficulty//2]




