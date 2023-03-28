from .IIIFItem import *
from .IIIFMediaItem import *
import os

class AnnotationPage(IIIFItem):
    def __init__(self, **kwargs):
        super().__init__(id = kwargs.get("id", ""), type = "AnnotationPage")
        self.canvasID = kwargs.get("canvasID", "")
        self.pageType = kwargs.get("pageType", "page")
        self.items = kwargs.get("items", [])

    def collectData(self):
        collectedSuper = super().collectData()
        collectedSuper["items"] = self.parseToList("items")
        return collectedSuper

    def addMediaItemFromImageData(self, index, imageData):
        newMediaItem = MediaItem(
            id = os.path.join(self.id, str(index)),
            targetID = self.canvasID,
            mediaInfo = {
                "id" : imageData["uri"],
                "type" : "Image",
                "format" : "image/png",
                "width" : imageData["width"],
                "height" : imageData["height"],
                "targetDims" : [0, 0, imageData["width"], imageData["height"]]
            }
        )

        if self.pageType == "page":
            newMediaItem.motivation = "painting"
        elif self.pageType == "annotation":
            newMediaItem.motivation = "commenting"
        self.items.append(newMediaItem)

        return newMediaItem

    def addMediaItem(self, index, node):
        mediaInfo = nodeToIIIFMediaItem(node, self.pageType)

        newMediaItem = MediaItem(
            id = os.path.join(self.id, str(index)),
            targetID = self.canvasID,
            mediaInfo = mediaInfo
        )
        if self.pageType == "page":
            newMediaItem.motivation = "painting"
        elif self.pageType == "annotation":
            newMediaItem.motivation = "commenting"
        self.items.append(newMediaItem)

        return newMediaItem

    def addIntraDocItem(self, index, node, **kwargs):
        newMediaItem = self.addMediaItem(index, node)

        newMediaItem.target = parseNestedNodeRegions(node, newMediaItem.target)
        newMediaItem.body.value = node.getFromLang("title", kwargs.get("lang", None))

        return newMediaItem

    def addNodeAnnotation(self, index, node, annotationDims, path, **kwargs):
        newMediaItem = self.addMediaItem(index, node)

        targetManifestPath = ""
        if node.instructionalMethod.important == False:
            targetManifestPath = os.path.join(path, "lower/" + str(node.uuid) + '.json')
        else:
            targetManifestPath = os.path.join(path, str(node.uuid) + '.json')
        
        #newMediaItem.body.value = node.getFromLang("title", kwargs.get("lang", None)) + " " + htmlLinkWrap(targetManifestPath, "Manifest") + "."
        newMediaItem.body.value = node.getFromLang("title", kwargs.get("lang", None)) + "."
        newMediaItem.body.id = ""
        newMediaItem.id = newMediaItem.id + "#" + targetManifestPath
        newMediaItem.target = parseAnnotationDims(annotationDims, newMediaItem.target)

        return newMediaItem

    def addInterDocItem(self, index, node, edge, regions, path, **kwargs):
        newMediaItem = self.addMediaItem(index, node)

        targetManifestPath = ""
        if node.instructionalMethod.important == False:
            targetManifestPath = os.path.join(path, "lower/" + str(node.uuid) + '.json')
        else:
            targetManifestPath = os.path.join(path, str(node.uuid) + '.json')
        
        #newMediaItem.body.value = node.getFromLang("title", kwargs.get("lang", None)) + " " + htmlLinkWrap(targetManifestPath, "Manifest") + " (" + edge.getFromLang("description", kwargs.get("lang", None)) + ")."
        newMediaItem.body.value = node.getFromLang("title", kwargs.get("lang", None)) + " (" + edge.getFromLang("description", kwargs.get("lang", None)) + ")."
        newMediaItem.body.id = ""
        newMediaItem.id = newMediaItem.id + "#" + targetManifestPath
        newMediaItem.target = parseEdgeResions(regions, newMediaItem.target)

        return newMediaItem
    
def nodeToIIIFMediaItem(node, type):
    returnData = {}
    returnData["id"] = node.format.uri
    returnData["type"] = node.format.type.capitalize()
    returnData["format"] = node.format.type + "/" + node.format.fileFormat
    returnData["width"] = node.format.fullDimensions[0]
    returnData["height"] = node.format.fullDimensions[1]
    if node.format.fullDuration != None:
        returnData["duration"] = node.format.fullDuration / 1000.0
    
    # Can use node.start, node.end and node.region to select PARTS of the media to be used

    # When main element:
    if type == "page":
        returnData["targetDims"] = [0, 0, node.format.fullDimensions[0], node.format.fullDimensions[1]]
        if node.format.fullDuration != None:
            returnData["targetStart"] = 0
            returnData["targetEnd"] = node.format.fullDuration / 1000.0
        
    return returnData

def parseNestedNodeRegions(node, originalTarget):
    returnString = originalTarget.split("#")[0]

    nodeX = str(node.instructionalMethod.annotationDisplayPos[0])
    nodeY = str(node.instructionalMethod.annotationDisplayPos[1] + 720)
    nodeW = str(node.format.fullDimensions[0])
    nodeH = str(node.format.fullDimensions[1])

    returnString = returnString + "#xywh=" + nodeX + "," + nodeY + "," + nodeW + "," + nodeH
    returnString = returnString + "&t=" + str(node.relation.sourceRegions[0]["start"] / 1000) + "," + str(node.relation.sourceRegions[0]["end"] / 1000)

    return returnString

def parseAnnotationDims(annotationDims, originalTarget):
    returnString = originalTarget.split("#")[0]

    returnString = returnString + "#xywh=" + str(annotationDims[0]) + "," + str(annotationDims[1]) + "," + str(annotationDims[2]) + "," + str(annotationDims[2])
    return returnString

def parseEdgeResions(regions, originalTarget):
    returnString = originalTarget.split("#")[0]
    if regions != None:
        if len(regions) > 0:
            if "start" in regions[0]:
                returnString = returnString + "#t=" + str(regions[0]["start"] / 1000) + "," + str(regions[0]["end"] / 1000)
    return returnString