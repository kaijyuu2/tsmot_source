# -*- coding: utf-8 -*-

from kaiengine.gconfig import *
from .keys import *

GAME_CAPTION = "There's So Many Of Them!"

DYNAMIC_SETTINGS_DEFAULTS = {DYNAMIC_SETTINGS_GAME_CAPTION: GAME_CAPTION, #overwrite defaults here
                    DYNAMIC_SETTINGS_WINDOW_DIMENSIONS: [480, 480],
                    DYNAMIC_SETTINGS_FRAMES_PER_SECOND: 20.0}


GRASS_LAYER = .5
MAP_LAYER = 1
KILL_COUNTER_LAYER = 1.5
PLAYER_LAYER = 2
ENEMY_LAYER = 2.5
SHOT_LAYER = 3



#facing
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
UP_LEFT = 4
UP_RIGHT = 5
DOWN_LEFT = 6
DOWN_RIGHT = 7

SHOT_TILES = {UP:[8,14],
            DOWN:[9,14],
            LEFT:[11,14],
            RIGHT:[10,14],
            UP_LEFT:[8, 14],
            UP_RIGHT:[8, 14],
            DOWN_LEFT:[9, 14],
            DOWN_RIGHT:[9, 14]}

LASER_TILES = {UP:[10,4],
            DOWN:[10,4],
            LEFT:[13,3],
            RIGHT:[13,3]}

