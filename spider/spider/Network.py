import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from .utils import *
import os
from .IIIF import *

class NetworkGraph():
    def __init__(self, web, **kwargs):
        self.G = nx.Graph()
        self.web = web
        self.nodeList = kwargs.get('nodeList', web.getFullList("nodes"))
        self.edgeList = kwargs.get('edgeList', web.getFullList("edges"))

        if isinstance(self.nodeList, list) == False:
            self.nodeList = self.nodeList.contentToList()
        if isinstance(self.edgeList, list) == False:
            self.edgeList = self.edgeList.contentToList()

        for nodeUUIDString in self.nodeList:
            node = self.web.loadNode(nodeUUIDString)
            self.G.add_node(str(node.uuid))

        for edgeUUIDString in self.edgeList:
            edge = web.loadEdge(edgeUUIDString)
            self.G.add_edge(edge.relation.source, edge.relation.target)

    def getGraph(self):
        return self.G

    def display(self):
        gCopy = self.G
        self.labelMap = {}
        for nodeUUIDString in self.nodeList:
            node = self.web.loadNode(nodeUUIDString)
            self.labelMap[nodeUUIDString] = node.title
        gCopy = nx.relabel_nodes(gCopy, self.labelMap)

        pos = nx.spring_layout(gCopy, seed=3068)
        nx.draw(gCopy, pos=pos, with_labels=True)
        plt.show()

    def saveToManifest(self, web, **kwargs):
        imagePath = os.path.join(kwargs.get("path", os.getcwd()), "media/" + kwargs.get("networkName", "Untitled_network").replace(" ", "_") + ".png")
        imageWritePath = os.path.join(kwargs.get("writePath", os.getcwd()), "media/" + kwargs.get("networkName", "Untitled_network").replace(" ", "_") + ".png")
        
        imgData = self.saveToImage(
            savePath = imageWritePath
        )
        
        networkxToManifest(web, imgData,
            imagePath = imagePath,
            networkName = kwargs.get("networkName", "Untitled_network"),
            path = kwargs.get("path", os.getcwd()),
            writePath = kwargs.get("writePath", os.getcwd())
        )
        pass

    def saveToImage(self, **kwargs):
        pos = nx.spring_layout(self.G, seed=3068)
        imgWidth = kwargs.get("width", 10000)
        imgHeight = kwargs.get("height", 10000)
        sizeMinMax = kwargs.get("sizeMinMax", [50, 200])
        savePath = kwargs.get("savePath", os.path.join(os.getcwd(), "IMG_OUTPUT.png"))
        edgeWidth = kwargs.get("edgeWidth", 10)

        finalImg = Image.new('RGBA',(imgWidth, imgHeight), (250,250,250, 0))
        draw = ImageDraw.Draw(finalImg)

        minMaxX = [None, None] # [minX, maxX]
        minMaxY = [None, None] # [minY, maxY]
        minMaxSize = [None, None]
        nodeInfo = {}
        for item in pos:
            if minMaxX[0] == None:
                minMaxX[0] = pos[item][0]
                minMaxX[1] = pos[item][0]
                minMaxY[0] = pos[item][1]
                minMaxY[1] = pos[item][1]
                minMaxSize = [len(list(self.G.neighbors(item))), len(list(self.G.neighbors(item)))]
            else:
                if pos[item][0] < minMaxX[0]:
                    minMaxX[0] = pos[item][0]
                if pos[item][0] > minMaxX[1]:
                    minMaxX[1] = pos[item][0]
                if pos[item][1] < minMaxY[0]:
                    minMaxY[0] = pos[item][1]
                if pos[item][1] > minMaxY[1]:
                    minMaxY[1] = pos[item][1]
                if len(list(self.G.neighbors(item))) < minMaxSize[0]:
                    minMaxSize[0] = len(list(self.G.neighbors(item)))
                if len(list(self.G.neighbors(item))) > minMaxSize[1]:
                    minMaxSize[1] = len(list(self.G.neighbors(item)))
            
            node = self.web.loadNode(item)
            nodeInfoEntry = {
                "numNeighbours" : len(list(self.G.neighbors(item))),
                "label" : node.title
            }
            nodeInfo[item] = nodeInfoEntry

        outData = {}    
        for item in pos:
            nodeSize = rescale(
                nodeInfo[item]["numNeighbours"], 
                minMaxSize[0], 
                minMaxSize[1],
                sizeMinMax[0],
                sizeMinMax[1]
            )
            nodeX = rescale(
                pos[item][0],
                minMaxX[0],
                minMaxX[1],
                sizeMinMax[1], imgWidth - sizeMinMax[1]
            )
            nodeY = rescale(
                pos[item][1],
                minMaxY[0],
                minMaxY[1],
                sizeMinMax[1], imgHeight - sizeMinMax[1]
            )

            outDataEntry = {
                "x" : nodeX,
                "y" : nodeY,
                "size" : nodeSize
            }
            outData[item] = outDataEntry

        for edgeUUID in self.edgeList:
            edge = self.web.loadEdge(edgeUUID)
            sourceInfo = outData[edge.relation.source]
            targetInfo = outData[edge.relation.target]

            draw.line(
                (
                    sourceInfo["x"] + (sourceInfo["size"] * 0.5), 
                    sourceInfo["y"] + (sourceInfo["size"] * 0.5), 
                    targetInfo["x"] + (targetInfo["size"] * 0.5), 
                    targetInfo["y"] + (targetInfo["size"] * 0.5)
                ),
                fill = (185, 187, 189),
                width = edgeWidth
            )

        for item in pos:
            draw.ellipse(
                (outData[item]["x"], outData[item]["y"], outData[item]["x"] + outData[item]["size"], outData[item]["y"] + outData[item]["size"]),
                fill=(124, 187, 217),
                outline=(142, 146, 148),
                width = 10
            )
        
        finalImg.save(savePath,"PNG")

        outData["meta"] = {"width" : imgWidth, "height" : imgHeight}


        return outData