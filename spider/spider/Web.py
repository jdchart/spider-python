import os
from .SpiderElement import *
from .Node import *
from .Edge import *
from .utils import *

class Web(SpiderElement):
    def __init__(self, **kwargs):
        super().__init__(
            format = {
                "type" : "dataCollection",
                "fileFormat" : "json",
            },
            **kwargs
        )

        if kwargs.get('path', None) != None or kwargs.get('identifier', None) != None:
            if kwargs.get('path', None) != None:
                setattr(self, "identifier", kwargs.get('path'))
                self.path = kwargs.get('path')
            elif kwargs.get('identifier', None) != None:
                self.path = kwargs.get('identifier')
            else:
                self.path = os.getcwd()
                setattr(self, "identifier", os.getcwd())

        if kwargs.get('read_from_file', None) == None:
            self.setPath(self.path)
        
        if kwargs.get('read_from_file', None) != None:
            self.read(kwargs.get('read_from_file'))
        
        self.write()
    
    def __str__(self):
        return super().__str__()

    def write(self):
        writeJson(self.collectData(), os.path.join(self.path, "metadata.json"))

    def read(self, path):
        readData = readJson(os.path.join(path, "metadata.json"))
        super().setFromReadData(readData)

    def setPath(self, path):
        makeDirsRecustive([
            path,
            os.path.join(path, "web/nodes"),
            os.path.join(path, "web/edges"),
            os.path.join(path, "cytoscape"),
            os.path.join(path, "mirador/lower")
        ])
        return path

    def addNode(self, metadata):
        newNode = Node(parentPath = os.path.join(self.path, "web"), **metadata)
        return newNode

    def loadNode(self, searchTerm, **kwargs):
        searchKey = kwargs.get('term', "uuid")
        nodePath = findElement(os.path.join(self.path, "web/nodes"), searchTerm, searchKey, "node")
        loadedNode = Node(read_from_file = nodePath)
        return loadedNode

    def addEdge(self, metadata):
        newEdge = Edge(parentPath = os.path.join(self.path, "web"), **metadata)
        return newEdge

    def loadEdge(self, searchTerm, **kwargs):
        searchKey = kwargs.get('term', "uuid")
        edgePath = findElement(os.path.join(self.path, "web/edges"), searchTerm, searchKey, "edge")
        loadedEdge = Node(read_from_file = edgePath)
        return loadedEdge