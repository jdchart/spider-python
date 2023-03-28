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

    Because of this, it's also advised to used the built in duplication methods for
    copying anything (be it a web of an element in the web) as paths will need to be 
    changed programatically.

    Methods
    ----------
    write() -> None
        write the web to disk at it's path as metadata.json.

    read(path: str) -> None
        read the metadata.json file in Web's path and set data.

    duplicate(path: str, newUUIDs = True) -> Web
        duplicate the current web to a new path (also duplicates all of the content)
    
    getFullList(type: str, returnNested = True) -> list:
        return a list of content uuid's according to type.

    addNode(metadata: dict = {}) -> Node
        add a new node to the web.

    loadNode(searchTerm: str, **kwargs) -> Node
        load a node that already exists in the web. Give the optional argument
        "term" to define how the search for finding the node will be performed 
        (by default uuid).

    duplicateNode(searchTerm: str, idChangeMap: dict = {}, duplicateNested = True, **kwargs) -> Node
        duplicate a node from the web to the web. Can give an idChangMap dict 
        which will get updated to keep track of UUID changes.

    addEdge(metadata: dict) -> Edge:
        add a new edge to the web.

    loadEdge(searchTerm: str, **kwargs) -> Edge:
       load an edge that already exists in the web

    duplicateEdge(searchTerm: str, idChangeMap: dict = {}, **kwargs) -> Edge
        duplicate an edge from the web to the web.
        kwargs :
        update_notes : (bool) optionally update the source and target nodes
        node_id_map : (dict) key = oldNode uuid, value = newNode uuid

    addCollection(collectionType: str, metadata: dict) -> Collection
        add a new collection to the web.
        collectionType = "node" or "edge"

    loadCollection(searchTerm: str, **kwargs) -> Collection
        load a collection that already exists in the web.

    duplicateCollection(searchTerm: str, idChangeMap: dict = {}, **kwargs) -> Collection
        duplicate a collection from the web to the web.
        update_items : (bool) optionally update the source and target nodes
        item_id_map : (dict) key = oldNode uuid, value = newNode uuid
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
    
    def duplicate(self, path: str, newUUIDs = True) -> 'Web':
        """Duplicate the current web to a new path."""
        
        # Create a deep copy of this web
        duplicated = copy.deepcopy(self)

        # Set the web's path, identifier and give a new uuid:
        duplicated.path = path
        duplicated.identifier = path
        if newUUIDs:
            duplicated.uuid = str(uuid.uuid4())

        # Create the new folder structure and write web data to file
        duplicated._setPath(duplicated.path)
        duplicated.write()

        # Duplicate nodes
        fullNodeList = self.getFullList("nodes", False)
        nodeIdMap = {}
        for node in fullNodeList:
            loaded = self.loadNode(node)
            loaded.duplicate(os.path.join(duplicated.path, "web"), nodeIdMap, newUUIDs)

        # Duplicate edges
        fullEdgeList = self.getFullList("edges")
        edgeIdMap = {}
        for edge in fullEdgeList:
            loaded = self.loadEdge(edge)
            loaded.duplicate(os.path.join(duplicated.path, "web"), edgeIdMap, True, nodeIdMap, newUUIDs)

        # Duplicate collections
        fullNodeCollectionList = self.getFullList("node_collections")
        nodeCollectionIdMap = {}
        for collection in fullNodeCollectionList:
            loaded = self.loadCollection(collection)
            loaded.duplicate(os.path.join(duplicated.path, "web"), nodeCollectionIdMap, True, nodeIdMap, newUUIDs)
        
        fullEdgeCollectionList = self.getFullList("edge_collections")
        edgeCollectionIdMap = {}
        for collection in fullEdgeCollectionList:
            loaded = self.loadCollection(collection)
            loaded.duplicate(os.path.join(duplicated.path, "web"), edgeCollectionIdMap, True, edgeIdMap, newUUIDs)

        # Duplicate media
        for file in os.listdir(os.path.join(self.path, "media")):
            shutil.copyfile(os.path.join(self.path, "media/" + file), os.path.join(duplicated.path, "media/" + file))

        # Return the duplicated web
        return duplicated

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
    
    def duplicateNode(self, searchTerm: str, idChangeMap: dict = {},  duplicateNested = True, **kwargs) -> Node:
        """
        Duplicate a node from the web to the web.
        
        Make a copy of a node that exists in the web and add it at the top level
        of the node folder.

        To duplicate nodes as a nested node to another node, use the duplicateNode
        on a Node class object.

        Can give an idChangeMap object which will be updated to keep track of 
        UUID changes.

        searchTerm : node UUID
        """
        
        # Load the node to duplicate:
        toDuplicate = self.loadNode(searchTerm, **kwargs)

        # Duplicate the node and return:
        duplicated = toDuplicate.duplicate(os.path.join(self.path, "web"), idChangeMap, True, duplicateNested)
        return duplicated

    def addEdge(self, metadata: dict) -> Edge:
        """Add a new edge to the web."""

        newEdge = Edge(parentPath = os.path.join(self.path, "web"), **parseMetadata(metadata))
        return newEdge

    def loadEdge(self, searchTerm: str, **kwargs) -> Edge:
        """Load an edge that already exists in the web."""

        searchKey = kwargs.get('term', "uuid")
        edgePath = findElement(os.path.join(self.path, "web/edges"), searchTerm, searchKey, "edge")
        loadedEdge = Edge(read_from_file = edgePath)
        return loadedEdge

    def duplicateEdge(self, searchTerm: str, idChangeMap: dict = {}, **kwargs) -> Edge:
        """
        Duplicate an edge from the web to the web.
        
        Make a copy of an edge that exists in the web and add it to the edges folder.

        Can give an idChangeMap object which will be updated to keep track of 
        UUID changes.

        searchTerm : node UUID
        kwargs 
        ----------
        update_nodes : (bool) optionally update the source and target nodes
        node_id_map : (dict) key = oldNode uuid, value = newNode uuid
        """
        
        # Load the node to duplicate:
        toDuplicate = self.loadEdge(searchTerm, **kwargs)

        # Duplicate the node and return:
        duplicated = toDuplicate.duplicate(os.path.join(self.path, "web"), idChangeMap, kwargs.get("update_nodes", False), kwargs.get("node_id_map", {}), True)

        return duplicated

    def addCollection(self, collectionType: str, metadata: dict) -> Collection:
        """
        Add a new collection to the web.
        
        collectionType = "node" or "edge"
        """

        newCollection = Collection(parentPath = os.path.join(self.path, "web"), collectionType = collectionType, **parseMetadata(metadata))
        return newCollection

    def loadCollection(self, searchTerm: str, **kwargs) -> Collection:
        """Load a collection that already exists in the web."""

        searchKey = kwargs.get('term', "uuid")
        collectionPath = findElement(os.path.join(self.path, "web"), searchTerm, searchKey, "collection")
        loadedCollection = Collection(read_from_file = collectionPath)
        return loadedCollection
    
    def duplicateCollection(self, searchTerm: str, idChangeMap: dict = {}, **kwargs) -> Collection:
        """
        Duplicate a collection from the web to the web.
        
        Make a copy of an collection that exists in the web and add it to the collections folder.

        Can give an idChangeMap object which will be updated to keep track of 
        UUID changes.

        searchTerm : node UUID
        kwargs 
        ----------
        update_items : (bool) optionally update the source and target nodes
        item_id_map : (dict) key = oldNode uuid, value = newNode uuid
        """
        
        # Load the node to duplicate:
        toDuplicate = self.loadCollection(searchTerm, **kwargs)

        # Duplicate the node and return:
        duplicated = toDuplicate.duplicate(os.path.join(self.path, "web"), idChangeMap, kwargs.get("update_items", False), kwargs.get("item_id_map", {}), True)

        return duplicated
    
    def getFullList(self, type: str, returnNested = True) -> list:
        """
        Return a list of content uuid's according to type.
        
        type = "nodes", "edges", "node_collections" or "edge_collections"
        Will also return nested content.
        """
        
        fullList = []
        if returnNested:
            for root, dirs, files in os.walk(os.path.join(self.path, "web/" + type)):
                for dir in dirs:
                    if dir != type:
                        fullList.append(dir)
        elif returnNested == False:
            for dir in os.listdir(os.path.join(self.path, "web/" + type)):
                if dir != type:
                    if os.path.isdir(os.path.join(self.path, "web/" + type + "/" + dir)):
                        fullList.append(dir)
        return fullList













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

    def convertToMemoRekall(self, **kwargs):
        webToManifestNetwork(
            self,
            **kwargs
        )

    def convertToNetwork(self, **kwargs):
        newNetwork = NetworkGraph(self, **kwargs)
        return newNetwork