#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Detecteur_Input_Snake
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


class Detecteur_Input_Snake(metaclass=Singleton):
    def __init__(self):
        pass
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
    
    def dir(self):
        result = {'value': None}
        def on_press(key):
            if key==keyboard.Key.down:
                result['value'] = 3
                return False
            if key==keyboard.Key.up:
                result['value'] = 1
                return False
            if key==keyboard.Key.left:
                result['value'] = 4
                return False
            if key==keyboard.Key.right:
                result['value'] = 2
                return False

        # Collecter les événements jusqu'à la libération
        with keyboard.Listener(
                on_press=on_press) as listener:
            listener.join()
        return result['value']


