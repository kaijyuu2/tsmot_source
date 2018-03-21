# -*- coding: utf-8 -*-


import AGE
from kaiengine.destroyinterface import DestroyInterface

from libraries.config import *
from libraries import gamestate



class Shot(DestroyInterface):
    def __init__(self, x, y, facing):
        super(Shot, self).__init__()
        self.pos = [x,y]
        self._displayed = False
        self.facing = facing
        self.AddGraphic()
        self.killed = False
        self.diagAccum = 0

        if gamestate.EnemyOnPos(*self.pos):
            self.killed = True
            gamestate.KillEnemy(newx, newy)

    def AddGraphic(self):
        if not self._displayed:
            AGE.SetTile(SHOT_TILES[self.facing], SHOT_LAYER, *self.pos, highlight_color = COLOR_DARK_GREEN)
            self._displayed = True

    def RemoveGraphic(self):
        if self._displayed:
            AGE.RemoveTile(SHOT_LAYER, *self.pos)
            self._displayed = False

    def run(self):
        self.Move()

    def Move(self):
        self.RemoveGraphic()
        if gamestate.EnemyOnPos(*self.pos):
            self.killed = True
            gamestate.KillEnemy(*self.pos)
            return
        if self.facing == UP:
            x, y = 0,1
        elif self.facing == DOWN:
            x, y = 0,-1
        elif self.facing == RIGHT:
            x, y = 1,0
        elif self.facing == LEFT:
            x, y = -1,0
        elif self.facing == UP_LEFT:
            x, y = -1,1
        elif self.facing == UP_RIGHT:
            x, y = 1,1
        elif self.facing == DOWN_LEFT:
            x, y = -1,-1
        elif self.facing == DOWN_RIGHT:
            x, y = 1,-1
        if self.facing in [UP, DOWN, RIGHT, LEFT]:
            newx = self.pos[0] + x
            newy = self.pos[1]  + y
        else:
            self.diagAccum += 1
            if self.diagAccum > 1.414213562373095:
                self.diagAccum -= 1.414213562373095
                newx = self.pos[0] + x
                newy = self.pos[1]  + y
            else:
                newx = self.pos[0]
                newy = self.pos[1]
        if newx < 0 or newx > 39:
            self.killed = True
            return
        if newy < 0 or newy > 39:
            self.killed = True
            return
        if gamestate.EnemyOnPos(newx, newy):
            self.killed = True
            gamestate.KillEnemy(newx, newy)
            return
        if gamestate.PosBlocked(newx, newy):
            self.killed = True
            return
        self.pos = [newx, newy]
        self.AddGraphic()

    def destroy(self):
        super(Shot, self).destroy()
        self.RemoveGraphic()

class Laser(DestroyInterface):
    def __init__(self, x, y, facing):
        super(Laser, self).__init__()
        self.pos = [x,y]
        self.source = [x,y]
        self.facing = facing
        self.AddGraphic()
        self.killed = False
        self.diagAccum = 0

        if gamestate.EnemyOnPos(*self.pos):
            self.killed = True
            gamestate.KillEnemy(newx, newy)

    @property
    def graphicWidth(self):
        if self.facing == UP or self.facing == DOWN:
            return 3
        else:
            return abs(self.pos[0] - self.source[0])+1

    @property
    def graphicHeight(self):
        if self.facing == UP or self.facing == DOWN:
            return abs(self.pos[1] - self.source[1])+1
        else:
            return 3

    @property
    def graphicOrigin(self):
        if self.facing == UP:
            return [self.source[0]-1, self.source[1]]
        elif self.facing == DOWN:
            return [self.pos[0]-1, self.pos[1]]
        elif self.facing == LEFT:
            return [self.pos[0], self.pos[1]-1]
        else:
            return [self.source[0], self.source[1]-1]

    @property
    def encompassedTiles(self):
        tiles = []
        for x in range(self.graphicWidth):
            for y in range(self.graphicHeight):
                tiles.append([self.graphicOrigin[0]+x, self.graphicOrigin[1]+y])
        return tiles

    def AddGraphic(self):
        AGE.SetTile(LASER_TILES[self.facing], SHOT_LAYER, *self.graphicOrigin, width=self.graphicWidth, height=self.graphicHeight, highlight_color = COLOR_DARK_GREEN)

    def RemoveGraphic(self):
        AGE.RemoveTile(SHOT_LAYER, *self.graphicOrigin, width=self.graphicWidth, height=self.graphicHeight)

    def run(self):
        self.Move()

    def Move(self):
        #self.RemoveGraphic()
        if self.facing == UP:
            x, y = 0,1
        elif self.facing == DOWN:
            x, y = 0,-1
        elif self.facing == RIGHT:
            x, y = 1,0
        elif self.facing == LEFT:
            x, y = -1,0
        elif self.facing == UP_LEFT:
            x, y = -1,1
        elif self.facing == UP_RIGHT:
            x, y = 1,1
        elif self.facing == DOWN_LEFT:
            x, y = -1,-1
        elif self.facing == DOWN_RIGHT:
            x, y = 1,-1
        if self.facing in [UP, DOWN, RIGHT, LEFT]:
            newx = self.pos[0] + x
            newy = self.pos[1]  + y
        else:
            self.diagAccum += 1
            if self.diagAccum > 1.414213562373095:
                self.diagAccum -= 1.414213562373095
                newx = self.pos[0] + x
                newy = self.pos[1]  + y
            else:
                newx = self.pos[0]
                newy = self.pos[1]
        if newx < 0 or newx > 39:
            self.killed = True
            return
        if newy < 0 or newy > 39:
            self.killed = True
            return
        for tile in self.encompassedTiles:
            if gamestate.EnemyOnPos(*tile):
                gamestate.KillEnemy(*tile)
        self.pos = [newx, newy]
        self.AddGraphic()

    def destroy(self):
        super(Laser, self).destroy()
        self.RemoveGraphic()