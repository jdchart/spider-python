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