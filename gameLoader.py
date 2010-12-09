from direct.showbase.Loader import Loader
from direct.actor.Actor import Actor

class GameLoader():

    textures = {}
    models = {}
    tracks = {}

    def __init__(self):
        self.loader = Loader()

    def loadModel(self,filename):

        model = None

        try:
           model = models[filename]
        except:
            #model = loader.loadModel('model/%s' % filename)
            #models[filename] = model
            pass
        return model

    def loadTexture(self,filename):
        texture = None

        try:
           texture = textures[filename]
        except:
           texture = loader.loadTexture('tex/%s.ogg' % (filename) )
           textures[filename] = texture

        return texture

    def loadMusic(self,filename):
        track = None

        try:
           track = tracks[filename]
        except:
           track = self.loader.loadMusic('music/%s' % (filename) )
           tracks[filename] = track

        return track

gload = GameLoader()
#m = gload.loadMusic('ralph')

