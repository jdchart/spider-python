import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from .utils import *
import os
from .IIIF import *
import math

class NetworkGraph():
    """
    Wrapper around a networkx Graph()
    
    Attributes
    ----------
    G : nx.Graph()
        the actual networkx Graph() that will be populated.
        
    web : Web
        the spider wbe that is being converted.

    nodeList : list
        a list of node UUIDs that exist in the web.
        Default: all nodes. Can supply as a kwarg a list, or a Collection.
    
    edgeList : list
        a list of edge UUIDs that exist in the web.
        Default: all edges. Can supply as a kwarg a list, or a Collection.

    Methods
    ----------
    getGraph() -> nx.Graph
        return the networkx graph object.

    display(**kwargs) -> None
        display the graph in a matplotlib GUI window.
    """
    def __init__(self, web, **kwargs):

        # Create the graph:
        self.G = nx.Graph()

        # Set the web:
        self.web = web

        # Set the node and edge lists (defaults to all nodes and edges).
        self.nodeList = kwargs.get('nodeList', web.getFullList("nodes"))
        self.edgeList = kwargs.get('edgeList', web.getFullList("edges"))

        # Check the list type. If list, use that, if not, treat as a Collection and convert to list:
        if isinstance(self.nodeList, list) == False:
            self.nodeList = self.nodeList.contentToList()
        if isinstance(self.edgeList, list) == False:
            self.edgeList = self.edgeList.contentToList()

        # Populate the graph:
        self._populateNetworkxGraph()

    def _populateNetworkxGraph(self) -> None:
        """Populate the networkx graph from lists"""

        for nodeUUIDString in self.nodeList:
            node = self.web.loadNode(nodeUUIDString)
            self.G.add_node(node.uuid)

        for edgeUUIDString in self.edgeList:
            edge = self.web.loadEdge(edgeUUIDString)
            self.G.add_edge(edge.relation.source, edge.relation.target)

    def getGraph(self) -> nx.Graph:
        """Return the networkx graph object."""

        return self.G

    def display(self, **kwargs) -> None:
        """
        Display the graph in a matplotlib GUI window.

        You can supply a "algo" kwarg to define the layout algorithm:
            "spring" (default), "circular", "fr", "spectral", "random"
        
        You can also supply a "labelAttribute" kwarg (default: "title")
        """

        # Create a copy of the graph:
        gCopy = self.G

        # Relabel nodes
        labelMap = self._labelNodes(kwargs.get("labelAttribute", "title"))
        gCopy = nx.relabel_nodes(gCopy, labelMap)

        # Get positions for display:
        pos = self._applyLayout(gCopy, kwargs.get("algo", "spring"))
        
        # Draw and display the graph:
        nx.draw(gCopy, pos=pos, with_labels=True)
        plt.show()

    def _labelNodes(self, labelAttribute: str) -> None:
        """Return a label map for display."""
        
        labelMap = {}
        for nodeUUIDString in self.nodeList:
            node = self.web.loadNode(nodeUUIDString)
            retrieved = getattr(node, labelAttribute)
            labelMap[nodeUUIDString] = retrieved[list(retrieved.keys())[0]]
        
        return labelMap

    def _applyLayout(self, graph: nx.Graph, algo: str) -> dict:
        """Apply a layout algorithm to a network graph."""

        if "algo" == "spring":
            pos = nx.spring_layout(graph, seed=3068)
        elif "algo" == "circular":
            pos = nx.circular_layout(graph)
        elif "algo" == "fr":
            pos = nx.fruchterman_reingold_layout(graph)
        elif "algo" == "spectral":
            pos = nx.spectral_layout(graph)
        elif "algo" == "random":
            pos = nx.random_layout(graph)
        else:
            pos = nx.spring_layout(graph, seed=3068)

        return pos

    def saveToImage(self, **kwargs) -> dict:
        """
        Output the image to a network and return the draw data used to make the image.

        kwargs:
        algo : str
            layout algorithm to apply (default: "spring").

        savePath : str
            the path on disk to save the image (default: os.path.join(os.getcwd(), "IMG_OUTPUT.png")).
            Must be a PNG
        
        width : int
            image width (default: 1000)

        height : int
            image height (default: 1000)

        sizeMinMax : list
            a list of minimum and maximum node sizes (default: [width / 200, width / 50])

        bgCol : tuple
            RGBA for background color (default: (250,250,250,0))

        edgeWidth : int
            draw width for edges and node border (default: width / 1000)

        edgeCol : tuple
            edge draw color (default: (185, 187, 189))
        
        nodeCol : tuple
            node draw color (default: (124, 187, 217))
        
        nodeOutlineCol : tuple
            node outline draw color (default: (142, 146, 148))
        """

        # Create a copy of the graph and get positions for display:
        gCopy = self.G
        pos = self._applyLayout(gCopy, kwargs.get("algo", "spring"))

        # Collect drawing parameters:
        imgWidth = kwargs.get("width", 1000)
        imgHeight = kwargs.get("height", 1000)
        sizeMinMax = kwargs.get("sizeMinMax", [int(math.floor(imgWidth / 200)), int(math.floor(imgWidth / 50))])
        bgCol = kwargs.get("bgCol", (250,250,250,0))
        edgeWidth = kwargs.get("edgeWidth", int(math.floor(imgWidth / 1000)))
        edgeCol = kwargs.get("edgeCol", (185, 187, 189))
        nodeCol = kwargs.get("nodeCol", (124, 187, 217))
        nodeOutlineCol = kwargs.get("nodeOutlineCol", (142, 146, 148))
        
        # Set output path:
        savePath = kwargs.get("savePath", os.path.join(os.getcwd(), "IMG_OUTPUT.png"))
        
        # Create image object and draw context:
        finalImg = Image.new('RGBA',(imgWidth, imgHeight), bgCol)
        draw = ImageDraw.Draw(finalImg)

        minMaxX = [None, None]
        minMaxY = [None, None]
        minMaxSize = [None, None]
        nodeInfo = {}

        # Process minMax for x y and collect neighbours.
        self._parseMinMaxAndNeighbors(gCopy, pos, minMaxX, minMaxY, minMaxSize, nodeInfo)

        # Rescale data and prepare return dict.
        outData = {"meta" : {"width" : imgWidth, "height" : imgHeight}}    
        self._rescaleData(pos, minMaxX, minMaxY, minMaxSize, nodeInfo, sizeMinMax, imgWidth, imgHeight, outData)

        # Draw edges:
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
                fill = edgeCol,
                width = edgeWidth
            )

        # Draw nodes:
        for item in pos:
            draw.ellipse(
                (outData[item]["x"], outData[item]["y"], outData[item]["x"] + outData[item]["size"], outData[item]["y"] + outData[item]["size"]),
                fill=nodeCol,
                outline=nodeOutlineCol,
                width = edgeWidth
            )
        
        # Save the final image:
        finalImg.save(savePath,"PNG")

        return outData
    
    def _parseMinMaxAndNeighbors(self, gr: nx.Graph, nodePositions: dict, mmX: list, mmY: list, mmSize: list, nodeInfoDict: dict) -> None:
        """Parse position data to get minMax's for x, y and size, and collect the number of neighbours."""

        for item in nodePositions:
            if mmX[0] == None:
                mmX[0] = nodePositions[item][0]
                mmX[1] = nodePositions[item][0]
                mmY[0] = nodePositions[item][1]
                mmY[1] = nodePositions[item][1]
                mmSize[0] = len(list(gr.neighbors(item)))
                mmSize[1] = len(list(gr.neighbors(item)))
            else:
                if nodePositions[item][0] < mmX[0]:
                    mmX[0] = nodePositions[item][0]
                if nodePositions[item][0] > mmX[1]:
                    mmX[1] = nodePositions[item][0]
                if nodePositions[item][1] < mmY[0]:
                    mmY[0] = nodePositions[item][1]
                if nodePositions[item][1] > mmY[1]:
                    mmY[1] = nodePositions[item][1]
                if len(list(gr.neighbors(item))) < mmSize[0]:
                    mmSize[0] = len(list(gr.neighbors(item)))
                if len(list(gr.neighbors(item))) > mmSize[1]:
                    mmSize[1] = len(list(gr.neighbors(item)))
            
            node = self.web.loadNode(item)
            nodeInfoEntry = {
                "numNeighbours" : len(list(gr.neighbors(item))),
                "label" : node.title
            }
            nodeInfoDict[item] = nodeInfoEntry

    def _rescaleData(self, nodePositions: dict, mmX: list, mmY: list, mmSize: list, nodeInfoDict: dict, mmImgSize: list, imgW: int, imgH: int, outDataDict: dict) -> None:
        """Rescale data according to draw parameters"""
        
        for item in nodePositions:
            nodeSize = rescale(
                nodeInfoDict[item]["numNeighbours"], 
                mmSize[0], 
                mmSize[1],
                mmImgSize[0],
                mmImgSize[1]
            )
            nodeX = rescale(
                nodePositions[item][0],
                mmX[0],
                mmX[1],
                mmImgSize[1], imgW - mmImgSize[1]
            )
            nodeY = rescale(
                nodePositions[item][1],
                mmY[0],
                mmY[1],
                mmImgSize[1], imgH - mmImgSize[1]
            )

            outDataEntry = {
                "x" : nodeX,
                "y" : nodeY,
                "size" : nodeSize
            }
            outDataDict[item] = outDataEntry
    
    def saveToManifest(self, web, **kwargs):
        imagePath = os.path.join(kwargs.get("path", os.getcwd()), "media/" + kwargs.get("networkName", "Untitled_network").replace(" ", "_") + ".png")
        imageWritePath = os.path.join(kwargs.get("writePath", os.getcwd()), "media/" + kwargs.get("networkName", "Untitled_network").replace(" ", "_") + ".png")
        
        imgData = self.saveToImage(
            savePath = imageWritePath,
            algo = kwargs.get("algo", "spring")
        )
        
        networkxToManifest(web, imgData,
            imagePath = imagePath,
            networkName = kwargs.get("networkName", "Untitled_network"),
            path = kwargs.get("path", os.getcwd()),
            writePath = kwargs.get("writePath", os.getcwd())
        )