import os
import shutil
from .utils import *

def initializeFolders(destDir, removePrevious):
    """Given parameters, remove old files and create folders"""

    # If set to remove manifest files:
    if removePrevious[0] == True:
        # Remove the "lower" folder:
        if os.path.isdir(os.path.join(destDir, "lower")) == True:
            shutil.rmtree(os.path.join(destDir, "lower"))
        # Remove all files from the destination directory
        if os.path.isdir(destDir) == True:
            for filename in os.listdir(destDir):
                if os.path.isfile(filename):
                    os.remove(filename)
    # If set to remove "media" files:
    if removePrevious[1] == True:
        # Remove the media folder:
        if os.path.isdir(os.path.join(destDir, "media")) == True:
            shutil.rmtree(os.path.join(destDir, "media"))
    
    # Create the new folders:
    makeDirsRecustive([
        os.path.join(destDir, "lower"),
        os.path.join(destDir, "media")
    ])

def getNodeToIIIFManifestPaths(node, path: str, destDir: str) -> dict:
    """Parse the various paths required for node to manifest creation"""

    # Get the node's paths
    realPath = path
    thisDestDir = destDir

    # Add "lower" to the path if node is not important:
    if node.instructionalMethod.important == False:
        thisDestDir = os.path.join(thisDestDir, "lower")
        realPath = os.path.join(realPath, "lower")

    # Set full media paths from node's associated media:
    realMediaPath = os.path.join(path, "media/" + os.path.basename(node.format.uri))
    writeMediaPath = os.path.join(destDir, "media/" + os.path.basename(node.format.uri))

    return{
        "realPath" : realPath,
        "thisDestDir" : thisDestDir,
        "realMediaPath" : realMediaPath,
        "writeMediaPath" : writeMediaPath,
        "destDir" : destDir
    }

def getNodeToIIIFMediaConvert(node, paths: dict, copyMedia: bool) -> dict:
    """Perform media copying and convertion for node to manifest and return data."""
    
    # Copy the node
    originalNode = node

    # Copy media if set to copy
    if copyMedia == True:
        shutil.copyfile(node.format.uri, paths["writeMediaPath"])
    
    # If the node's associated media is a PDF:
    convertedFiles = []
    if node.format.fileFormat == "pdf":
        # Convert PDF the image and populate convertedFiles list
        # (will populate list if copyMedia is True or False
        # this allows for paged media to work even if the convertion
        # didn't take place.)
        convertedFiles = convertPDF(
            node.format.uri, 
            os.path.join(paths["destDir"], "media"), 
            node.format.pages, 
            copyMedia
        )
    # Get the number of pages
    numPages = 1
    if originalNode.format.pages != None:
        numPages = originalNode.format.pages
    # See if file convertion happened
    fileConverted = False
    if originalNode.format.type == "document":
        fileConverted = True

    # Set the node's media uri as the realMediaPath for parsing later on:
    node.format.uri = paths["realMediaPath"]

    return {
        "numPages" : numPages,
        "fileConverted" : fileConverted,
        "convertedFiles" : convertedFiles,
        "originalNode" : originalNode
    }

def getNodeToIIIFManifestAnnotations(node, web, edges) -> dict:
    """Get the lists of inter and intra documentary annnotations for node to manifest convert."""

    # Get the edges to parse:
    edgeList = edges
    # If the type of the given edge list is not a list, treat it as a collection:
    if type(edgeList) != list:
        edgeList = edgeList.contentToList()

    # List of inter-documenatry annotations:
    interDocAnnotations = getInterDocs(web, node, edgeList)

    # Get the nested nodes as intra-documentary annotations:
    nestedNodes = node.getFullList(False)

    return {
        "inter" : interDocAnnotations,
        "intra" : nestedNodes
    }

def getInterDocs(web, node, edgeList):
    """Return a list of edges in which the node is present as a source or a target."""

    interList = []
    for item in edgeList:
        thisEdge = web.loadEdge(item)
        if str(node.uuid) == thisEdge.relation.source or str(node.uuid) == thisEdge.relation.target:
            interList.append(item)
    return interList

def parseToLabel(spiderInput):
    """Take the output of a MultiLangAttribute and parse it to IIIF label format."""
    
    labelData = {}
    for item in spiderInput:
        labelData[item] = [spiderInput[item]]
    return labelData

def parseImageDataToMediaInfo(imageData: dict) -> dict:
    """Take image info and parse it to a mediaInfo dict for making a MediaItem."""

    return {
        "id" : imageData["uri"],
        "type" : "Image",
        "format" : "image/" + imageData["fileformat"],
        "width" : imageData["width"],
        "height" : imageData["height"],
        "targetDims" : [0, 0, imageData["width"], imageData["height"]]
    }

def parseVideoDataToMediaInfo(videoData: dict) -> dict:
    """Take video info and parse it to a mediaInfo dict for making a MediaItem."""

    return {
        "id" : videoData["uri"],
        "type" : "Video",
        "format" : "video/" + videoData["fileformat"],
        "width" : videoData["width"],
        "height" : videoData["height"],
        "targetDims" : [0, 0, videoData["width"], videoData["height"]],
        "duration" : videoData["duration"],
        "targetStart" : 0,
        "targetEnd" : videoData["duration"]
    }

