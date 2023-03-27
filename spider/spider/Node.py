import os
import copy
import uuid
from .SpiderElement import *
from .utils import *

class Node(SpiderElement):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.parentPath = kwargs.get('parentPath', None)

        if kwargs.get('read_from_file', None) == None:
            if self.parentPath != None:
                self.path = self._setPath(self.parentPath)
                setattr(self, "identifier", self.path)

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

    def _setPath(self, path):
        makeDirsRecustive([
            os.path.join(path, "nodes/" + str(self.uuid)),
            os.path.join(path, "nodes/" + str(self.uuid) + "/nodes")
        ])
        return os.path.join(path, "nodes/" + str(self.uuid))
    
    def addNode(self, metadata):
        newNode = Node(parentPath = self.path, **parseMetadata(metadata))
        return newNode

    def loadNode(self, searchTerm, **kwargs):
        searchKey = kwargs.get('term', "uuid")
        nodePath = findElement(self.path, searchTerm, searchKey, "node")
        loadedNode = Node(read_from_file = nodePath)
        return loadedNode
    

    def duplicate(self, webPath: str, idChangeMap: dict, newUUIDs = True, duplicateNested = True) -> 'Node':
        """
        Duplicate the node to a new path.
        
        Different from Web's method duplicateNode which duplicates a node
        within the web. This can take any node, and duplicate it to a new web.
        """

        # Create a deep copy of this node and set a new uuid:
        duplicated = copy.deepcopy(self)
        if newUUIDs:
            duplicated.uuid = str(uuid.uuid4())
        idChangeMap[self.uuid] = duplicated.uuid

        # Set the web's path, identifier and give a new uuid:
        duplicated.path = os.path.join(webPath, "nodes/" + str(duplicated.uuid))
        duplicated.identifier = os.path.join(webPath, "nodes/" + str(duplicated.uuid))

        # Create the new folder structure and write node data to file
        duplicated._setPath(webPath)
        duplicated.write()

        # Duplicate nested nodes
        if duplicateNested:
            nestedNodes = self.getFullList(False)
            for nestedNode in nestedNodes:
                fullPath = os.path.join(self.path, "nodes/" + nestedNode + "/node.json")
                oldNode = Node(read_from_file = fullPath)
                oldNode.duplicate(duplicated.path, idChangeMap, newUUIDs, duplicateNested)

        return duplicated
    
    def duplicateNode(self, node: 'Node', idChangeMap: dict = {}, duplicateNested = True, **kwargs) -> 'Node':
        """
        Duplicate a node as a nested node to this node.
        
        Make a copy of a node that exists and add it at the top level
        of the node's nodes folder.

        Can give an idChangeMap object which will be updated to keep track of 
        UUID changes.
        """

        # Duplicate the node and return:
        duplicated = node.duplicate(os.path.join(self.path), idChangeMap, True, duplicateNested)
        return duplicated

    def getFullList(self, returnNested = True) -> list:
        """Return a list of content uuid's."""
        
        fullList = []
        if returnNested:
            for root, dirs, files in os.walk(os.path.join(self.path, "nodes")):
                for dir in dirs:
                    if dir != "nodes":
                        fullList.append(dir)
        elif returnNested == False:
            for dir in os.listdir(os.path.join(self.path, "nodes")):
                if dir != type:
                    if os.path.isdir(os.path.join(self.path, "nodes" + "/" + dir)):
                        fullList.append(dir)
        return fullList