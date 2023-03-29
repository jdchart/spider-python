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
    """Convert a web to a network of IIIF manifests."""
    
    webToManifestNetwork(
        web,
        **kwargs
    )



def checkCollectionSanity(web, nodes, edges):
    toReturn = True
    nodeList = nodes.contentToList()
    edgeList = edges.contentToList()

    for item in edgeList:
        loadedEdge = web.loadEdge(item)
        if loadedEdge.relation.source not in nodeList or loadedEdge.relation.target not in nodeList:
            toReturn = False

    return toReturn