#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Moteur_Jeu
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


class Moteur_Jeu(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.DirectionI = None
        self.PauseI = None
        self.LevelI = None

        # outputs
        self._DisplayO = None

    # outputs
    @property
    def DisplayO(self):
        return self._DisplayO

    @DisplayO.setter
    def DisplayO(self, value):
        self._DisplayO = value
        if self._DisplayO is not None:
            igs.output_set_data("display", value)
    def set_New_LevelO(self):
        igs.output_set_impulsion("new_level")

    def set_Game_OverO(self):
        igs.output_set_impulsion("game_over")



