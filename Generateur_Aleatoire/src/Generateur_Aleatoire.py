#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Generateur_Aleatoire
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


class Generateur_Aleatoire(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.SeedI = None

        # outputs
        self._LayoutO = None

    # outputs
    @property
    def LayoutO(self):
        return self._LayoutO

    @LayoutO.setter
    def LayoutO(self, value):
        self._LayoutO = value
        if self._LayoutO is not None:
            igs.output_set_data("layout", value)


