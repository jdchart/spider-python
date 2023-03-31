import os
from .utils import *
from .IIIFManifest import *
from .IIIFutils import *

def networkxToIIIFManifest(web, imageData, **kwargs) -> Manifest:
    """Convert a web and networkx imageData to a IIIF manifest."""

    # Create the manifest:
    newManifest = Manifest(
        writepath = kwargs.get("writePath", os.getcwd()),
        filename = kwargs.get("networkName", os.getcwd()).replace(" ", "_") + '.json',
        path = kwargs.get("path", os.getcwd()),
        label = {"en" : [kwargs.get("networkName", os.getcwd())]}
    )

    # Create the main canvas:
    pageCanvas = newManifest.addCanvas()

    # Create the main and annotation annotationPage layers:
    mainLayer = pageCanvas.addAnnotationPage()
    annotationLayer = pageCanvas.addAnnotationPage(type = "annotation")

    # Add main media item:
    mainMediaItem = mainLayer.addMediaItem(mediaInfo = parseImageDataToMediaInfo({
        "uri" : kwargs.get("imagePath"),
        "width" : imageData["meta"]["width"],
        "height" : imageData["meta"]["height"],
        "fileformat" : imageData["meta"]["fileformat"]
    }))

    # Resize canvas:
    pageCanvas.width = mainMediaItem.body.width
    pageCanvas.height = mainMediaItem.body.height
    if mainMediaItem.body.duration != None:
        pageCanvas.duration = mainMediaItem.body.duration

    # Add nodes as annotations:
    for item in imageData:
        if item != "meta":
            # Retrieve target node and it's dimensions:
            targetNode = web.loadNode(item)
            annotationDims = [imageData[item]["x"], imageData[item]["y"], imageData[item]["size"]]

            # Add the media item:
            annotationLayer.addMediaItem(bespokeItem = {
                "type" : "networkxNode",
                "data" : {
                    "node" : targetNode,
                    "path" : kwargs.get('path', os.getcwd()),
                    "annotationDims" : annotationDims
                }
            })

    # Write the manifest to disk
    newManifest.write()

    return newManifest

def webToIIIFManifestNetwork(web, **kwargs):
    """
    Convert a web to a network of IIIF manifests.
    
    Convert a web (possibility to set collections of nodes and edges) to a
    network of IIIF manifests to be navigated in Mirador.

    kwargs:
    writePath : str
        the folder in which to write the manifest files (default: web.path/mirador)
    
    removePrevious : list
        delete previous content in the given writePath (default: [True, True])
        [removeManifestFiles, removeMediaFiles] 
    
    nodeList : list | Collection
        list of collection of nodes to parse (defualt: web.getFullList("nodes"))
    """

    # Create folders to write manifest files:
    initializeFolders(
        kwargs.get('writePath', os.path.join(web.path, "mirador")), 
        kwargs.get("removePrevious", [True, True])
    )

    # Get the list of nodes to parse:
    nodeList = kwargs.get("nodeList", web.getFullList("nodes", False))
    # If the type of the given node list is not a list, treat it as a collection:
    if type(nodeList) != list:
        nodeList = nodeList.contentToList()

    for i in range(len(nodeList)):
        # Load the node
        node = web.loadNode(nodeList[i])

        # Create the manifest
        #print("Converting node " + str(i + 1) + "/" + str(len(nodeList)) + " \"" + node.title + "\"\n(" + str(node.uuid) + ")\n")
        thisManifest = nodeToIIIFManifest(
            web, 
            node, 
            destDir = kwargs.get('writePath', os.path.join(web.path, "mirador")), 
            **kwargs
        )
        
        # Save the manifest
        thisManifest.write()

