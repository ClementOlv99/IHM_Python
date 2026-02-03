#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Detecteur_Input_Whiteboard
#
#  Created by Ingenuity i/o on 2026/02/02
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
            igs.output_set_int("button_pressed", self._Button_PressedO)
    
    def inpWithe(self):
        result = {'value': None}
        def on_press(key):
            if key==keyboard.Key.enter:
                result['value'] = 0
                return False
            if key==keyboard.Key.up:
                result['value'] = 1
                return False
            if key==keyboard.Key.down:
                result['value'] = 2
                return False

        # Collecter les événements jusqu'à la libération
        with keyboard.Listener(
                on_press=on_press) as listener:
            listener.join()
        return result['value']


