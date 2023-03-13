from .Web import *

def testMessage() -> None:
    """
    A test function to check things are working.

    Will print a test string to the console.
    """

    print("\nThe itsy bitsy spider crawled up the water spout...\n")

def createWeb(metadata: dict) -> Web:
    """Create a new spider web.

    Provide a dict of metadata for creating the web.
    The web will be saved to disk at the given in the metadata dict.

    Parameters
    ----------
    Obligatory metadata field:
        "path" : Path/on/disk/to/save/web
    """



    newWeb = Web(**metadata)
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