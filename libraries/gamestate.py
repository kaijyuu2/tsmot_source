# -*- coding: utf-8 -*-

#game driver

from libraries.config import *

from kaiengine.destroyinterface import DestroyInterface
from kaiengine.sDict import sDict
from kaiengine.timer import Timer
import AGE

import random


def PosBlocked(x, y):
    return glob.PosBlocked(x, y)

def EnemyOnPos(x, y):
    return glob.EnemyOnPos(x, y)

def PlayerOnPos(x, y):
    return glob.PlayerOnPos(x, y)

def ShotOnPos(x, y):
    return glob.ShotOnPos(x, y)

def GetPlayerPos():
    return glob.GetPlayerPos()

def KillEnemy(x, y):
    glob.KillEnemy(x, y)

def SpawnShot(facing, x, y):
    glob.SpawnShot(facing, x, y)

def SpawnMultiShot(facing, x, y):
    glob.SpawnMultiShot(facing, x, y)

def SpawnLaser(facing, x, y):
    glob.SpawnLaser(facing, x, y)

def PlayerHit():
    glob.ResetGame()


def close():
    global glob
    if glob is not None:
        glob.destroy()
        glob = None

class GameState(DestroyInterface):
    def __init__(self):
        super(GameState, self).__init__()
        from .killcounter import KillCounter
        self.doodads = {}
        self.player = None
        self.enemies = sDict()
        self.shots = sDict()
        self.difficulty = 1
        self.killcount = KillCounter()

        self.gametime = Timer()
        self.spawntimer = Timer()

    def init(self):
        from .tree import Tree
        from .player import Player
        for i in range(100): #add trees:
            while(True):
                x = random.randint(0,39)
                y = random.randint(0,39)
                pos = (x,y)
                if pos == (20,20): #player start pos
                    continue
                if pos in self.doodads: #already a tree here
                    continue
                self.doodads[pos] = Tree(x, y)
                break
        self.player = Player(20,20)
        self.gametime.start()
        self.spawntimer.stopTimer()
        self.difficulty = 1
        self.killcount.Reset()

    def ResetGame(self):
        for doodad in self.doodads.values():
            doodad.destroy()
        self.doodads.clear()
        for shot in self.shots.values():
            shot.destroy()
        self.shots.clear()
        for enemy in self.enemies.values():
            enemy.destroy()
        self.enemies.clear()
        self.player.destroy()
        self.init()

    def run(self):
        self.difficulty = (int(self.gametime.check_time()) / 10) + 1
        if self.player is not None:
            self.player.run()
        for key, shot in list(self.shots.items()):
            shot.run()
            if shot.killed:
                shot.destroy()
                del self.shots[key]
        for enemy in list(self.enemies.values()):
            enemy.run()
        if not self.spawntimer.started or self.spawntimer.checkCountdown():
            self.SpawnEnemy()
            self.spawntimer.countdownStart(5.0 / self.difficulty)



    def PosBlocked(self, x, y):
        key = (x,y)
        if key in self.doodads:
            return True
        return self.EnemyOnPos(x, y)

    def EnemyOnPos(self, x, y):
        key = (x, y)
        for enemy in self.enemies.values():
            if key == tuple(enemy.pos):
                return True
        return False

    def PlayerOnPos(self, x, y):
        if self.player is not None:
            if list(self.player.pos) == [x, y]:
                return True
        return False

    def GetPlayerPos(self):
        try:
            return self.player.pos
        except AttributeError:
            return [0,0]

    def SpawnEnemy(self):
        from libraries.enemy import Enemy
        while(True):
            side = random.randint(0,3)
            if side == UP:
                pos = [random.randint(0,39),39]
            elif side == DOWN:
                pos = [random.randint(0,39),0]
            elif side == RIGHT:
                pos = [39,random.randint(0,39)]
            else:
                pos = [0,random.randint(0,39)]
            if self.PosBlocked(*pos):
                continue
            self.enemies.append(Enemy(pos[0], pos[1], self.difficulty))
            break

    def KillEnemy(self, x, y):
        for key, enemy in self.enemies.items():
            if [x,y] == list(enemy.pos):
                enemy.destroy()
                del self.enemies[key]
                break
        self.killcount.Add()

    def SpawnShot(self, facing, x, y):
        if x >= 0 and x <= 39 and y >= 0 and y <= 39:
            from .shot import Shot
            index = self.shots.append(Shot(x, y, facing))
            if self.shots[index].killed:
                self.shots[index].destroy()
                del self.shots[index]

    def SpawnMultiShot(self, facing, x, y):
        if x >= 0 and x <= 39 and y >= 0 and y <= 39:
            from .shot import Shot
            for shotFacing in {UP:[UP, UP_LEFT, UP_RIGHT],LEFT:[LEFT,UP_LEFT,DOWN_LEFT],RIGHT:[RIGHT,UP_RIGHT,DOWN_RIGHT],DOWN:[DOWN,DOWN_LEFT,DOWN_RIGHT]}[facing]:
                index = self.shots.append(Shot(x, y, shotFacing))
                if self.shots[index].killed:
                    self.shots[index].destroy()
                    del self.shots[index]

    def SpawnLaser(self, facing, x, y):
        if x >= 0 and x <= 39 and y >= 0 and y <= 39:
            from .shot import Laser
            index = self.shots.append(Laser(x, y, facing))
            if self.shots[index].killed:
                self.shots[index].destroy()
                del self.shots[index]

    def destroy(self):
        super().destroy()
        for key, doodad in list(self.doodads.items()):
            doodad.destroy()
            del self.doodads[key]
        for key, enemy in list(self.enemies.items()):
            enemy.destroy()
            del self.enemies[key]
        for key, shot in list(self.shots.items()):
            shot.destroy()
            del self.shots[key]
        if self.player is not None:
            self.player.destroy()
            self.player = None
        if self.killcount is not None:
            self.killcount.destroy()
            self.killcount = None

glob = GameState()