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
        self.WidthI = None
        self.HeightI = None

        # outputs
        self._ConfigO = None
        self._XO = None
        self._YO = None
        self._WidthO = None
        self._HeightO = None
        self._Stroke_WitdthO = None
        self._ColorO = None
        self._Color_StrokeO = None
        self._ContentO = None

        self.ingame=False
        self.difficulty = 1
        self.width = 100
        self.height = 100

    # outputs
    @property
    def ConfigO(self):
        return self._ConfigO

    @ConfigO.setter
    def ConfigO(self, value):
        self._ConfigO = value
        if self._ConfigO is not None:
            igs.output_set_int("config", self._ConfigO)
    def set_Add_ShapeO(self):
        igs.output_set_impulsion("add_shape")

    @property
    def XO(self):
        return self._XO

    @XO.setter
    def XO(self, value):
        self._XO = value
        if self._XO is not None:
            igs.output_set_double("x", self._XO)
    @property
    def YO(self):
        return self._YO

    @YO.setter
    def YO(self, value):
        self._YO = value
        if self._YO is not None:
            igs.output_set_double("y", self._YO)
    @property
    def WidthO(self):
        return self._WidthO

    @WidthO.setter
    def WidthO(self, value):
        self._WidthO = value
        if self._WidthO is not None:
            igs.output_set_double("width", self._WidthO)
    @property
    def HeightO(self):
        return self._HeightO

    @HeightO.setter
    def HeightO(self, value):
        self._HeightO = value
        if self._HeightO is not None:
            igs.output_set_double("height", self._HeightO)
    @property
    def Stroke_WitdthO(self):
        return self._Stroke_WitdthO

    @Stroke_WitdthO.setter
    def Stroke_WitdthO(self, value):
        self._Stroke_WitdthO = value
        if self._Stroke_WitdthO is not None:
            igs.output_set_double("stroke_witdth", self._Stroke_WitdthO)
    @property
    def ColorO(self):
        return self._ColorO

    @ColorO.setter
    def ColorO(self, value):
        self._ColorO = value
        if self._ColorO is not None:
            igs.output_set_string("color", self._ColorO)
    @property
    def Color_StrokeO(self):
        return self._Color_StrokeO

    @Color_StrokeO.setter
    def Color_StrokeO(self, value):
        self._Color_StrokeO = value
        if self._Color_StrokeO is not None:
            igs.output_set_string("color_stroke", self._Color_StrokeO)
    def set_Add_TextO(self):
        igs.output_set_impulsion("add_text")

    @property
    def ContentO(self):
        return self._ContentO

    @ContentO.setter
    def ContentO(self, value):
        self._ContentO = value
        if self._ContentO is not None:
            igs.output_set_string("content", self._ContentO)


    def whiteboard(self,button):
        if self.ingame == False:
            match button:
                case 0:
                    self.ConfigO = self.difficulty
                    self.ingame = True
                    return 0
                case 1:
                    match self.difficulty:
                        case 1:
                            return 2
                        case _:
                            self.difficulty = self.difficulty -1
                            return 1
                case 2:
                    match self.difficulty:
                        case 4:
                            return 2
                        case _:
                            self.difficulty = self.difficulty +1
                            return 1
    
    def menu1(self,x,y,w,h):
        self.XO = x
        self.YO = y
        self.WidthO = w
        self.HeightO = h
        self.Stroke_WitdthO = 1
        self.ColorO = "lightgreen"
        self.Color_StrokeO = "green"
        self.ContentO = "square"
        self.set_Add_ShapeO()

    def dmenu1(self,x,y,w,h):
        self.XO = x
        self.YO = y
        self.WidthO = w
        self.HeightO = h
        self.Stroke_WitdthO = 1
        self.ColorO = "green"
        self.Color_StrokeO = "darkgreen"
        self.ContentO = "square"
        self.set_Add_ShapeO()
    
    def menu2(self,texte,x,y):
         self.XO = x
         self.YO = y
         self.ColorO = "yellow"
         self.ContentO = texte
         self.set_Add_TextO()

    def dmenu2(self,texte,x,y):
         self.XO = x
         self.YO = y
         self.ColorO = "darkyellow"
         self.ContentO = texte
         self.set_Add_TextO()