def parseNodeToIIIFMediaItem(node, type: str) -> dict:
    """
    Take a spider node and parse it to a mediaInfo dict for making a MediaItem.
    
    TODO: use node.start, node.end and node.region to select PARTS of the media to be used.
    """

    returnData = {
        "id" : "",
        "type" : "",
        "format" : "",
        "width" : 0,
        "height" : 0
    }

    if node.format.uri != None:
        returnData["id"] = node.format.uri
    if node.format.type != None:
        returnData["type"] = node.format.type.capitalize()
    if node.format.fileFormat != None and node.format.type != None:
        returnData["format"] = node.format.type + "/" + node.format.fileFormat
    
    if node.format.fullDimensions != None:
        returnData["width"] = node.format.fullDimensions[0]
        returnData["height"] = node.format.fullDimensions[1]

    if node.format.fullDuration != None:
        returnData["duration"] = node.format.fullDuration / 1000.0
    
    # When main element:
    if type == "page":
        returnData["targetDims"] = [0, 0, node.format.fullDimensions[0], node.format.fullDimensions[1]]
        if node.format.fullDuration != None:
            returnData["targetStart"] = 0
            returnData["targetEnd"] = node.format.fullDuration / 1000.0
        
    return returnData

def updateMediaItemToIntra(mediaItem, bespokeData: dict):
    """Take an existing media item, and update it as an intra-ducmentary annotation."""

    mediaItem.target = parseNestedNodeRegions(bespokeData["node"], mediaItem.target)
    mediaItem.body.value = bespokeData["node"].title[list(bespokeData["node"].title.keys())[0]]

    return mediaItem

def updateMediaItemToInter(mediaItem, bespokeData: dict):
    """Take an existing media item, and update it as an inter-ducmentary annotation."""

    # Get the path to the target manifest for linking:
    targetManifestPath = parseTargetManifestPath(bespokeData["node"], bespokeData["path"])
    
    # Collect metadata:
    edgeDescription = bespokeData["edge"].description[list(bespokeData["edge"].description.keys())[0]]
    nodeTitle = bespokeData["node"].title[list(bespokeData["node"].title.keys())[0]]

    # Update mediaItem fields:
    mediaItem.body.value = nodeTitle + " (" + edgeDescription + ")."
    mediaItem.body.id = ""
    mediaItem.id = mediaItem.id + "#" + targetManifestPath
    mediaItem.target = parseEdgeResions(bespokeData["regions"], mediaItem.target)

    return mediaItem

def updateMediaItemToNetworkxNode(mediaItem, bespokeData: dict):
    """Take an existing media item, and update it as a networkx node annotation."""

    # Get the path to the target manifest for linking:
    targetManifestPath = parseTargetManifestPath(bespokeData["node"], bespokeData["path"])
    
    # Collect metadata:
    nodeTitle = bespokeData["node"].title[list(bespokeData["node"].title.keys())[0]]

    # Update mediaItem fields:
    mediaItem.body.value = nodeTitle + "."
    mediaItem.body.id = ""
    mediaItem.id = mediaItem.id + "#" + targetManifestPath
    mediaItem.target = parseAnnotationDims(bespokeData["annotationDims"], mediaItem.target)

    return mediaItem

def parseTargetManifestPath(node, path: str) -> str:
    targetManifestPath = ""
    if node.instructionalMethod.important == False:
        targetManifestPath = os.path.join(path, "lower/" + str(node.uuid) + '.json')
    else:
        targetManifestPath = os.path.join(path, str(node.uuid) + '.json')

    return targetManifestPath

def parseNestedNodeRegions(node, originalTarget: str) -> str:
    """Update a media item target according to node"""

    # Get the path of the original target
    returnString = originalTarget.split("#")[0]

    if node.instructionalMethod.annotationPaint == True:
        # Get the drawing dimensions as strings:
        nodeX = str(node.instructionalMethod.annotationDisplayPos[0])
        nodeY = str(node.instructionalMethod.annotationDisplayPos[1] + 720)
        nodeW = str(node.format.fullDimensions[0])
        nodeH = str(node.format.fullDimensions[1])

        # Update the target:
        returnString = returnString + "#xywh=" + nodeX + "," + nodeY + "," + nodeW + "," + nodeH
        returnString = returnString + "&t=" + str(node.relation.sourceRegions[0]["start"] / 1000) + "," + str(node.relation.sourceRegions[0]["end"] / 1000)

    return returnString

def parseEdgeResions(regions: list, originalTarget: str) -> str:
    """Update media item target according to time regions."""

    # Get the path of the original string
    returnString = originalTarget.split("#")[0]
    
    # Parse region list:
    if regions != None:
        if len(regions) > 0:
            if "start" in regions[0]:
                returnString = returnString + "#t=" + str(regions[0]["start"] / 1000) + "," + str(regions[0]["end"] / 1000)
    
    return returnString

def parseAnnotationDims(annotationDims: list, originalTarget: str) -> str:
    """Update media item target according to annotation dimensions."""
    
    # Get the path of the original string
    returnString = originalTarget.split("#")[0]

    # Parse the dimesnion list:
    returnString = returnString + "#xywh=" + str(annotationDims[0]) + "," + str(annotationDims[1]) + "," + str(annotationDims[2]) + "," + str(annotationDims[2])
    return returnString