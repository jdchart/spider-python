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
import copy
import uuid

class Web(SpiderElement):
    """
    The Spider Web class where everything lives.

    This is the main structure of elements. It contains nodes, edges and collections.
    It is based on the basic SpiderElement class, and therefore shares all of its
    attributes, as well as the Dublin Core Resources elements.

    On disk, the web takes the form of a folder, containing folders for nodes, edges and
    collections. This folder structure is created whenever a new web is created (which means)
    that you must always provide a path on creation.

    Methods
    ----------
    write() -> None
        write the web to disk at it's path as metadata.json.

    read(path: str) -> None
        read the metadata.json file in Web's path and set data.

    addNode(metadata: dict = {}) -> Node
        add a new node to the web.

    loadNode(searchTerm: str, **kwargs) -> Node
        load a node that already exists in the web. Give the optional argument
        "term" to define how the search for finding the node will be performed 
        (by default uuid).
    """
    def __init__(self, path: str = os.path.join(os.getcwd(), "newWeb"), **kwargs):
        
        # Set the kwargs' path value to the given variable.
        kwargs["path"] = path

        # Init base SpiderElement class:
        super().__init__(**kwargs)

        # Set path and indentifier attributes to be the same:
        self._initPathAndIdentifier(**kwargs)

        # When creating a new web, create paths:
        if kwargs.get('read_from_file', None) == None:
            self._setPath(self.path)
        
        # When loading a web, read from file:
        if kwargs.get('read_from_file', None) != None:
            self.read(kwargs.get('read_from_file'))

        # Write to disk
        self.write()

    def _initPathAndIdentifier(self, **kwargs):
        """Make the self.path and self.identifier attributes the same"""

        # If the path or identifier is given:
        if kwargs.get('path', None) != None or kwargs.get('identifier', None) != None:
            # If the path is given:
            if kwargs.get('path', None) != None:
                setattr(self, "identifier", kwargs.get('path'))
                self.path = kwargs.get('path')
            # If identifier is given:
            elif kwargs.get('identifier', None) != None:
                self.path = kwargs.get('identifier')
            else:
                self.path = os.getcwd()
                setattr(self, "identifier", os.getcwd())
    
    def __str__(self):
        return super().__str__()

    def write(self) -> None:
        """Write the web to disk at it's path as 'metadata.json'"""

        writeJson(self.collectData(), os.path.join(self.path, "metadata.json"))

    def read(self, path: str) -> None:
        """Read the metadata.json file in Web's path and set data."""

        readData = readJson(os.path.join(path, "metadata.json"))
        super().setFromReadData(readData)

    def _setPath(self, path: str):
        """Create basic folder structure and files."""

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

    def addNode(self, metadata: dict = {}) -> Node:
        """Add a new node to the web."""

        newNode = Node(parentPath = os.path.join(self.path, "web"), **parseMetadata(metadata))
        return newNode
    
    def loadNode(self, searchTerm: str, **kwargs) -> Node:
        """Load a node that already exists in the web."""

        searchKey = kwargs.get('term', "uuid")
        nodePath = findElement(os.path.join(self.path, "web/nodes"), searchTerm, searchKey, "node")
        loadedNode = Node(read_from_file = nodePath)
        return loadedNode
    
    def duplicateNode(self, searchTerm, **kwargs):
        toDuplicate = self.loadNode(searchTerm, **kwargs)

        newNode = copy.deepcopy(toDuplicate)
        newNode.uuid = str(uuid.uuid4())

        makeDirsRecustive([os.path.join(self.path, "web/nodes/" + newNode.uuid)])
        newNode.path = os.path.join(self.path, "web/nodes/" + newNode.uuid) # TODO This will not work for nested
        print(newNode.path)

        newNode.write()

        return newNode

    

    def addEdge(self, metadata):
        newEdge = Edge(parentPath = os.path.join(self.path, "web"), **parseMetadata(metadata))
        return newEdge

    def loadEdge(self, searchTerm, **kwargs):
        searchKey = kwargs.get('term', "uuid")
        edgePath = findElement(os.path.join(self.path, "web/edges"), searchTerm, searchKey, "edge")
        loadedEdge = Edge(read_from_file = edgePath)
        return loadedEdge





    def addCollection(self, collectionType, metadata):
        newCollection = Collection(parentPath = os.path.join(self.path, "web"), collectionType = collectionType, **parseMetadata(metadata))
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
        webToManifestNetwork(
            self,
            **kwargs
        )

    def convertToNetwork(self, **kwargs):
        newNetwork = NetworkGraph(self, **kwargs)
        return newNetwork