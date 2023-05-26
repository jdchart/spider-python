from .IIIFItem import *
from .IIIFCanvas import *
import os
from .utils import *

class Manifest(IIIFItem):
    """
    An OOP representation of a IIIF manifest.

    Build upon the IIIFItem base class.
    
    Attributes
    ----------
    path : str
        the IIIF folder path where the resource is found (for example, the path in a git repo, or a path on a server).

    writepath : str
        the local folder path on disk to write the manifest.

    filename : str
        the filename of the manifest, must end with ".json".

    label : dict
        the IIIF manifest's label.
        example: {"en" : ["title in english"], "fr" : ["titre en francais"]}

    item : list
        a list that will be populated with the manifest's items.

    Methods
    ----------
    collectData() -> dict
        return the manifest's data as a dict.

    write() -> None
        write the manifest to it's writepath.

    addCanvas(**kwargs) -> Canvas
        add a new IIIF Canvas object to the manifest.
        Optionally provide an index (default: len(self.items)).
    """
    def __init__(self, **kwargs):

        # Set arrtibutes
        self.path = kwargs.get("path", os.getcwd())
        self.writepath = kwargs.get("writepath", os.getcwd())
        self.filename = kwargs.get("filename", "untitled_manifest.json")
        self.label = kwargs.get("label", {})
        self.items = kwargs.get("items", [])
        self.metadata = kwargs.get("metadata", [])

        # Set the manifest's id and type:
        super().__init__(id = os.path.join(self.path, self.filename), type = "Manifest")

    def collectData(self) -> dict:
        """Return the manifest's data as a dict."""
        
        # Get the IIIFItem's data
        collectedSuper = super().collectData()

        # Manifest's local data
        collectedSuper["@context"] = "http://iiif.io/api/presentation/3/context.json"
        collectedSuper["label"] = self.label
        collectedSuper["items"] = self.parseToList("items")
        collectedSuper["metadata"] = self.metadata
        return collectedSuper

    def write(self) -> None:
        """Write the manifest to it's writepath."""

        writeJson(self.collectData(), os.path.join(self.writepath, self.filename))

    def addCanvas(self, **kwargs) -> Canvas:
        """
        Add a new IIIF Canvas object to the manifest.
        
        Optionally provide an index (default: len(self.items)).
        """

        newCanvas = Canvas(id = os.path.join(self.path, "canvas/" + str(kwargs.get("index", len(self.items) + 1))), label = self.label, **kwargs)
        self.items.append(newCanvas)
        return newCanvas