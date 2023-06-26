from .IIIFItem import *
from .IIIFMediaItemBody import *

class MediaItem(IIIFItem):
    """
    OOP structure for a IIIF media item.
    
    Attributes
    ----------
    motivation : str
        IIIF motiation, "painting", "commenting"

    targetID : str
        target before parsing media info

    target : str
        target with media info

    body : MediaItemBody
        object containing info pertaining to the media.

    Methods
    ----------
    collectData() -> dict
        collect the item's data into a dict.
    """
    def __init__(self, **kwargs):
        
        # Set the id and type
        super().__init__(id = kwargs.get("id", ""), type = "Annotation")
        
        # Local attributes
        self.motivation = kwargs.get("motivation", "painting")
        
        # Target ID is te path before painting info
        self.targetID = kwargs.get('targetID', "")
        # Target will be the parsed target:
        self.target = ""
        # Body pertains to the actual media data
        self.body = MediaItemBody()

        # Parse media info to body and get final target
        self._parseMediaInfo(kwargs.get("mediaInfo", {}))

        if "read_data" in kwargs:
            self.read(kwargs.get("read_data"))

    def collectData(self) -> dict:
        """Collect the item's data into a dict."""

        # Collect id and type:
        collectedSuper = super().collectData()

        # Collect local level attributes:
        collectedSuper["motivation"] = self.motivation
        collectedSuper["target"] = self.target
        collectedSuper["body"] = self.body.collectData()

        return collectedSuper
    
    def read(self, read_data):
        self.id = read_data["id"]
        self.type = read_data["type"]
        self.motivation = read_data["motivation"]
        self.target = read_data["target"]

        if "body" in read_data:
            self.body = MediaItemBody(read_data = read_data["body"])


    def _parseMediaInfo(self, info: dict) -> None:
        """Set the final target from media data and update the body."""

        # Update body:
        for item in info:
            setattr(self.body, item, info[item])
        
        # Update target:
        self.target = self.targetID
        hadDims = False
        if "targetDims" in info:
            self.target = self.target + "#xywh="
            self.target = self.target + str(info["targetDims"][0]) + ","
            self.target = self.target + str(info["targetDims"][1]) + ","
            self.target = self.target + str(info["targetDims"][2]) + ","
            self.target = self.target + str(info["targetDims"][3])
            hadDims = True
        if 'targetStart' in info:
            if hadDims == True:
                self.target = self.target + "&t="
            else:
                self.target = self.target + "#t="
            self.target = self.target + str(info["targetStart"]) + ","
            self.target = self.target + str(info["targetEnd"])