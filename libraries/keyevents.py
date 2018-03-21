# -*- coding: utf-8 -*-

import kaiengine.event as event
from kaiengine.keybinds import *
from libraries.config import *


keydriver = None

def InitKeys():
    global keydriver
    keydriver = KeyDriver()
    addBoundKeyDict(KEY_BINDS)
    
def RefreshKeys():
    keydriver.RefreshKeys()
    
def KeyPressed(key):
    return keydriver.KeyPressed(key)
    
def KeyReleased(key):
    return keydriver.KeyReleased(key)
    
def KeyHeld(key):
    return keydriver.KeyHeld(key)
    
class KeyDriver(object):
    def __init__(self):
        self.keys_held = set()
        self.keys_pressed = set()
        self.keys_released = set()
        event.addKeyPressListener(self.EventKeyPressed, KEY_DRIVER_PRIORITY)
        event.addKeyReleaseListener(self.EventKeyReleased , KEY_DRIVER_PRIORITY)
        
    def EventKeyPressed(self, symbol, modifiers):
        if symbol is not None:
            self.keys_pressed.add(symbol)
            self.keys_held.add(symbol)
    
    def EventKeyReleased(self, symbol, modifiers):
        if symbol is not None:
            self.keys_released.add(symbol)
            self.keys_pressed.discard(symbol)
            self.keys_held.discard(symbol)
    
    def RefreshKeys(self):
        self.keys_pressed.clear()
        self.keys_released.clear()
        
    def KeyPressed(self, key):
        try: return KEY_BINDS[key] & self.keys_pressed
        except KeyError: return False
        
    def KeyReleased(self, key):
        try: return KEY_BINDS[key] & self.keys_released
        except KeyError: return False
        
    def KeyHeld(self, key):
        try: return KEY_BINDS[key] & self.keys_held
        except KeyError: return False