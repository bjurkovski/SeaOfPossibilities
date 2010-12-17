from direct.showbase.Loader import Loader
from direct.actor.Actor import Actor

class GameLoader():

    music = None
    textures = {}
    tracks = {}
    models = {}
    sfx = {}
    loader = Loader('loader')


def loadModel(filename):
    return GameLoader.loader.loadModel(filename)

def loadTexture(filename):
    texture = None

    try:
       texture = GameLoader.textures[filename]
    except KeyError:
       texture = GameLoader.loader.loadTexture('tex/%s' % (filename) )
       GameLoader.textures[filename] = texture

    return texture

def loadMusic(filename):
    track = None

    try:
       track = GameLoader.tracks[filename]
    except KeyError:
       track = GameLoader.loader.loadMusic('music/%s' % (filename) )
       GameLoader.tracks[filename] = track

    return track

def loadSfx(filename):
    sfx = None

    try:
       sfx = GameLoader.sfx[filename]
    except KeyError:
       sfx = GameLoader.loader.loadSfx('sfx/%s' % (filename) )
       GameLoader.sfx[filename] = sfx

    return sfx

