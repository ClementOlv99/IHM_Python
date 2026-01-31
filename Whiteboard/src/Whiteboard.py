#!/usr/bin/env -P /usr/bin:/usr/local/bin python3 -B
# coding: utf-8

#
#  Whiteboard
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


class Whiteboard(metaclass=Singleton):
    def __init__(self):
        # inputs
        self.TitleI = None
        self.BackgroundcolorI = None
        self.LabelsvisibleI = None
        self.ChatmessageI = None
        self.Ui_CommandI = None

        # outputs
        self._WindowwidthO = None
        self._WindowheightO = None
        self._WhiteboardwidthO = None
        self._WhiteboardheightO = None
        self._LastchatmessageO = None
        self._LastactionO = None
        self._Ui_ErrorO = None

    # outputs
    @property
    def WindowwidthO(self):
        return self._WindowwidthO

    @WindowwidthO.setter
    def WindowwidthO(self, value):
        self._WindowwidthO = value
        if self._WindowwidthO is not None:
            igs.output_set_int("windowWidth", self._WindowwidthO)
    @property
    def WindowheightO(self):
        return self._WindowheightO

    @WindowheightO.setter
    def WindowheightO(self, value):
        self._WindowheightO = value
        if self._WindowheightO is not None:
            igs.output_set_int("windowHeight", self._WindowheightO)
    @property
    def WhiteboardwidthO(self):
        return self._WhiteboardwidthO

    @WhiteboardwidthO.setter
    def WhiteboardwidthO(self, value):
        self._WhiteboardwidthO = value
        if self._WhiteboardwidthO is not None:
            igs.output_set_int("whiteboardWidth", self._WhiteboardwidthO)
    @property
    def WhiteboardheightO(self):
        return self._WhiteboardheightO

    @WhiteboardheightO.setter
    def WhiteboardheightO(self, value):
        self._WhiteboardheightO = value
        if self._WhiteboardheightO is not None:
            igs.output_set_int("whiteboardHeight", self._WhiteboardheightO)
    @property
    def LastchatmessageO(self):
        return self._LastchatmessageO

    @LastchatmessageO.setter
    def LastchatmessageO(self, value):
        self._LastchatmessageO = value
        if self._LastchatmessageO is not None:
            igs.output_set_string("lastChatMessage", self._LastchatmessageO)
    @property
    def LastactionO(self):
        return self._LastactionO

    @LastactionO.setter
    def LastactionO(self, value):
        self._LastactionO = value
        if self._LastactionO is not None:
            igs.output_set_string("lastAction", self._LastactionO)
    @property
    def Ui_ErrorO(self):
        return self._Ui_ErrorO

    @Ui_ErrorO.setter
    def Ui_ErrorO(self, value):
        self._Ui_ErrorO = value
        if self._Ui_ErrorO is not None:
            igs.output_set_string("ui_error", self._Ui_ErrorO)

    # services
    def Settitle(self, sender_agent_name, sender_agent_uuid, Title):
        pass
        # add code here if needed

    def Setbackgroundcolor(self, sender_agent_name, sender_agent_uuid, Color):
        pass
        # add code here if needed

    def Getwindowsize(self, sender_agent_name, sender_agent_uuid):
        pass
        # add code here if needed

    def Getwhiteboardsize(self, sender_agent_name, sender_agent_uuid):
        pass
        # add code here if needed

    def Chat(self, sender_agent_name, sender_agent_uuid, Message):
        pass
        # add code here if needed

    def Chatas(self, sender_agent_name, sender_agent_uuid, Name, Message):
        pass
        # add code here if needed

    def Snapshot(self, sender_agent_name, sender_agent_uuid):
        pass
        # add code here if needed

    def Clear(self, sender_agent_name, sender_agent_uuid):
        pass
        # add code here if needed

    def Showlabels(self, sender_agent_name, sender_agent_uuid):
        pass
        # add code here if needed

    def Hidelabels(self, sender_agent_name, sender_agent_uuid):
        pass
        # add code here if needed

    def Addshape(self, sender_agent_name, sender_agent_uuid, Type, X, Y, Width, Height, Fill, Stroke, Strokewidth):
        pass
        # add code here if needed

    def Addtext(self, sender_agent_name, sender_agent_uuid, Text, X, Y, Color):
        pass
        # add code here if needed

    def Addimage(self, sender_agent_name, sender_agent_uuid, Base64, X, Y, Width, Height):
        pass
        # add code here if needed

    def Addimagefromurl(self, sender_agent_name, sender_agent_uuid, Url, X, Y):
        pass
        # add code here if needed

    def Remove(self, sender_agent_name, sender_agent_uuid, Elementid):
        pass
        # add code here if needed

    def Translate(self, sender_agent_name, sender_agent_uuid, Elementid, Dx, Dy):
        pass
        # add code here if needed

    def Moveto(self, sender_agent_name, sender_agent_uuid, Elementid, X, Y):
        pass
        # add code here if needed

    def Setstringproperty(self, sender_agent_name, sender_agent_uuid, Elementid, Property, Value):
        pass
        # add code here if needed

    def Setdoubleproperty(self, sender_agent_name, sender_agent_uuid, Elementid, Property, Value):
        pass
        # add code here if needed

    def Getelementids(self, sender_agent_name, sender_agent_uuid):
        pass
        # add code here if needed

    def Getelements(self, sender_agent_name, sender_agent_uuid):
        pass
        # add code here if needed


