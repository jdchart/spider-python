from .IIIFItem import *
from .IIIFMediaItem import *
from .IIIFutils import *
import os

class AnnotationPage(IIIFItem):
    """
    OOP structure representation of a IIIF AnnotationPage.
    
    Attributes
    ----------
    items : list
        a list that will be populated with the annotationPage's items.
    
    canvasID : str
        the ID of the canvas to which the annotation page belongs

    pageType : str
        the type of page to which the annotation page pertains ("page" or "annotation").

    Methods
    ----------
    collectData() -> dict
        collect the item's data into a dict.

    addMediaItem(**kwargs) -> MediaItem
        add a new media item to the annotation page.
        kwargs:
        index : int
            default len(self.items) + 1
        mediaInfo: dict
            a dict giving media info (default: {})
        bespokeItem: dict | None
            trigger additional operations according to a bespoke type of Media Item (default: None)
            provide a dict according to the type of bespoke item.
            examples: 
                {"type": "intra", "data" : {"node" : nodeObject}}
                {"type": "inter", "data" : {"node" : nodeObject, "edge" : edgeObject, "path" : "/", "regions" : [0, 1]}}
                {"type": "networkxNode", "data" : {"node" : nodeObject, "path" : "/", "annotationDims" : [0, 1, 2, 3]}}
    """
    def __init__(self, **kwargs):
        
        # Set id and type:
        super().__init__(id = kwargs.get("id", ""), type = "AnnotationPage")
        
        # The ID of the canvas to
        self.canvasID = kwargs.get("canvasID", "")
        self.pageType = kwargs.get("pageType", "page")
        self.items = kwargs.get("items", [])

        if "read_data" in kwargs:
            self.read(kwargs.get("read_data"))

    def collectData(self):
        """Collect the item's data into a dict."""

        # Collect id and type:
        collectedSuper = super().collectData()

        # Collect local level attributes:
        collectedSuper["items"] = self.parseToList("items")
        return collectedSuper
    
    def read(self, read_data):
        self.id = read_data["id"]
        self.type = read_data["type"]

        for item in read_data["items"]:
            self.addMediaItem(read_data = item)


    def addMediaItem(self, **kwargs) -> MediaItem:
        """
        Add a new media item to the annotation page.
        
        kwargs:
        index : int
            default len(self.items) + 1
        mediaInfo: dict
            a dict giving media info (default: {})
        bespokeItem: dict | None
            trigger additional operations according to a bespoke type of Media Item (default: None)
            provide a dict according to the type of bespoke item.
            examples: 
                {"type": "intra", "data" : {"node" : nodeObject}}
                {"type": "inter", "data" : {"node" : nodeObject, "edge" : edgeObject, "path" : "/", "regions" : [0, 1]}}
                {"type": "networkxNode", "data" : {"node" : nodeObject, "path" : "/", "annotationDims" : [0, 1, 2, 3]}}
        """

        # Create the media item:
        newMediaItem = MediaItem(
            id = os.path.join(self.id, str(kwargs.get("index", len(self.items) + 1))),
            targetID = self.canvasID,
            mediaInfo = kwargs.get("mediaInfo", {})
        )

        if "read_data" in kwargs:
            newMediaItem.read(read_data = kwargs.get("read_data"))
        else:
            # Update the media item's motivation according to page type:
            if self.pageType == "page":
                newMediaItem.motivation = "painting"
            elif self.pageType == "annotation":
                newMediaItem.motivation = "commenting"

            # Add the media item to items:    
            self.items.append(newMediaItem)

            # Update the media item according to bespoke criteria:
            if kwargs.get("bespokeItem", None) != None:
                if kwargs.get("bespokeItem")["type"] == "intra":
                    updateMediaItemToIntra(newMediaItem, kwargs.get("bespokeItem")["data"])
                if kwargs.get("bespokeItem")["type"] == "inter":
                    updateMediaItemToInter(newMediaItem, kwargs.get("bespokeItem")["data"])
                if kwargs.get("bespokeItem")["type"] == "networkxNode":
                    updateMediaItemToNetworkxNode(newMediaItem, kwargs.get("bespokeItem")["data"])

        return newMediaItem