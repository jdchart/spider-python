import os
import csv
import copy
from .SpiderElement import *
from .utils import *

class Collection(SpiderElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.parentPath = kwargs.get('parentPath', None)
        self.collectionType = kwargs.get('collectionType', "node")

        if kwargs.get('read_from_file', None) == None:
            if self.parentPath != None:
                self.path = self._setPath(self.parentPath, kwargs.get('collectionType', "node"))
                setattr(self, "identifier", self.path)

        if kwargs.get('read_from_file', None) != None:
            self.read(kwargs.get('read_from_file'))
        
        self.write()
    
    def __str__(self):
        return super().__str__()

    def write(self):
        writeJson(self.collectData(), os.path.join(self.path, "collection.json"))

    def collectData(self) -> dict:
        collectData = super().collectData()
        collectData["collectionType"] = self.collectionType
        return collectData

    def read(self, path):
        readData = readJson(path)
        # Note this is jsut so legacy works:
        if "collectionType" in list(readData.keys()):
            self.collectionType = readData["collectionType"]
        else:
            self.collectionType = "node"
        super().setFromReadData(readData)

    def _setPath(self, path, collectiontype):
        folderName = "node_collections/"
        if collectiontype == "edge":
            folderName = "edge_collections/"
        makeDirsRecustive([
            os.path.join(path, folderName + str(self.uuid))
        ])
        writeJson({"items" : []}, os.path.join(path, folderName + str(self.uuid), "content.json"))
        return os.path.join(path, folderName + str(self.uuid))
    
    def duplicate(self, webPath: str, idChangeMap: dict, updateItems = False, itemChangeMap = {}, newUUIDs = True) -> 'Collection':
        """
        Duplicate the collection to a new path.
        
        Can optionally supply a itemChangeMap to update elemnts
        The old ID is a key in the itemChangeMap and the new ID is it's value.
        """

        # Create a deep copy of this collection and set a new uuid:
        duplicated = copy.deepcopy(self)
        if newUUIDs:
            duplicated.uuid = str(uuid.uuid4())
        idChangeMap[self.uuid] = duplicated.uuid

        # Set the collection's path, identifier:
        if self.collectionType == "node":
            duplicated.path = os.path.join(webPath, "node_collections/" + str(duplicated.uuid))
            duplicated.identifier = os.path.join(webPath, "node_collections/" + str(duplicated.uuid))
        elif self.collectionType == "edge":
            duplicated.path = os.path.join(webPath, "edge_collections/" + str(duplicated.uuid))
            duplicated.identifier = os.path.join(webPath, "edge_collections/" + str(duplicated.uuid))

        # Create the new folder structure and write edge data to file
        duplicated._setPath(webPath, self.collectionType)
        
        # Update content:
        oldContent = duplicated.contentToList()
        newContent = []
        for item in oldContent:
            if updateItems:
                if item in list(itemChangeMap.keys()):
                    newContent.append(itemChangeMap[item])
                else:
                    newContent.append(item)
            else:
                newContent.append(item)
        
        duplicated.clearContent()
        duplicated.addContent(newContent)
        
        # Write the updated collection:
        duplicated.write()

        return duplicated

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
    
    def clearContent(self):
        writeJson({"items" : []}, os.path.join(self.path, "content.json"))

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