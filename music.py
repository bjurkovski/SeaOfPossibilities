from direct.showbase.Loader import Loader
from direct.task import Task

class Music():
    def __init__(self,name):

        self.timer = 0
        self.name = name
        self.tracks = {}
        self.current = None

    def play(self):
        if self.current != None:
            self.getCurrent().play()
            self.getCurrent().setPlayRate(1)

    def stop(self):
        self.getCurrent().setPlayRate(0)

    def getTracks(self):
        return self.tracks.keys

    def setCurrent(self,cur):
        """
            Expects a string indicating
            what's the current track to be played
        """
        self.current = cur
        #sound starts playing here, I know it's crazy
        self.getCurrent().setTime(self.timer)

    def getCurrent(self):
        """
            Returns the current sound object
            that is being played
        """
        return self.tracks[self.current]


    def addTrack(self,track):
        t = self.tracks[track] = loader.loadMusic('music/%s.ogg' % (track) )
        t.setLoop(True)

    def setTimer(self,param):

        if (self.current != None):
            self.timer = self.getCurrent().getTime()
        return Task.cont

