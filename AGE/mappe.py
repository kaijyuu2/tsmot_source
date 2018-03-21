

from .tile import Tile
from .constants import NULL_CHAR, NULL_CHAR_LOC

from kaiengine.destroyinterface import DestroyInterface

class Map(DestroyInterface):
    def __init__(self, width = 0, height = 0):
        super(Map, self).__init__()
        self._tiles = {}
        self.width = 0
        self.height = 0
        self.SetDimensions(width, height)

    def SetTile(self, value, layer, x, y, width = 1, height = 1, color = None, highlight_color = -1):
        if value == NULL_CHAR or value == NULL_CHAR_LOC:
            return
        self._IterateTiles(width, height, x, y, "SetTile", value, layer, color, highlight_color)

    def SetTileColor(self, color, layer, x, y, width = 1, height = 1):
        self._IterateTiles(width, height, x, y, "SetColor", color, layer)

    def SetTileHighlight(self, color, layer, x, y, width = 1, height = 1):
        self._IterateTiles(width, height, x, y, "SetHighlight", color, layer)

    def RemoveTile(self, layer, x, y, width = 1, height = 1):
        self._IterateTiles(width, height, x, y, "RemoveTile", layer)

    def GetTile(self, x, y):
        try:
            return self._tiles[(x,y)]
        except KeyError:
            return None

    def DrawString(self, string, layer, x, y, *args, **kwargs):
        for char in string:
            self.SetTile(char, layer, x, y, 1, 1, *args, **kwargs)
            x += 1

    def ClearLayer(self, layer):
        self.RemoveTile(layer, 0, 0, self.width, self.height)

    def ClearScreen(self):
        for tile in list(self._tiles.values()):
            tile.ClearTile()

    def _IterateTiles(self, width, height, x, y, func, *args, **kwargs):
        """call the specified func on all tiles in the specified range"""
        if width >= 0:
            xlist = range(width)
        else:
            xlist = [i * -1 for i in range(abs(width))]
        if height >= 0:
            ylist = range(height)
        else:
            ylist = [i * -1 for i in range(abs(height))]
        method = getattr(Tile, func)
        for i in xlist:
            for i2 in ylist:
                tile = self.GetTile(x + i, y + i2)
                if tile is not None:
                    method(tile, *args, **kwargs)

    def SetDimensions(self, width, height):
        if width > self.width:
            for i in range(width - self.width):
                for i2 in range(self.height):
                    pos = (self.width +i, i2)
                    self._tiles[pos] = Tile(*pos)
        else:
            for i in range(self.width - width):
                for i2 in range(self.height):
                    pos = (self.width - i, i2)
                    self._tiles[pos].destroy()
                    del self._tiles[pos]
        self.width = width
        if height > self.height:
            for i in range(height - self.height):
                for i2 in range(self.width):
                    pos = (i2, self.height +i)
                    self._tiles[pos] = Tile(*pos)
        else:
            for i in range(self.height - height):
                for i2 in range(self.width):
                    pos = (i2, self.height - i)
                    self._tiles[pos].destroy()
                    del self._tiles[pos]
        self.height = height
        from .driver import Driver
        if Driver is not None:
            Driver.UpdateDarkener()

    def GetDimensions(self):
        return self.width, self.height


    def UpdateSpriteGraphics(self):
        '''refreshes graphics if the basic texture was changed in some way'''
        for tile in list(self._tiles.values()):
            tile.UpdateSpriteGraphics()

    def destroy(self):
        if Map is not None:
            super(Map, self).destroy()
        for tile in list(self._tiles.values()):
            tile.destroy()
        self._tiles.clear()
