# -*- coding: utf-8 -*-

#only doodad

import AGE
from kaiengine.destroyinterface import DestroyInterface

from libraries.config import *

class Tree(DestroyInterface):
    def __init__(self, x, y):
        super(Tree, self).__init__()
        self.pos = (x,y)
        AGE.SetTile([6,15], MAP_LAYER, x, y, color = COLOR_GREEN, highlight_color = COLOR_DARK_GREEN)

    def destroy(self):
        super(Tree, self).destroy()
        AGE.RemoveTile(MAP_LAYER, *self.pos)