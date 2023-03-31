# TODO Make all of this a class.

from .IIIFconverts import *
from .Network import *

def webToNetworkx(web, **kwargs):
    """Convert a web to a Network object which is around networkx's Graph class."""
    
    newNetwork = NetworkGraph(web, **kwargs)
    return newNetwork

def networkxToManifest(networkx, web, **kwargs):
    """
    Convert the networkx convertion and it's web to a IIIF manifest.
    
    kwargs:
    path : str
        the prefix for the server.

    writePath: str
        the folder for saving to disk.
    
    networkName : str
        give the manifest and the network a name.
    """

    # Set the paths for the network image that will be created.
    imagePath = os.path.join(kwargs.get("path", os.getcwd()), "media/" + kwargs.get("networkName", "Untitled_network").replace(" ", "_") + ".png")
    imageWritePath = os.path.join(kwargs.get("writePath", os.getcwd()), "media/" + kwargs.get("networkName", "Untitled_network").replace(" ", "_") + ".png")
    
    # Create the image and retrieve the image data:
    imgData = networkx.saveToImage(
        savePath = imageWritePath,
        algo = kwargs.get("algo", "spring")
    )
    
    # Create the IIIF manifest:
    manifest = networkxToIIIFManifest(web, imgData,
        imagePath = imagePath,
        networkName = kwargs.get("networkName", "Untitled_network"),
        path = kwargs.get("path", os.getcwd()),
        writePath = kwargs.get("writePath", os.getcwd())
    )

    return manifest

def webToMemoRekall(web, **kwargs):
    """
    Convert a web to a network of IIIF manifests.
    
    kwargs:
    writePath : str
        the folder in which to write the manifest files (default: web.path/mirador)

    path : str
        the path on the server for the manifest.
    
    removePrevious : list
        delete previous content in the given writePath (default: [True, True])
        [removeManifestFiles, removeMediaFiles] 
    
    copyMedia : bool
        corpy the node's media to the out media folder (default: True)

    nodeList : list | Collection
        list of collection of nodes to parse (defualt: web.getFullList("nodes"))
    
    edgeList : list | Collection
        list of collection of edges to parse (defualt: web.getFullList("edges"))
    """
    
    webToIIIFManifestNetwork(
        web,
        **kwargs
    )

def nodeToManifest(node):
    """
    Convert a node to a network of IIIF manifests.
    
    
    """
    pass


def checkCollectionSanity(web, nodes, edges):
    toReturn = True
    nodeList = nodes.contentToList()
    edgeList = edges.contentToList()

    for item in edgeList:
        loadedEdge = web.loadEdge(item)
        if loadedEdge.relation.source not in nodeList or loadedEdge.relation.target not in nodeList:
            toReturn = False

    return toReturn