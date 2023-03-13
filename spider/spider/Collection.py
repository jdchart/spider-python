import os
import csv
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
        writeJson({"items" : []}, os.path.join(path, folderName + str(self.uuid), "content.json"))
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

    def removeContent(self, toRemove):
        contentData = readJson(os.path.join(self.path, "content.json"))["items"]
        if isinstance(toRemove, str):
            toRemove = [toRemove]
        for item in toRemove:
            contentData.remove(item) 
        writeJson({"items" : contentData}, os.path.join(self.path, "content.json"))

    def collectionToCSV(self, web, path, **kwargs):
        # TODO : a collection should have its web itself
        toKeep = kwargs.get("fields", [])
        with open(path, 'w', newline = '') as file:
            writer = csv.writer(file)

            nodeList = self.contentToList()

            keyList = list(web.loadNode(nodeList[0]).__dict__.keys())
            
            formattedKeyList = []
            for item in keyList:
                if self.checkIfKeep(item, toKeep):
                    if item[0] == "_":
                        formattedKeyList.append(item.replace("_", ""))
                    elif item in ["relation", "coverage", "format", "instructionalMethod"]:
                        thisModifiedField = getattr(web.loadNode(nodeList[0]), item)
                        modifKeyList = list(thisModifiedField.__dict__.keys())
                        for modifKey in modifKeyList:
                            formattedKeyList.append(item + "_" + modifKey)
                    elif item != "specials":
                        formattedKeyList.append(item)
                    
            writer.writerow(formattedKeyList)

            for item in nodeList:
                thisItem = web.loadNode(item)
                writeList = []
                for field in keyList:
                    if self.checkIfKeep(field, toKeep):
                        if field[0] == "_":
                            #writeList.append(getattr(thisItem, field.replace("_", "")))
                            writeList.append(thisItem.getFromLang(field.replace("_", ""), "full"))
                        elif field in ["relation", "coverage", "format", "instructionalMethod"]:
                            thisModifiedField = getattr(thisItem, field)
                            modifKeyList = list(thisModifiedField.__dict__.keys())
                            for modifKey in modifKeyList:
                                writeList.append(getattr(thisModifiedField, modifKey))
                        elif field != "specials":
                            writeList.append(getattr(thisItem, field))

                writer.writerow(writeList)

    def checkIfKeep(self, item, toKeep):
        if toKeep == []:
            return True
        else:
            if item[0] == "_":
                keyModified = item.replace("_", "")
                if keyModified in toKeep:
                    return True
                else:
                    return False
            else:
                if item in toKeep:
                    return True
                else:
                    return False