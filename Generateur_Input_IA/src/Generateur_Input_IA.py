#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Generateur_Input_IA
#
#  Created by Ingenuity i/o on 2026/01/30
#
#  Copyright © 2025 Ingenuity i/o. All rights reserved.
#
import ingescape as igs


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Generateur_Input_IA(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.Manual_ControlI = None
        self.DisplayI = None

        # outputs
        self._DirectionO = None

    # outputs
    @property
    def DirectionO(self):
        return self._DirectionO

    @DirectionO.setter
    def DirectionO(self, value):
        self._DirectionO = value
        if self._DirectionO is not None:
            igs.output_set_int("direction", self._DirectionO)


