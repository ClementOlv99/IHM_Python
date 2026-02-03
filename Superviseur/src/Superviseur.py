#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Superviseur
#
#  Created by Ingenuity i/o on 2026/02/03
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


class Superviseur(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.ConfigI = None

        # outputs
        self._Difficulty_LevelO = None
        self._Level_ConfigO = None
        self._Level_TypeO = None

    # outputs
    @property
    def Difficulty_LevelO(self):
        return self._Difficulty_LevelO

    @Difficulty_LevelO.setter
    def Difficulty_LevelO(self, value):
        self._Difficulty_LevelO = value
        if self._Difficulty_LevelO is not None:
            igs.output_set_int("difficulty_level", self._Difficulty_LevelO)
    @property
    def Level_ConfigO(self):
        return self._Level_ConfigO

    @Level_ConfigO.setter
    def Level_ConfigO(self, value):
        self._Level_ConfigO = value
        if self._Level_ConfigO is not None:
            igs.output_set_int("level_config", self._Level_ConfigO)
    @property
    def Level_TypeO(self):
        return self._Level_TypeO

    @Level_TypeO.setter
    def Level_TypeO(self, value):
        self._Level_TypeO = value
        if self._Level_TypeO is not None:
            igs.output_set_string("level_type", self._Level_TypeO)


