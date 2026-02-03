#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Detecteur_Echap
#
#  Created by Ingenuity i/o on 2026/01/30
#
#  Copyright © 2025 Ingenuity i/o. All rights reserved.
#
import ingescape as igs
from pynput import keyboard

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Detecteur_Echap(metaclass=Singleton):
    def __init__(self):
        pass
        # outputs
        self._Pause_PressedO = None

    # outputs
    @property
    def Pause_PressedO(self):
        return self._Pause_PressedO

    @Pause_PressedO.setter
    def Pause_PressedO(self, value):
        self._Pause_PressedO = value
        if self._Pause_PressedO is not None:
            igs.output_set_bool("pause_pressed", self._Pause_PressedO)
    
    def echap(self):
        result = {'value': None}
        def on_press(key):
            if key==keyboard.Key.esc:
                result['value'] = True
                return False

        # Collecter les événements jusqu'à la libération
        with keyboard.Listener(
                on_press=on_press) as listener:
            listener.join()
        return result['value']


