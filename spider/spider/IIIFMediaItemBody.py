from .IIIFItem import *

class MediaItemBody(IIIFItem):
    """
    OOP structure for the body of a IIIF media item.
    
    Attributes
    ----------
    width : int | float
        set the item's width

    height : int | float
        set the item's height

    duration : int | float
        set the item's duration

    format : str
        set media item's format

    value : dict
        set media item's value
        example : {"en" : "value in english", "fr" : "value in french"}

    Methods
    ----------
    collectData() -> dict
        collect the item's data into a dict.
    """
    def __init__(self, **kwargs):

        # Set id and type (note, these point directly to the media file)
        super().__init__(id = kwargs.get("id", ""), type = kwargs.get("type", ""))

        # Media item information
        self.width = kwargs.get("width", 0)
        self.height = kwargs.get("height", 0)
        self.duration = kwargs.get("duration", None)
        self.format = kwargs.get("format", None)
        self.value = kwargs.get("value", None)

        if "read_data" in kwargs:
            self.read(kwargs.get("read_data"))

    def collectData(self) -> dict:
        """Collect the item's data into a dict"""

        # Gather id and type:
        collectedSuper = super().collectData()

        # Media body item local attributes:
        collectedSuper["format"] = self.format
        collectedSuper["width"] = self.width
        collectedSuper["height"] = self.height
        if self.duration != None:
            collectedSuper["duration"] = self.duration
        if self.value != None:
            collectedSuper["value"] = self.value

        return collectedSuper
    
    def read(self, read_data):
        self.id = read_data["id"]
        self.format = read_data["format"]
        self.type = read_data["type"]

        if "width" in read_data:
            self.width = read_data["width"]
        if "height" in read_data:
            self.height = read_data["height"]
        if "duration" in read_data:
            self.duration = read_data["duration"]
        if "value" in read_data:
            self.value = read_data["value"]
        