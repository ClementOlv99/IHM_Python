#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Traitement_Input_Whiteboard
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


class Traitement_Input_Whiteboard(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.Button_PressedI = None

        # outputs
        self._ConfigO = None
        self._InstructionO = None

    # outputs
    def set_StartO(self):
        igs.output_set_impulsion("start")

    @property
    def ConfigO(self):
        return self._ConfigO

    @ConfigO.setter
    def ConfigO(self, value):
        self._ConfigO = value
        if self._ConfigO is not None:
            igs.output_set_data("config", value)
    def set_RefreshO(self):
        igs.output_set_impulsion("refresh")

    @property
    def InstructionO(self):
        return self._InstructionO

    @InstructionO.setter
    def InstructionO(self, value):
        self._InstructionO = value
        if self._InstructionO is not None:
            igs.output_set_string("instruction", self._InstructionO)


