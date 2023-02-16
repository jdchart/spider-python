import os
from .SpiderElement import *
from .utils import *

class Edge(SpiderElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.parentPath = kwargs.get('parentPath', None)

        if kwargs.get('read_from_file', None) == None:
            if self.parentPath != None:
                self.path = self.setPath(self.parentPath)
                setattr(self, "identifier", self.path)

        if kwargs.get('read_from_file', None) != None:
            self.read(kwargs.get('read_from_file'))
        
        self.write()
    
    def __str__(self):
        return super().__str__()

    def write(self):
        writeJson(self.collectData(), os.path.join(self.path, "edge.json"))

    def read(self, path):
        readData = readJson(path)
        super().setFromReadData(readData)

    def setPath(self, path):
        makeDirsRecustive([
            os.path.join(path, "edges/" + str(self.uuid))
        ])
        return os.path.join(path, "edges/" + str(self.uuid))