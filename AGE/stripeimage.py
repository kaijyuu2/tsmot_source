

'''

Format specifications!

direction can be v or h, for vertical or horistonal
tiles should be a list of lists of tiles. A tile is a list containing:
the glyph, the color, the highlight color (can be none), and the length, in that order
eg, ["8",[1,1,1],None,1]
Once one list of tiles ends, the next list is the next line of tiles
Horisontal stripes go left to right. Vertical go down to up.
Horisontal stripes should be assumed to go upwards after a line break. Vertical should go right
IE, the origin is always the bottom left
A null character u'/00' or [0,15] is considered blank and should not be drawn at all

eg:

{
"direction":"h",
"tiles":[[[u"8",[1,1,1],[.5,.5,.5],1],[u"a",[1,1,1],None,19]],[[u"8",[1,1,1],None,1]],[[u'/00',[1,1,1],None,1]]]
}

'''

from kaiengine.baseobject import BaseObject
from kaiengine.gconfig.datakeys import PATH, EXTENSION

from .functions import SetTile, RemoveTile
from .constants import NULL_CHAR

STRIPE_GLYPH_INDEX = 0
STRIPE_COLOR_INDEX = 1
STRIPE_HIGHLIGHT_INDEX = 2
STRIPE_LENGTH_INDEX = 3

#vertical or horisontal constants
STRIPE_VERTICAL = "v"
STRIPE_HORISONTAL = "h"

#extension
STRIPE_EXTENSION = ".stripe"

#data keys
STRIPE_DIRECTION = "direction"
STRIPE_TILES = "tiles"
STRIPE_OFFSET = "offset"
STRIPE_USE_OFFSET = "use_offset"


STRIPE_BLANK_TILE = [NULL_CHAR, [1.0,1.0,1.0], None]

class StripeImage(BaseObject):

    #default attributes. Should really be set by the child classes
    #vars()[PATH] = [] #for any dynamic child classes
    vars()[EXTENSION] = STRIPE_EXTENSION #file extension for dynamic child classes

    #other properties
    default_prop = {STRIPE_DIRECTION:STRIPE_HORISONTAL,
                STRIPE_TILES:[],
                STRIPE_OFFSET:[0,0],
                STRIPE_USE_OFFSET:False}

    def CreateFromData(self, data):
        for key, val in list(data.items()):
            setattr(self, key, val)

    def DrawTiles(self, layer, x, y):
        self._manipulateTiles(layer, x, y)

    def RemoveTiles(self, layer, x, y):
        self._manipulateTiles(layer, x, y, draw=False)

    def GetTiles(self):
        return self.tiles

    def GetDirection(self):
        return self.direction

    def IsVertical(self):
        return self.direction == STRIPE_VERTICAL

    def IsHorisontal(self):
        return self.direction == STRIPE_HORISONTAL

    def GetOffset(self):
        return self.offset

    def GetUseOffset(self):
        return self.use_offset

    def Decompress(self):
        #returns individual tiles without the length attribute in (x,y):val dictionary format.
        tiles = {}
        if self.use_offset:
            xstart = self.offset[0]
            ystart = self.offset[1]
        else:
            xstart = 0
            ystart = 0
        x = 0
        y = 0
        if self.IsVertical():
            xinc = 0
            yinc = 1
            x2inc = 1
            y2inc = 0
        else:
            xinc = 1
            yinc = 0
            x2inc = 0
            y2inc = 1
        for tile_list in self.tiles:
            for tile in tile_list:
                for i in range(tile[-1]):
                    tiles[(x + xstart,y + ystart)] = tile[:3]
                    x += xinc
                    y += yinc
            x = (x * x2inc) + x2inc
            y = (y * y2inc) + y2inc
        return tiles

    def Compress(self, data, direction = STRIPE_HORISONTAL, use_offset = False):
        tiles = [[], []]
        if direction == STRIPE_HORISONTAL:
            tiles[0] = data[:]
            tiles[1] = list(zip(*data[::1]))
        else:
            tiles[0] = list(zip(*data[::1]))
            tiles[1] = data[:]
        if use_offset:
            offset = [self._compress_calc_offset(tiles[1]),self._compress_calc_offset(tiles[0])]
        else:
            offset = [0,0]
        newtiles = [self._compress_tiles(tiles[0], offset[1], offset[0]), self._compress_tiles(tiles[1], offset[0], offset[1])]
        if self._compress_find_length(newtiles[0]) > self._compress_find_length(newtiles[1]):
            self.tiles = newtiles[1]
            self.direction = STRIPE_VERTICAL
        else:
            self.tiles = newtiles[0]
            self.direction = STRIPE_HORISONTAL
        self.offset = offset
        self.use_offset = use_offset

    def _compress_calc_offset(self, tiles):
        newoffset = -1
        for i, line in enumerate(tiles):
            for tile in line:
                if tile[0] != NULL_CHAR:
                    newoffset = i
                    break
            if newoffset != -1:
                break
        if newoffset < 0:
            newoffset = 0
        return newoffset

    def _compress_tiles(self, tiles, offset1, offset2):
        newtiles = []
        for i, line in enumerate(tiles):
            if offset1 > i:
                continue
            previous_tile = None
            newtiles.append([])
            for i2, tile in enumerate(line):
                if offset2 > i2:
                    continue
                if tile == previous_tile:
                    newtiles[-1][-1][-1] += 1
                else:
                    newtiles[-1].append(tile[:])
                    newtiles[-1][-1].append(1)
                previous_tile = tile
            if len(newtiles[-1]) > 0 and newtiles[-1][-1][0] == NULL_CHAR:
                newtiles[-1] = newtiles[-1][:-1] #lop off useless ends
        while len(newtiles) > 0 and len(newtiles[-1]) <= 0:
            newtiles = newtiles[:-1]
        return newtiles

    def _compress_find_length(self, tiles):
        count = 0
        for line in tiles:
            for tile in line:
                if tile[0] != NULL_CHAR:
                    count += tile[-1] #add length
        return count

    def serialize(self):
        output_dict = {}
        output_dict[STRIPE_DIRECTION] = self.direction
        output_dict[STRIPE_TILES] = self.tiles
        output_dict[STRIPE_OFFSET] = self.offset
        output_dict[STRIPE_USE_OFFSET] = self.use_offset
        return output_dict

    def _manipulateTiles(self, layer, x, y, draw=True):
        if self.direction == STRIPE_VERTICAL:
            y = x
            length_keyword = "height"
        else:
            length_keyword = "width"
        if self.use_offset:
            offset = self.offset
        else:
            offset = [0,0]
        for i, tilelist in enumerate(self.tiles):
            counter = y
            for tile in tilelist:
                if self.direction == STRIPE_VERTICAL:
                    xx = i
                    yy = counter
                else:
                    xx = counter
                    yy = i
                if draw:
                    SetTile(tile[STRIPE_GLYPH_INDEX], layer, xx + offset[0], yy + offset[1], **{length_keyword:tile[STRIPE_LENGTH_INDEX], "color":tile[STRIPE_COLOR_INDEX],
                                                "highlight_color": tile[STRIPE_HIGHLIGHT_INDEX]})
                else:
                    RemoveTile(layer, xx + offset[0], yy + offset[1], **{self.direction:tile[STRIPE_LENGTH_INDEX]})
                counter += tile[STRIPE_LENGTH_INDEX]

