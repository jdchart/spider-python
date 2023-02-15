from .Web import *

def testMessage():
    print("\nThe itsy bitsy spider crawled up the water spout...\n")

def createWeb(metadata):
    newWeb = Web(**metadata)
    return newWeb

def loadWeb(path):
    loadedWeb = Web(read_from_file = path)
    return loadedWeb