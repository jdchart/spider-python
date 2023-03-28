from .Web import *
from .utils import *
from .IIIF import *
from .Network import *

def createWeb(metadata: dict) -> Web:
    """
    Create a new spider web.

    Provide a dict of metadata for creating the web.
    The web will be saved to disk at the given in the metadata dict.
    """

    newWeb = Web(**parseMetadata(metadata))
    return newWeb

def loadWeb(path: str) -> Web:
    """
    Load a spider web from disk.
    
    Provide the path to a folder and return the spider web object.
    """

    loadedWeb = Web(read_from_file = path)
    return loadedWeb

def webToMemoRekall(web, **kwargs):
    webToManifestNetwork(
        web,
        **kwargs
    )

def webToNetworkx(web: Web, **kwargs):
    """Convert a web to a Network object which is around networkx's Graph class."""
    
    newNetwork = NetworkGraph(web, **kwargs)
    return newNetwork

def checkCollectionSanity(web, nodes, edges):
    toReturn = True
    nodeList = nodes.contentToList()
    edgeList = edges.contentToList()

    for item in edgeList:
        loadedEdge = web.loadEdge(item)
        if loadedEdge.relation.source not in nodeList or loadedEdge.relation.target not in nodeList:
            toReturn = False

    return toReturn