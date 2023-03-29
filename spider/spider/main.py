from .Web import *
from .utils import *
from .convertions import *

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