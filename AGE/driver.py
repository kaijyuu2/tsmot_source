

#.mappe is imported in __init__
from .constants import *

from kaiengine.destroyinterface import DestroyInterface
from kaiengine.sprite import Sprite
from kaiengine.display import getWindowDimensions
from kaiengine.sGraphics import getTextureDimensions
from kaiengine.resource import toStringPath

import os
import copy
import operator

Driver = None

class AGEDriver(DestroyInterface):
    def __init__(self):
        from .mappe import Map
        from .darkener import Darkener
        super(AGEDriver, self).__init__()
        self.glyph_filepath = toStringPath(os.path.dirname(__file__), RESOURCES_FOLDER, GLYPH_FILENAME) #default
        self.glyph_dim = [GLYPHS_W, GLYPHS_H] #default
        self.map = Map()
        self.darkener = Darkener()
        path = toStringPath(os.path.dirname(__file__), RESOURCES_FOLDER, BACKGROUND_FILENAME)
        self.background = Sprite(path, layer = BACKGROUND_LAYER)
        self.background.setColor(*DEFAULT_BACKGROUND_COLOR)
        self.background.set_dimensions(*getWindowDimensions())
        self.background.follow_camera = True

    def SetBackgroundColor(self, color):
        self.background.setColor(*color)

    def GetGlyphFilepath(self):
        return self.glyph_filepath

    def GetGlyphsColumnsRows(self):
        return copy.copy(self.glyph_dim)

    def GetGlyphSize(self):
        dim = getTextureDimensions(self.glyph_filepath)
        return list(map(operator.truediv, dim, self.glyph_dim))

    def SetGlyphData(self, filepath = None, x = None, y = None):
        if filepath is None:
            filepath = self.glyph_filepath
        if x is None:
            x = self.glyph_dim[0]
        if y is None:
            y = self.glyph_dim[1]
        refresh = filepath != self.glyph_filepath or self.glyph_dim != [x,y]
        assert os.path.isfile(filepath), filepath + " doesn't seem to exist."
        self.glyph_filepath = filepath
        self.glyph_dim = [x, y]
        if refresh:
            self.UpdateSpriteGraphics()

    def UpdateSpriteGraphics(self):
        '''call if glyph filepath or dimenions are changed'''
        if self.map is not None:
            self.map.UpdateSpriteGraphics()
        self.UpdateDarkener()

    def UpdateDarkener(self):
        if self.darkener is not None:
            self.darkener.UpdateSpritePos()

    def destroy(self):
        if AGEDriver is not None:
            super(AGEDriver, self).destroy()
        if self.map is not None:
            self.map.destroy()
            self.map = None
        if self.background is not None:
            self.background.destroy()
            self.background = None
        if self.darkener is not None:
            self.darkener.destroy()
            self.darkener = None

def InitDriver():
    global Driver
    Driver = AGEDriver()
    Driver.UpdateDarkener()

def CloseDriver():
    global Driver
    if Driver is not None:
        Driver.destroy()
        Driver = None
