from direct.showbase.Loader import Loader
from direct.actor.Actor import Actor

class GameLoader():

    textures = {}
    tracks = {}
    models = {}
    loader = Loader('loader')


def loadModel(filename):
    return GameLoader.loader.loadModel(filename)

def loadTexture(filename):
    texture = None

    try:
       texture = textures[filename]
    except KeyError:
       texture = GameLoader.loader.loadTexture('tex/%s.ogg' % (filename) )
       GameLoader.textures[filename] = texture

    return texture

def loadMusic(filename):
    track = None

    try:
       track = tracks[filename]
    except KeyError:
       track = GameLoader.loader.loadMusic('music/%s' % (filename) )
       GameLoader.tracks[filename] = track

    return track

