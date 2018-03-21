# -*- coding: utf-8 -*-

import pyglet

#event priorities
KEY_DRIVER_PRIORITY = 100000

KEY_X = 0
KEY_Y = 1
KEY_A = 2
KEY_B = 3
KEY_UP = 4
KEY_DOWN = 5
KEY_LEFT = 6
KEY_RIGHT = 7
KEY_MOUSE_LEFT = 8
KEY_MOUSE_RIGHT = 9

DEFAULT_KEY_X = {pyglet.window.key.Z}
DEFAULT_KEY_Y = {pyglet.window.key.V}
DEFAULT_KEY_A = {pyglet.window.key.X}
DEFAULT_KEY_B = {pyglet.window.key.C}
DEFAULT_KEY_UP = {pyglet.window.key.UP, pyglet.window.key.W}
DEFAULT_KEY_DOWN = {pyglet.window.key.DOWN, pyglet.window.key.S}
DEFAULT_KEY_LEFT = {pyglet.window.key.LEFT, pyglet.window.key.A}
DEFAULT_KEY_RIGHT = {pyglet.window.key.RIGHT, pyglet.window.key.D}
DEFAULT_KEY_MOUSE_LEFT = {pyglet.window.mouse.LEFT}
DEFAULT_KEY_MOUSE_RIGHT = {pyglet.window.mouse.RIGHT}

KEY_BINDS = {KEY_X:DEFAULT_KEY_X, KEY_Y:DEFAULT_KEY_Y, KEY_A:DEFAULT_KEY_A, KEY_B:DEFAULT_KEY_B,
        KEY_UP:DEFAULT_KEY_UP, KEY_DOWN:DEFAULT_KEY_DOWN, KEY_LEFT:DEFAULT_KEY_LEFT, KEY_RIGHT:DEFAULT_KEY_RIGHT, 
        KEY_MOUSE_LEFT:DEFAULT_KEY_MOUSE_LEFT, KEY_MOUSE_RIGHT:DEFAULT_KEY_MOUSE_RIGHT}