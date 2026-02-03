#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Traitement_Input_Whiteboard
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


class Traitement_Input_Whiteboard(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.Button_PressedI = None

        # outputs
        self._ConfigO = None

        self.ingame = False
        self.difficulty = 1

    # outputs
    @property
    def ConfigO(self):
        return self._ConfigO

    @ConfigO.setter
    def ConfigO(self, value):
        self._ConfigO = value
        if self._ConfigO is not None:
            igs.output_set_int("config", self._ConfigO)


    def whiteboard(self,button):
        if self.ingame == False:
            match button:
                case 0:
                    self.ConfigO = self.difficulty
                    self.ingame = True
                    return True
                case 1:
                    match self.difficulty:
                        case 1:
                            return False
                        case _:
                            self.difficulty = self.difficulty -1
                            return True
                case 2:
                    match self.difficulty:
                        case 4:
                            return False
                        case _:
                            self.difficulty = self.difficulty +1
                            return True