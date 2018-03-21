# -*- coding: utf-8 -*-

import math
import random

import AGE
from kaiengine.destroyinterface import DestroyInterface
from kaiengine.timer import Timer

from libraries import gamestate
from libraries.config import *

class Enemy(DestroyInterface):
    def __init__(self, x, y, power):
        super(Enemy, self).__init__()
        self.pos = [x,y]
        self._displayed = False
        self.power = power
        self.movementtimer = Timer()
        self.movementtimer.start()

        self.AddGraphic()

    def AddGraphic(self):
        if not self._displayed:
            AGE.SetTile([2,15], ENEMY_LAYER, self.pos[0], self.pos[1], color = COLOR_RED, highlight_color = COLOR_DARK_GREEN)
            self._displayed = True

    def RemoveGraphic(self):
        if self._displayed:
            AGE.RemoveTile(ENEMY_LAYER, *self.pos)
            self._displayed = False

    def run(self):
        if self.movementtimer.check_time() > 1.0 / self.power :
            if random.randint(0,99) >= 10:
                pos = gamestate.GetPlayerPos()
                xdistance = pos[0] - self.pos[0]
                ydistance = pos[1] - self.pos[1]
            else:
                xdistance = random.randint(-50,50)
                ydistance = random.randint(-50,50)
            if abs(xdistance) > abs(ydistance):
                self.Move(math.copysign(1,xdistance), 0)
            else:
                self.Move(0, math.copysign(1,ydistance))
            self.movementtimer.start()

    def Move(self, x, y):
        self.RemoveGraphic()
        x = self.pos[0] + x
        if gamestate.PosBlocked(x, self.pos[1]):
            x = self.pos[0]
        if x < 0:
            x = 0
        elif x > 39: #fuck making this support larger map sizes
            x = 39
        y = self.pos[1] + y
        if gamestate.PosBlocked(x, y):
            y = self.pos[1]
        if y < 0:
            y = 0
        elif y > 39:
            y = 39
        self.pos = [x,y]
        self.AddGraphic()
        if gamestate.PlayerOnPos(*self.pos):
            gamestate.PlayerHit()


    def destroy(self):
        super(Enemy, self).destroy()
        self.RemoveGraphic()