from .Web import *

def testMessage():
    print("\nThe itsy bitsy spider crawled up the water spout...\n")

def createWeb(metadata):
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