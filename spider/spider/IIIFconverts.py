import os
import shutil
from .utils import *
from .IIIFManifest import *

def networkxToIIIFManifest(web, imageData, **kwargs):
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






def webToManifestNetwork(web, **kwargs):
    # Making folders to save the manifest files:
    destDir = os.path.join(web.path, "mirador")
    if kwargs.get('writePath', None) != None:
        destDir = kwargs.get('writePath')
    
    if kwargs.get("removePrevious", [True, True])[0] == True:
        if os.path.isdir(os.path.join(destDir, "lower")) == True:
            shutil.rmtree(os.path.join(destDir, "lower"))
        if os.path.isdir(destDir) == True:
            for filename in os.listdir(destDir):
                if os.path.isfile(filename):
                    os.remove(filename)
    if kwargs.get("removePrevious", [True, True])[1] == True:
        if os.path.isdir(os.path.join(destDir, "media")) == True:
            shutil.rmtree(os.path.join(destDir, "media"))
    
    makeDirsRecustive([
        os.path.join(destDir, "lower"),
        os.path.join(destDir, "media")
    ])

    nodeColl = kwargs.get("nodeList", web.getFullList("nodes"))
    nodeList = nodeColl.contentToList() # Mis match between given collection and default being a list !

    for i in range(len(nodeList)):
        # Load the node
        node = web.loadNode(nodeList[i])

        # Create the manifest
        print("Converting node " + str(i + 1) + "/" + str(len(nodeList)) + " \"" + node.title + "\"\n(" + str(node.uuid) + ")\n")
        thisManifest = nodeToManifest(web, node, destDir = destDir, **kwargs)
        
        # Save the manifest
        thisManifest.write()

def nodeToManifest(web, node, **kwargs):
    # Get the node's paths
    realPath = kwargs.get('path', os.getcwd())
    thisDestDir = kwargs.get('destDir', os.getcwd())
    if node.instructionalMethod.important == False:
        thisDestDir = os.path.join(thisDestDir, "lower")
        realPath = os.path.join(realPath, "lower")

    # Media paths and copy:
    realMediaPath = os.path.join(kwargs.get('path', os.getcwd()), "media/" + os.path.basename(node.format.uri))
    writeMediaPath = os.path.join(kwargs.get('destDir', os.getcwd()), "media/" + os.path.basename(node.format.uri))
    if kwargs.get("copyMedia", True) == True:
        shutil.copyfile(node.format.uri, writeMediaPath)
    
    # If PDF, convert to image:
    convertedFiles = []
    if node.format.fileFormat == "pdf":
        convertedFiles = convertPDF(
            node.format.uri, 
            os.path.join(kwargs.get('destDir', os.getcwd()), "media"), 
            node.format.pages, 
            kwargs.get("copyMedia", True)
        )

    node.format.uri = realMediaPath

    # Get the node's adges:
    edgeColl = kwargs.get("edgeList", web.getFullList("edges")) # Mis match between given collection and default being a list !
    edgeList = edgeColl.contentToList()
    interDocAnnotations = getInterDocs(web, node, edgeList)

    # Get the NESTED NODES:
    nestedNodes = node.getFullList()

    # Main title object
    labelObject = parseToLabel(node.title)

    # Create the manifest
    newManifest = Manifest(
        writepath = thisDestDir,
        filename = str(node.uuid) + ".json",
        path = realPath,
        label = labelObject
    )

    originalNode = node
    numPages = 1

    if originalNode.format.pages != None:
        numPages = originalNode.format.pages

    fileConverted = False
    if originalNode.format.type == "document":
        fileConverted = True
    for i in range(numPages):
        pageCanvas = newManifest.addCanvas(i + 1)
            
        # Create layers
        mainLayer = pageCanvas.addAnnotationPage("page", 1)
        annotationLayer = pageCanvas.addAnnotationPage("annotation", 1)

        # Create a new node for this page if paged document:
        pageNode = originalNode
        if fileConverted:
            pageNode.format.type = "image"
            pageNode.format.fileFormat = "jpg"
            pageNode.format.uri = os.path.join(kwargs.get('path', os.getcwd()), "media/" + convertedFiles[i])

        # Add main media item:
        mainMediaItem = mainLayer.addMediaItem(1, pageNode)
        # Resize canvas:
        pageCanvas.width = mainMediaItem.body.width
        pageCanvas.height = mainMediaItem.body.height
        if mainMediaItem.body.duration != None:
            pageCanvas.duration = mainMediaItem.body.duration

        # Add infra-documentary annotations:
        if len(nestedNodes) > 0:
            print("Found nested nodes for " + node.title + ":")
            print(nestedNodes)

            maxNodeHeight = 0
            # COPY MEDIA IF NEEDED
            for j in range(len(nestedNodes)):
                loadedNestedNode = web.loadNode(nestedNodes[j])

                loadedNestedNode.format.uri = os.path.join(kwargs.get('path', os.getcwd()), "media/" + loadedNestedNode.format.uri)
                
                annotationMediaItem = annotationLayer.addIntraDocItem(j + 1, loadedNestedNode, lang = kwargs.get("lang", None))
                if loadedNestedNode.format.fullDimensions[1] > maxNodeHeight:
                    maxNodeHeight = loadedNestedNode.format.fullDimensions[1]

            pageCanvas.height = pageCanvas.height + maxNodeHeight

        # Add inter-documentary annotations:
        for j in range(len(interDocAnnotations)):
            thisEdge = web.loadEdge(interDocAnnotations[j])
            theOtherNode = None
            regions = None
            if str(node.uuid) == thisEdge.relation.source:
                theOtherNode = web.loadNode(thisEdge.relation.target)
                regions = thisEdge.relation.sourceRegions
            else:
                theOtherNode = web.loadNode(thisEdge.relation.source)
                regions = thisEdge.relation.targetRegions
            annotationMediaItem = annotationLayer.addInterDocItem(j + 1 + len(nestedNodes), theOtherNode, thisEdge, regions, kwargs.get('path', os.getcwd()), lang = kwargs.get("lang", None))

    return newManifest



def getInterDocs(web, node, edgeList):
    # Return a list of edges in which the node is present as a source or a target:
    interList = []
    for item in edgeList:
        thisEdge = web.loadEdge(item)
        if str(node.uuid) == thisEdge.relation.source or str(node.uuid) == thisEdge.relation.target:
            interList.append(item)
    return interList