import os
import shutil
from .utils import *

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
        
        # IF NEEDED (nested nodes, probably needed when using collections):
        nestedNodes = node.getFullList()

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

    # Main title object
    labelObject = {}
    labelObject[node.language] = [node.title]

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

        # Add inter-documentary annotations:
        for j in range(len(interDocAnnotations)):
            thisEdge = web.loadEdge(interDocAnnotations[j])
            theOtherNode = None
            if str(node.uuid) == thisEdge.relation.source:
                theOtherNode = web.loadNode(thisEdge.relation.target)
            else:
                theOtherNode = web.loadNode(thisEdge.relation.source)
            annotationMediaItem = annotationLayer.addInterDocItem(j + 1, theOtherNode, thisEdge, kwargs.get('path', os.getcwd()))

    return newManifest

def getInterDocs(web, node, edgeList):
    # Return a list of edges in which the node is present as a source or a target:
    interList = []
    for item in edgeList:
        thisEdge = web.loadEdge(item)
        if str(node.uuid) == thisEdge.relation.source or str(node.uuid) == thisEdge.relation.target:
            interList.append(item)
    return interList


class IIIFItem:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", "")
        self.type = kwargs.get("type", "")

    def collectData(self):
        return {
            "id" : self.id,
            "type" : self.type
        }
    
    def parseToList(self, listKey):
        returnList = []
        for item in getattr(self, listKey):
            returnList.append(item.collectData())
        return returnList

class Manifest(IIIFItem):
    def __init__(self, **kwargs):
        self.path = kwargs.get("path", os.getcwd())
        self.writepath = kwargs.get("writepath", os.getcwd())
        self.filename = kwargs.get("filename", "untitled_manifest.json")
        self.label = kwargs.get("label", {})
        self.items = kwargs.get("items", [])

        super().__init__(id = os.path.join(self.path, self.filename), type = "Manifest")

    def collectData(self):
        collectedSuper = super().collectData()
        collectedSuper["@context"] = "http://iiif.io/api/presentation/3/context.json"
        collectedSuper["label"] = self.label
        collectedSuper["items"] = self.parseToList("items")
        return collectedSuper

    def write(self):
        writeJson(self.collectData(), os.path.join(self.writepath, self.filename))

    def addCanvas(self, index):
        newCanvas = Canvas(id = os.path.join(self.path, "canvas/" + str(index)), label = self.label)
        self.items.append(newCanvas)
        return newCanvas

class Canvas(IIIFItem):
    def __init__(self, **kwargs):
        super().__init__(id = kwargs.get("id", ""), type = "Canvas")
        self.label = kwargs.get("label", {})
        
        self.items = kwargs.get("items", [])
        self.annotations = kwargs.get("annotations", [])
        self.thumbnail = kwargs.get("thumbnail", [])

        self.width = kwargs.get("width", 0)
        self.height = kwargs.get("height", 0)
        self.duration = kwargs.get("duration", None)

    def collectData(self):
        collectedSuper = super().collectData()
        collectedSuper["label"] = self.label
        collectedSuper["items"] = self.parseToList("items")
        collectedSuper["annotations"] = self.parseToList("annotations")
        collectedSuper["thumbnail"] = self.parseToList("thumbnail")
        collectedSuper["width"] = self.width
        collectedSuper["height"] = self.height
        if self.duration != None:
            collectedSuper["duration"] = self.duration
        return collectedSuper

    def addAnnotationPage(self, type, index):
        newAnnotationPage = AnnotationPage(
            pageType = type, 
            id = os.path.join(self.id, type + "/" + str(index)),
            canvasID = self.id
        )
        if type == "page":
            self.items.append(newAnnotationPage)
        elif type == "annotation":
            self.annotations.append(newAnnotationPage)
        return newAnnotationPage

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

    def addInterDocItem(self, index, node, edge, path):
        newMediaItem = self.addMediaItem(index, node)

        targetManifestPath = ""
        if node.instructionalMethod.important == False:
            targetManifestPath = os.path.join(path, "lower/" + str(node.uuid) + '.json')
        else:
            targetManifestPath = os.path.join(path, str(node.uuid) + '.json')
        
        newMediaItem.body.value = node.title + " " + htmlLinkWrap(targetManifestPath, "Manifest") + " (" + edge.description + ")."
        newMediaItem.body.id = ""
        newMediaItem.id = newMediaItem.id + "#" + targetManifestPath
        return newMediaItem

class MediaItem(IIIFItem):
    def __init__(self, **kwargs):
        super().__init__(id = kwargs.get("id", ""), type = "Annotation")
        self.motivation = kwargs.get("motivation", "painting")
        
        self.targetID = kwargs.get('targetID', "")
        self.target = ""
        self.body = MediaItemBody()

        self.parseMediaInfo(kwargs.get("mediaInfo", {}))

    def parseMediaInfo(self, info):
        for item in info:
            setattr(self.body, item, info[item])
        
        self.target = self.targetID
        if "targetDims" in info:
            self.target = self.target + "#xywh="
            self.target = self.target + str(info["targetDims"][0]) + ","
            self.target = self.target + str(info["targetDims"][1]) + ","
            self.target = self.target + str(info["targetDims"][2]) + ","
            self.target = self.target + str(info["targetDims"][3])
        if 'targetStart' in info:
            self.target = self.target + "&t="
            self.target = self.target + str(info["targetStart"]) + ","
            self.target = self.target + str(info["targetEnd"])
        
    def collectData(self):
        collectedSuper = super().collectData()
        collectedSuper["motivation"] = self.motivation
        collectedSuper["target"] = self.target
        collectedSuper["body"] = self.body.collectData()

        return collectedSuper

class MediaItemBody:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", "")
        self.type = kwargs.get("type", "")
        self.width = kwargs.get("width", 0)
        self.height = kwargs.get("height", 0)
        self.duration = kwargs.get("duration", None)
        self.format = kwargs.get("format", None)
        self.value = kwargs.get("value", None)

    def collectData(self):
        toReturn = {
            "id" : self.id,
            "type" : self.type,
            "format" : self.format,
            "width" : self.width,
            "height" : self.height
        }
        if self.duration != None:
            toReturn["duration"] = self.duration
        if self.value != None:
            toReturn["value"] = self.value

        return toReturn

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