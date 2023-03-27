from .Web import *
from .utils import *

def testMessage() -> str:
    """
    A test function to check things are working.

    Will print a test string to the console.
    """
    msg = "The itsy bitsy spider crawled up the water spout..."

    print("\n" + msg + "\n")
    return msg

def createWeb(metadata: dict) -> Web:
    """Create a new spider web.

    Provide a dict of metadata for creating the web.
    The web will be saved to disk at the given in the metadata dict.
    """

    newWeb = Web(**parseMetadata(metadata))
    return newWeb

def loadWeb(path):
    loadedWeb = Web(read_from_file = path)
    return loadedWeb

def checkCollectionSanity(web, nodes, edges):
    toReturn = True
    nodeList = nodes.contentToList()
    edgeList = edges.contentToList()

    for item in edgeList:
        loadedEdge = web.loadEdge(item)
        if loadedEdge.relation.source not in nodeList or loadedEdge.relation.target not in nodeList:
            toReturn = False

    return toReturn