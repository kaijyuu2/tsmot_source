

from .constants import *
from .functions import GetGlyphFilepath, GetGlyphColumnsRows

from kaiengine.sprite import Sprite
from kaiengine.destroyinterface import DestroyInterface
from kaiengine.resource import toStringPath

import os
import sys


class Tile(DestroyInterface):
    def __init__(self, x, y):
        super(Tile, self).__init__()
        self._sprite = Sprite(GetGlyphFilepath(), layer = GLYPH_LAYER)
        self._sprite.set_gridsize(GLYPHS_W, GLYPHS_H, True)
        self._spritehighlight = Sprite(toStringPath(os.path.dirname(__file__), RESOURCES_FOLDER, BACKGROUND_FILENAME), layer = GLYPH_HIGHLIGHT_LAYER)
        dim = GetGlyphColumnsRows()
        self._spritehighlight.set_dimensions(self._sprite.original_width / dim[0], self._sprite.original_height / dim[1])
        self._default_image = [0,self._sprite.gridsize[1] - 1]
        self._sprite.change_image(self._default_image)
        self._spritehighlight.show = False
        self._layers = {}
        self._sorted_layer_keys = []
        self._pos = [0,0]
        self.SetPos(x, y)

    def SetPos(self, x = None, y = None):
        if x is None:
            x = self._pos[0]
        if y is None:
            y = self._pos[1]
        self._pos = [x,y]
        self._sprite.setPos(self._pos[0] * self._sprite.width, self._pos[1] * self._sprite.height)
        self._spritehighlight.setPos(self._pos[0] * self._sprite.width, self._pos[1] * self._sprite.height)

    def SetColor(self, color, layer):
        try:
            self._layers[layer][COLOR] = color
        except KeyError:
            return
        self._SetTile(layer)

    def SetHighlight(self, color, layer):
        try:
            self._layers[layer][HIGHLIGHT] = color
        except KeyError:
            return
        self._SetTile(layer)

    def SetTile(self, char, layer, color = None, highlight_color = -1):
        try:
            index = CHARLIST[char]
        except TypeError: #it's proooobably an appropriate index already
            index = char
        except KeyError: #something not in the lookup dict...
            try:
                index = CHARLIST[str(char)] #check if it's a number not yet turned into a string
            except KeyError:
                raise KeyError("Unsupported glyph: " + str(char))
        if index == NULL_CHAR_LOC:
            return
        self.SetTileByIndex(index, layer, color, highlight_color)

    def SetTileByIndex(self, index, layer, color = None, highlight_color = -1):
        if color is None:
            try:
                color = self._layers[layer][COLOR]
            except KeyError:
                color = DEFAULT_COLOR
        if highlight_color is -1:
            try:
                highlight_color = self._layers[layer][HIGHLIGHT]
            except KeyError:
                highlight_color = None
        self._layers[layer] = [index, color, highlight_color]
        self._sorted_layer_keys = sorted(list(self._layers.keys()), reverse = True)
        self._SetTile(layer)

    def RemoveTile(self, layer):
        try:
            update = layer == self._sorted_layer_keys[0]
        except IndexError:
            return #nothing in the layers list; just return to save time
        try:
            del self._layers[layer]
        except KeyError:
            pass
        try:
            self._sorted_layer_keys.remove(layer)
        except ValueError:
            pass
        if update:
            self._SetTile()

    def ClearTile(self):
        self._layers.clear()
        self._sorted_layer_keys[:] = [] #clear the list
        self._SetTile()

    def GetTileIndex(self, layer):
        try:
            return self._layers[layer][INDEX]
        except KeyError:
            return self._default_image

    def GetTileColor(self, layer):
        try:
            return self._layers[layer][COLOR]
        except KeyError:
            return DEFAULT_COLOR[:]

    def _SetTile(self, layer = None):
        if layer is not None:
            try:
                currentlayer = self._sorted_layer_keys[0]
            except IndexError:
                currentlayer = None
            if currentlayer != layer:
                return #skip everything if we don't need to update the tile's graphics
        try:
            index = self._layers[self._sorted_layer_keys[0]][INDEX]
            color = self._layers[self._sorted_layer_keys[0]][COLOR]
            highlight = self._layers[self._sorted_layer_keys[0]][HIGHLIGHT]
        except (IndexError, KeyError):
            index = self._default_image
            color = DEFAULT_COLOR
            highlight = None
        self._sprite.change_image(index)
        self._sprite.setColor(*color)
        self._SetHighlight(highlight)

    def _SetHighlight(self, color):
        if color is None:
            self._spritehighlight.show = False
        else:
            self._spritehighlight.setColor(*color)
            self._spritehighlight.show = True


    def UpdateSpriteGraphics(self):
        '''refreshes graphics if the basic texture was changed in some way'''
        self._sprite.set_image(GetGlyphFilepath())
        dim = GetGlyphColumnsRows()
        self._sprite.set_gridsize(*dim, reset_dim = True)
        self._spritehighlight.set_dimensions(self._sprite.original_width / dim[0], self._sprite.original_height / dim[1])
        self.SetPos()

    def destroy(self):
        if Tile:
            super(Tile, self).destroy()
        if self._sprite is not None:
            self._sprite.destroy()
            self._sprite = None
        if self._spritehighlight is not None:
            self._spritehighlight.destroy()
            self._spritehighlight = None
