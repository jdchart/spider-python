import os
import shutil
from .SpiderElement import *
from .Node import *
from .Edge import *
from .Collection import *
from .Network import *
from .utils import *
from .mediaConvert import *
from .IIIF import *

class Web(SpiderElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
            os.path.join(path, "web/node_collections"),
            os.path.join(path, "web/edge_collections"),
            os.path.join(path, "media")
        ])
        makeGitignoreFile(os.path.join(path, ".gitignore"), ["media"])
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
        loadedEdge = Edge(read_from_file = edgePath)
        return loadedEdge

    def addCollection(self, collectionType, metadata):
        newCollection = Collection(parentPath = os.path.join(self.path, "web"), collectionType = collectionType, **metadata)
        return newCollection

    def loadCollection(self, searchTerm, **kwargs):
        searchKey = kwargs.get('term', "uuid")
        collectionPath = findElement(os.path.join(self.path, "web"), searchTerm, searchKey, "collection")
        loadedCollection = Collection(read_from_file = collectionPath)
        return loadedCollection

    def mediaToNode(self, mediaPath, copyMedia):
        if copyMedia == True:
            shutil.copyfile(mediaPath, os.path.join(self.path, "media/" + os.path.basename(mediaPath)))
            mediaPath = os.path.join(self.path, "media/" + os.path.basename(mediaPath))

        mediaData = getMediaData(mediaPath)
        if mediaData != None:
            mediaNode = Node(
                parentPath = os.path.join(self.path, "web"),
                **mediaData
            )
            return mediaNode

    def printContent(self, type, printKey):
        for root, dirs, files in os.walk(os.path.join(self.path, "web/" + type)):
            for dir in dirs:
                if dir != type:
                    node = self.loadNode(dir)
                    print()
                    for key in printKey:
                        print(key + ": " + str(getattr(node, key)))

    def getFullList(self, type):
        fullList = []
        for root, dirs, files in os.walk(os.path.join(self.path, "web/" + type)):
            for dir in dirs:
                if dir != type:
                    fullList.append(dir)
        return fullList

    def convertToMemoRekall(self, **kwargs):
        nodeList = kwargs.get("nodeList", self.getFullList("nodes"))
        edgeList = kwargs.get("edgeList", self.getFullList("edges"))
        webToManifestNetwork(
            self, 
            nodeList = nodeList,
            edgeList = edgeList,
            **kwargs
        )

    def convertToNetwork(self, **kwargs):
        newNetwork = webToNetworkX(self, **kwargs)
        return newNetwork