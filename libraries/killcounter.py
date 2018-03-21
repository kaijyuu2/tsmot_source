# -*- coding: utf-8 -*-


import AGE
from kaiengine.destroyinterface import DestroyInterface

from libraries.config import *

class KillCounter(DestroyInterface):
    def __init__(self):
        super(KillCounter, self).__init__()
        self.count = 0
        self.hi = 0

    def Add(self):
        self.count += 1
        if self.hi < self.count:
            self.hi = self.count
        self.UpdateCounter()

    def Reset(self):
        self.count = 0
        self.UpdateCounter()

    def UpdateCounter(self):
        self.RemoveCounter()
        glyphs = []
        tempval = self.count
        if tempval > 0:
            while(tempval != 0):
                glyphs.append(tempval % 10)
                tempval = int(tempval / 10)
        else:
            glyphs.append(0)
        glyphs.reverse()
        counter = 0
        for glyph in glyphs:
            AGE.SetTile(str(glyph), KILL_COUNTER_LAYER, counter, 39)
            counter += 1
        glyphs = []
        tempval = self.hi
        if tempval > 0:
            while(tempval != 0):
                glyphs.append(tempval % 10)
                tempval = int(tempval / 10)
        else:
            glyphs.append(0)
        counter = 0
        for glyph in glyphs:
            AGE.SetTile(str(glyph), KILL_COUNTER_LAYER, 39 - counter, 39)
            counter += 1

    def RemoveCounter(self):
        for i in range(39):
            AGE.RemoveTile(KILL_COUNTER_LAYER, i, 39)

    def destroy(self):
        super(KillCounter, self).destroy()
        self.RemoveCounter()