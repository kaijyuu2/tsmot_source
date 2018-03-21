


from . import driver

def InitGame():
    """does everything necessary to initialize the game"""
    driver.InitDriver()

def Close():
    driver.CloseDriver()

def SetMapDimensions(width, height):
    _GetMap().SetDimensions(width, height)

def GetMapDimensions():
    return _GetMap().GetDimensions()

def SetTile(value, layer, x, y, width = 1, height = 1, color = None, highlight_color = -1):
    _GetMap().SetTile(value, layer, x, y, width, height, color, highlight_color)
    return [layer, x, y, width, height] #return data about what was drawn (intended for later removal, though maybe for other things too)

def SetTileColor(color, layer, x, y, width = 1, height = 1):
    _GetMap().SetTileColor(color, layer, x, y, width, height)

def SetTileHighlight(color, layer, x, y, width = 1, height = 1):
    _GetMap().SetTileHighlight(color, layer, x, y, width, height)

def DrawString(string, layer, x, y, color = None, highlight_color = -1):
    _GetMap().DrawString(string, layer, x, y, color, highlight_color)
    return [layer, x, y, len(string), 1] #return some information about the drawn string (layer, origin, length, and height) intended for use in removal

def RemoveTile(layer, x, y, width = 1, height = 1, swapcoordinates=False):
    if swapcoordinates: x, y = y, x
    _GetMap().RemoveTile(layer, x, y, width, height)

def SetBackgroundColor(color):
    driver.Driver.SetBackgroundColor(color)

def ClearLayer(*args, **kwargs):
    _GetMap().ClearLayer(*args, **kwargs)

def ClearScreen(): #won't reset the background color'
    _GetMap().ClearScreen()

def GetTileIndex(layer, x, y):
    return _GetMap().GetTile(x,y).GetTileIndex(layer)

def GetTileColor(layer, x, y):
    return _GetMap().GetTile(x,y).GetTileColor(layer)

def LoadStripeImage(filepath = None):
    from .stripeimage import StripeImage
    return StripeImage(filepath)

def CreateStripeFromData(data):
    from .stripeimage import StripeImage
    stripe = StripeImage()
    stripe.CreateFromData(data)
    return stripe

def ChangeGlyphsData(*args, **kwargs):
    '''sets filepath and/or dimesions of glyphs'''
    driver.Driver.SetGlyphData(*args, **kwargs)

def ChangeGlyphsSource(*args, **kwargs):
    '''sets filepath of glyphs'''
    driver.Driver.SetGlyphData(*args, **kwargs)

def ChangeGlyphsTileSize(*args, **kwargs):
    '''sets dimesions of glyphs'''
    driver.Driver.SetGlyphData(None, *args, **kwargs)

def GetGlyphFilepath():
    return driver.Driver.GetGlyphFilepath()

def GetGlyphColumnsRows():
    return driver.Driver.GetGlyphsColumnsRows()

def GetGlyphSize():
    return driver.Driver.GetGlyphSize()

def FadeIn(*args, **kwargs):
    _GetDarkener().FadeIn(*args, **kwargs)

def FadeOut(*args, **kwargs):
    _GetDarkener().FadeOut(*args, **kwargs)

def StopFade(*args, **kwargs):
    _GetDarkener().StopFade(*args, **kwargs)

def InstantFadeIn(*args, **kwargs):
    _GetDarkener().InstantFadeIn(*args, **kwargs)

def InstantFadeOut(*args, **kwargs):
    _GetDarkener().InstantFadeOut(*args, **kwargs)

def SetDarkenerAlpha(*args, **kwargs):
    if not "override_flicker" in list(kwargs.keys()):
        kwargs["override_flicker"] = True
    _GetDarkener().SetAlpha(*args,**kwargs)


#internal use only. Do not use
def _GetMap():
    return driver.Driver.map

def _GetDarkener():
    return driver.Driver.darkener
