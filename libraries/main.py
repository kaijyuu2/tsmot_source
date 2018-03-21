# -*- coding: utf-8 -*-

from libraries.config import *
from kaiengine import settings
settings.initialize(DYNAMIC_SETTINGS_DEFAULTS) #can change in config's __init__
#done very early here to allow access to settings in initialization of imported modules
from . import gamestate
from . import keyevents

import AGE 
from kaiengine import display
from kaiengine import event
from kaiengine.debug import debugMessage, checkDebugOn
from kaiengine.gameframehandler import  initializeGameFrames, closeGameFrames
from kaiengine.setup import *


def init():
    event.addGameCloseListener(close)

    if checkDebugOn():
        debugMessage("WARNING: Launching in debug mode")
    setupWindowBasic("logo.png")

    setupDrivers()
    keyevents.InitKeys()
    AGE.InitGame()
    
    AGE.SetMapDimensions(40,40)
    AGE.SetTile([10,0], GRASS_LAYER, 0, 0, 40, 40, COLOR_GREEN, COLOR_DARK_GREEN) # fill with grass
    AGE.InstantFadeIn()
    
    gamestate.glob.init()
    #AGE.SetBackgroundColor(COLOR_DARK_GREEN)
    


    initializeGameFrames(main_loop)

def main_loop(dt):
    gamestate.glob.run()
    keyevents.RefreshKeys()

def close():
    gamestate.close()
    AGE.Close()
    closeGameFrames()
    settings.saveToFile()