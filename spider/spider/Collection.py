import os
from .SpiderElement import *
from .utils import *

class Collection(SpiderElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.parentPath = kwargs.get('parentPath', None)

        if kwargs.get('read_from_file', None) == None:
            if self.parentPath != None:
                self.path = self.setPath(self.parentPath, kwargs.get('collectionType', "node"))
                setattr(self, "identifier", self.path)

        if kwargs.get('read_from_file', None) != None:
            self.read(kwargs.get('read_from_file'))
        
        self.write()
    
    def __str__(self):
        return super().__str__()

    def write(self):
        writeJson(self.collectData(), os.path.join(self.path, "collection.json"))
        writeJson({"items" : []}, os.path.join(self.path, "content.json"))

    def read(self, path):
        readData = readJson(path)
        super().setFromReadData(readData)

    def setPath(self, path, collectiontype):
        folderName = "node_collections/"
        if collectiontype == "edge":
            folderName = "edge_collections/"
        makeDirsRecustive([
            os.path.join(path, folderName + str(self.uuid))
        ])
        return os.path.join(path, folderName + str(self.uuid))

    def addContent(self, toAdd):
        contentData = readJson(os.path.join(self.path, "content.json"))
        if isinstance(toAdd, str):
            if toAdd not in contentData["items"]:
                contentData["items"].append(toAdd)
        elif isinstance(toAdd, list):
            for item in toAdd:
                if item not in contentData["items"]:
                    contentData["items"].append(item)
        writeJson(contentData, os.path.join(self.path, "content.json"))

    def contentToList(self):
        return readJson(os.path.join(self.path, "content.json"))["items"]