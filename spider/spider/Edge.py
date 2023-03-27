import os
import copy
from .SpiderElement import *
from .utils import *

class Edge(SpiderElement):
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
        writeJson(self.collectData(), os.path.join(self.path, "edge.json"))

    def read(self, path):
        readData = readJson(path)
        super().setFromReadData(readData)

    def _setPath(self, path):
        makeDirsRecustive([
            os.path.join(path, "edges/" + str(self.uuid))
        ])
        return os.path.join(path, "edges/" + str(self.uuid))
    
    def duplicate(self, webPath: str, idChangeMap: dict, updateNodes = False, nodeChangeMap = {}, newUUIDs = True) -> 'Edge':
        """
        Duplicate the edge to a new path.
        
        Can optionally supply a nodeChangeMap to updateNodes (sources and targets).
        The old ID is a key in the nodeChangeMap and the new ID is it's value.
        """

        # Create a deep copy of this node and set a new uuid:
        duplicated = copy.deepcopy(self)
        if newUUIDs:
            duplicated.uuid = str(uuid.uuid4())
        idChangeMap[self.uuid] = duplicated.uuid

        # Set the edges's path, identifier and give a new uuid:
        duplicated.path = os.path.join(webPath, "edges/" + str(duplicated.uuid))
        duplicated.identifier = os.path.join(webPath, "edges/" + str(duplicated.uuid))

        # Create the new folder structure and write edge data to file
        duplicated._setPath(webPath)
        
        # Update sources and targets:
        if updateNodes:
            if duplicated.relation.source != None:
                if duplicated.relation.source in list(nodeChangeMap.keys()):
                    duplicated.relation.source = nodeChangeMap[duplicated.relation.source]
            if duplicated.relation.target != None:
                if duplicated.relation.target in list(nodeChangeMap.keys()):
                    duplicated.relation.target = nodeChangeMap[duplicated.relation.target]
        
        # Write the updated edge:
        duplicated.write()

        return duplicated