def nodeToIIIFManifest(web, node, **kwargs):
    """
    Convert a spider Node to a IIIF Manifest.
    
    kwargs:
    destDir : str
        the folder in which to write the manifest files (default: web.path/mirador)
    
    path : str
        the path on the server for the manifest.

    copyMedia : bool
        corpy the node's media to the out media folder (default: True)
    
    edgeList : list | Collection
        list of collection of edges to parse (defualt: web.getFullList("edges"))
    """

    # Parse the various paths required for node to manifest creation:
    paths = getNodeToIIIFManifestPaths(node, kwargs.get('path', os.getcwd()), kwargs.get('destDir', os.getcwd()))

    # Perform media copying and convertion for node to manifest and return data:
    mediaConvert = getNodeToIIIFMediaConvert(node, paths, kwargs.get("copyMedia", True))

    # Get lists of annotations inter and intra annotations:
    annotationLists = getNodeToIIIFManifestAnnotations(node, web, kwargs.get("edgeList", web.getFullList("edges")))

    # Create the manifest
    newManifest = Manifest(
        writepath = paths["thisDestDir"],
        filename = str(node.uuid) + ".json",
        path = paths["realPath"],
        label = parseToLabel(node.title)
    )

    # Perform operations for each page of the associated media:
    for i in range(mediaConvert["numPages"]):
        # Create the canvas and page and annotation annotationPages:
        pageCanvas = newManifest.addCanvas()
        mainLayer = pageCanvas.addAnnotationPage()
        annotationLayer = pageCanvas.addAnnotationPage(type = "annotation")

        # Get a copy of the original node, update the associated media's format data if it was converted:
        pageNode = mediaConvert["originalNode"]
        if mediaConvert["fileConverted"]:
            pageNode.format.type = "image"
            pageNode.format.fileFormat = "jpg"
            pageNode.format.uri = os.path.join(kwargs.get('path', os.getcwd()), "media/" + mediaConvert["convertedFiles"][i])

        # Add main media item and resize canvas accordingly:
        mainMediaItem = mainLayer.addMediaItem(mediaInfo = parseNodeToIIIFMediaItem(pageNode, "page"))
        pageCanvas.width = mainMediaItem.body.width
        pageCanvas.height = mainMediaItem.body.height
        if mainMediaItem.body.duration != None:
            pageCanvas.duration = mainMediaItem.body.duration

        # Add intra-documentary annotations:
        if len(annotationLists["intra"]) > 0:
            # Colllecting the tallest node:
            maxNodeHeight = 0

            for j in range(len(annotationLists["intra"])):
                # Load the nested node and update it's adresse:
                loadedNestedNode = web.loadNode(annotationLists["intra"][j])
                
                # Convert it's media
                nestedNodeToIIIFManifestMediaConvert(loadedNestedNode, paths, kwargs.get("copyMedia", True))

                if loadedNestedNode.format.uri != None:
                    loadedNestedNode.format.uri = os.path.join(kwargs.get('path', os.getcwd()), "media/" + loadedNestedNode.format.uri)
                else:
                    loadedNestedNode.format.uri = ""
                
                # Create the annotation:
                annotationLayer.addMediaItem(
                    mediaInfo = parseNodeToIIIFMediaItem(loadedNestedNode, "annotation"),
                    bespokeItem = {"type" : "intra", "data" : {"node" : loadedNestedNode}}
                )
                
                # Collecting the tallest node:
                if loadedNestedNode.instructionalMethod.annotationPaint == True:
                    if loadedNestedNode.format.fullDimensions[1] > maxNodeHeight:
                        maxNodeHeight = loadedNestedNode.format.fullDimensions[1]

            # Update the height of the main canvas according to the tallest node:
            pageCanvas.height = pageCanvas.height + maxNodeHeight

        # Add inter-documentary annotations:
        for j in range(len(annotationLists["inter"])):
            # Load the edge:
            thisEdge = web.loadEdge(annotationLists["inter"][j])
            
            # Get the target node and regions for the annotation:
            theOtherNode = None
            regions = None
            if str(node.uuid) == thisEdge.relation.source:
                theOtherNode = web.loadNode(thisEdge.relation.target)
                regions = thisEdge.relation.sourceRegions
            else:
                theOtherNode = web.loadNode(thisEdge.relation.source)
                regions = thisEdge.relation.targetRegions
            
            # Create the annotation:
            annotationLayer.addMediaItem(
                mediaInfo = parseNodeToIIIFMediaItem(theOtherNode, "annotation"),
                bespokeItem = {
                "type" : "inter", 
                "data" : {
                    "node" : theOtherNode, 
                    "edge" : thisEdge, 
                    "path" : kwargs.get('path', os.getcwd()),
                    "regions" : regions
                    }
                }
            )

    return newManifest