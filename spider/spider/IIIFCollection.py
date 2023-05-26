from .IIIFItem import *
from .IIIFManifest import *
import os
from .utils import *

class ManifestCollection(IIIFItem):
    def __init__(self, **kwargs):

        # Set arrtibutes
        self.path = kwargs.get("path", os.getcwd())
        self.writepath = kwargs.get("writepath", os.getcwd())
        self.filename = kwargs.get("filename", "untitled_manifest.json")
        self.label = kwargs.get("label", {})
        self.items = kwargs.get("items", [])
        self.metadata = kwargs.get("metadata", [])

        # Set the manifest's id and type:
        super().__init__(id = os.path.join(self.path, self.filename), type = "Collection")

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

    def addFullManifest(self, **kwargs) -> Manifest:
        """
        Add a new IIIF Canvas object to the manifest.
        
        Optionally provide an index (default: len(self.items)).
        """

        newManifest = Manifest(id = kwargs.get("manifest_id", ""), **kwargs)
        self.items.append(newManifest)
        return newManifest
    
    def addManifestRef(self, manifest_id):
        self.items.append({
            "id" : manifest_id
        })