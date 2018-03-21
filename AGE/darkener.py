

#darkener for AGE

from kaiengine.objectinterface import SchedulerInterface
from kaiengine.sprite import Sprite
from kaiengine.timer import FrameTimer
from kaiengine.resource import toStringPath

import os
import math

from .functions import *
from .constants import *

STANDARD_TYPE = 0
SCREEN_TEAR_TYPE = 1

FADE_IN = 0
FADE_OUT = 1



class Darkener(SchedulerInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fadetimer = FrameTimer()
        self.sprites = []
        for i in range(4):
            self.sprites.append(Sprite(toStringPath(os.path.dirname(__file__), RESOURCES_FOLDER, BACKGROUND_FILENAME), layer = DARKENER_LAYER))
            self.sprites[-1].alpha = 1.0
            self.sprites[-1].color = COLOR_BLACK[:3]

        self.type = SCREEN_TEAR_TYPE
        self.flicker = True
        self.last_frame_alpha = 1.0

        self.fading = False
        self.fading_mode = FADE_IN



    def _runFade(self):
        perc = self.fadetimer.getCountdownPercent()
        if self.fading_mode == FADE_OUT:
            alpha = 1.0 - perc
        else:
            alpha = perc
        self.SetAlpha(alpha)
        if perc <= 0.0:
            self.fading = False
            self.SetAlpha(alpha)
            self.Unschedule(self._runFade)

    def SetFadeType(self, fadetype):
        self.type = fadetype

    def FadeIn(self, time):
        self._Fade(time, FADE_IN)

    def FadeOut(self, time):
        self._Fade(time, FADE_OUT)

    def _Fade(self, time, fadetype):
        self.fading_mode = fadetype
        self.fadetimer.countdownStart(time)
        self.fading = True
        self.ScheduleUnique(self._runFade, 1, True)

    def StopFade(self, fadetype = None):
        if fadetype == None:
            fadetype = self.fading_mode
        self.fadetimer.stopTimer()
        self.fading_mode = fadetype
        self._runFade()

    def InstantFadeIn(self):
        self.StopFade(FADE_IN)

    def InstantFadeOut(self):
        self.StopFade(FADE_OUT)

    def SetAlpha(self, alpha, override_flicker = False):
        original_alpha = alpha
        if self.flicker and not override_flicker:
            if alpha >= .875:
                alpha = 1.0
            elif alpha >= .625:
                alpha = .75
            elif alpha >= .375:
                alpha = .5
            elif alpha >= .125:
                alpha = .25
            else:
                alpha = 0.0
        if self.type == SCREEN_TEAR_TYPE and original_alpha > 0.0 and original_alpha < 1.0 :
            self.sprites[2].alpha = self.last_frame_alpha
            self.sprites[3].alpha = self.last_frame_alpha
        else:
            self.sprites[2].alpha = alpha
            self.sprites[3].alpha = alpha
        self.sprites[0].alpha = alpha
        self.sprites[1].alpha = alpha
        self.last_frame_alpha = alpha


    def UpdateSpritePos(self):
        map_dim = GetMapDimensions()
        glyph_dim = GetGlyphSize()
        big = [math.ceil(map_dim[0]/2) *glyph_dim[0], math.ceil(map_dim[1] /2) * glyph_dim[1]]
        small = [math.floor(map_dim[0]/2) * glyph_dim[0], math.floor(map_dim[1]/ 2) * glyph_dim[1]]
        topleft = big[:]
        topright = small[:]
        bottomleft = small[:]
        bottomright = big[:]
        if big[1] == small[1] and big[0] == small[0]:
            topleft = [topleft[0], topleft[1] + glyph_dim[1]]
            bottomleft = [bottomleft[0], bottomleft[1] - glyph_dim[1]]
        elif big[1] == small[1] and big[0] != small[0]:
            topleft = [big[0], big[1] + glyph_dim[1]]
            bottomleft = [small[0] + glyph_dim[0], small[1] - glyph_dim[1]]
            bottomright = [bottomright[0] - glyph_dim[0], bottomright[1]]
        self.sprites[0].set_dimensions(*topleft)
        self.sprites[1].set_dimensions(*topright)
        self.sprites[2].set_dimensions(*bottomleft)
        self.sprites[3].set_dimensions(*bottomright)
        self.sprites[0].setPos(0,bottomleft[1])
        self.sprites[1].setPos(topleft[0], bottomright[1])
        self.sprites[2].setPos(0,0)
        self.sprites[3].setPos(bottomleft[0], 0)

    def destroy(self):
        if Darkener:
            super(Darkener, self).destroy()
        for sprite in self.sprites:
            sprite.destroy()
        self.sprites = []
