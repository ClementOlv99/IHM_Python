#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Detecteur_Input_Whiteboard
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


class Detecteur_Input_Whiteboard(metaclass=Singleton):
    def __init__(self):
        pass
        # outputs
        self._Button_PressedO = None

    # outputs
    @property
    def Button_PressedO(self):
        return self._Button_PressedO

    @Button_PressedO.setter
    def Button_PressedO(self, value):
        self._Button_PressedO = value
        if self._Button_PressedO is not None:
            igs.output_set_bool("button_pressed", self._Button_PressedO)


