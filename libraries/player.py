# -*- coding: utf-8 -*-


import AGE
from kaiengine.destroyinterface import DestroyInterface

from libraries import keyevents
from libraries import gamestate
from libraries.config import *


class Player(DestroyInterface):
    def __init__(self, x, y):
        super(Player, self).__init__()
        self.pos = [x,y]
        self._displayed = False
        self.AddGraphic()
        self.last_facing_direction = DOWN


    def run(self):
        self.CheckKeyPresses()

    def CheckKeyPresses(self):
        if keyevents.KeyHeld(KEY_UP):
            self.Move(0,1)
            self.last_facing_direction = UP
        if keyevents.KeyHeld(KEY_DOWN):
            self.Move(0,-1)
            self.last_facing_direction = DOWN
        if keyevents.KeyHeld(KEY_RIGHT):
            self.Move(1,0)
            self.last_facing_direction = RIGHT
        if keyevents.KeyHeld(KEY_LEFT):
            self.Move(-1,0)
            self.last_facing_direction = LEFT
        if keyevents.KeyPressed(KEY_X):
            gamestate.SpawnShot(self.last_facing_direction, *self.pos)
        if keyevents.KeyPressed(KEY_A):
            gamestate.SpawnMultiShot(self.last_facing_direction, *self.pos)
        if keyevents.KeyPressed(KEY_B):
            gamestate.SpawnLaser(self.last_facing_direction, *self.pos)

    def AddGraphic(self):
        if not self._displayed:
            AGE.SetTile([1,15], PLAYER_LAYER, *self.pos, highlight_color = COLOR_DARK_GREEN)
            self._displayed = True

    def RemoveGraphic(self):
        if self._displayed:
            AGE.RemoveTile(PLAYER_LAYER, *self.pos)
            self._displayed = False

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
        if gamestate.EnemyOnPos(*self.pos):
            gamestate.PlayerHit()


    def destroy(self):
        super(Player, self).destroy()
        self.RemoveGraphic()