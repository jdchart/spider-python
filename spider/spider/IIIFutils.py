import os

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
        "id" : node.format.uri,
        "type" : node.format.type.capitalize(),
        "format" : node.format.type + "/" + node.format.fileFormat,
        "width" : node.format.fullDimensions[0],
        "height" : node.format.fullDimensions[1]
    }

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