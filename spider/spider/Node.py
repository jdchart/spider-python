import os
from .SpiderElement import *
from .utils import *

class Node(SpiderElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.parentPath = kwargs.get('parentPath', None)

        self.startDateTime = kwargs.get('startDateTime', None)
        self.endDateTime = kwargs.get('endDateTime', None)
        self.modificationDateTimes = kwargs.get('modificationDateTimes', [])
        self.media = kwargs.get('media', None)

        if kwargs.get('read_from_file', None) == None:
            if self.parentPath != None:
                self.path = self.setPath(self.parentPath)

        if kwargs.get('read_from_file', None) != None:
            self.read(kwargs.get('read_from_file'))
        
        self.write()
    
    def __str__(self):
        return super().__str__()

    def write(self):
        writeJson(self.collectData(), os.path.join(self.path, "node.json"))

    def read(self, path):
        readData = readJson(path)
        super().setFromReadData(readData)

    def collectData(self):
        dataObj = super().collectData()
        dataObj["startDateTime"] = self.startDateTime.strftime("%m-%d-%Y:%H:%M:%S")
        dataObj["endDateTime"] = self.startDateTime.strftime("%m-%d-%Y:%H:%M:%S")
        finalArray = []
        for date in self.modificationDateTimes:
            finalArray.append(date.strftime("%m-%d-%Y:%H:%M:%S"))
        dataObj["modificationDateTimes"] = finalArray
        return dataObj
    
    def setPath(self, path):
        makeDirsRecustive([
            os.path.join(path, "nodes/" + str(self.uuid)),
            os.path.join(path, "nodes/" + str(self.uuid) + "/nodes")
        ])
        return os.path.join(path, "nodes/" + str(self.uuid))
    
    def addNode(self, metadata):
        newNode = Node(parentPath = self.path, **metadata)
        return newNode

    def loadNode(self, searchTerm, **kwargs):
        searchKey = kwargs.get('term', "uuid")
        nodePath = findElement(self.path, searchTerm, searchKey, "node")
        loadedNode = Node(read_from_file = nodePath)
        return loadedNode