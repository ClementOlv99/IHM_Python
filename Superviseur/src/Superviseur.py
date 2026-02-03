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
import random
lvtype = {1 : "random", 2: "preset"}

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

        #attribut
        self.ready = False

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

    def reset(self,config):
        self.seed = random.randint(1,100000000000000000000)
        self.level = 0
        self.config = config
        self.ready = True

    def superviseur(self):
        match self.level:
            case 0:              
                self.level=self.level+self.config
                return lvtype[2],0
            case 6:
                lvconfig=1
                self.level =self.level+self.config
                return lvtype[2],lvconfig
            case 12:
                lvconfig=2
                self.level=self.level+self.config
                return lvtype[2],lvconfig
            case 18:
                lvconfig=3
                self.level=self.level+self.config
                return lvtype[2],lvconfig
            case _:
                lvconfig=self.seed+self.level
                self.level=self.level+self.config
                return lvtype[1],lvconfig



