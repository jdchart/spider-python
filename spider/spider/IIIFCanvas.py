from .IIIFItem import *
from .IIIFAnnotationPage import *
import os

class Canvas(IIIFItem):
    """
    An OOP representation of a IIIF canvas.

    Build upon the IIIFItem base class.
    
    Attributes
    ----------
    label : dict
        the IIIF canvas's label.
        example: {"en" : ["title in english"], "fr" : ["titre en francais"]}
    
    item : list
        a list that will be populated with the canvas's items.

    annotation : list
        a list that will be populated with the canvas's annotations.

    thumbnail : list
        a list that will be populated with the canvas's thumbnails.

    width : int | float
        set the canvas's width

    height : int | float
        set the canvas's height

    duration : int | float
        set the canvas's duration

    Methods
    ----------
    collectData() -> dict
        return the canvas's data as a dict.

    addAnnotationPage(**kwargs) -> AnnotationPage
        add a new annotation page to the canvas's items or annotaitons list.
        Optionally provide the following kwargs:
        "type" = "page" or "annotation" (default: "page")
        "index" = the index of the item (default: len(items or annotations depending on type))
    """
    def __init__(self, **kwargs):
        
        # Set id and type
        super().__init__(id = kwargs.get("id", ""), type = "Canvas")
        
        # The canvas's label:
        self.label = kwargs.get("label", {})
        
        # Lists to be populated
        self.items = kwargs.get("items", [])
        self.annotations = kwargs.get("annotations", [])
        self.thumbnail = kwargs.get("thumbnail", [])

        # Dimensions:
        self.width = kwargs.get("width", 0)
        self.height = kwargs.get("height", 0)
        self.duration = kwargs.get("duration", None)

    def collectData(self) -> dict:
        """Return the canvas's data as a dict."""
        
        # Collect id and type:
        collectedSuper = super().collectData()
        
        # Collect local Canvas attributes
        collectedSuper["label"] = self.label
        collectedSuper["items"] = self.parseToList("items")
        collectedSuper["annotations"] = self.parseToList("annotations")
        collectedSuper["thumbnail"] = self.parseToList("thumbnail")
        collectedSuper["width"] = self.width
        collectedSuper["height"] = self.height
        if self.duration != None:
            collectedSuper["duration"] = self.duration
        return collectedSuper

    def addAnnotationPage(self, **kwargs) -> AnnotationPage:
        """
        Add a new annotation page to the canvas's items or annotaitons list.
        
        Optionally provide the following kwargs:
        "type" = "page" or "annotation" (default: "page")
        "index" = the index of the item (default: len(items or annotations depending on type))
        """

        # Get defualt index:
        index = 0
        if "index" not in kwargs:
            if kwargs.get("type", "page") == "page":
                index = len(self.items)
            elif kwargs.get("type", "page") == "annotation":
                index = len(self.annotations)
        else:
            index = kwargs.get("index")

        # Create the annotation page:
        newAnnotationPage = AnnotationPage(
            pageType = kwargs.get("type", "page"), 
            id = os.path.join(self.id, kwargs.get("type", "page") + "/" + str(index)),
            canvasID = self.id
        )

        # Add to the corresponding list:
        if kwargs.get("type", "page") == "page":
            self.items.append(newAnnotationPage)
        elif kwargs.get("type", "page") == "annotation":
            self.annotations.append(newAnnotationPage)
        return newAnnotationPage