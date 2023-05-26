class IIIFItem:
    """
    Base class for a IIIF item (manifest, canvas, annotation etc.)
    
    Spider gives a wrapper around the IIIF Presentation API 3 standard.
    For more information visit: https://iiif.io/api/presentation/3.0/

    Attributes
    ----------
    id : str
        ususally the path to the IIIF item

    type : str
        the type of the item (Manifest, Canvas, AnnotationPage etc.).

    Methods
    ----------
    collectData(self) -> dict
        return the item's attributs as a dict.

    parseToList(listKey: str) -> list
        parse a list of IIIFItem ojects as a list of their collectData dicts.
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", "")
        self.type = kwargs.get("type", "")

    def collectData(self) -> dict:
        """Return the item's attributs as a dict"""
        
        return {
            "id" : self.id,
            "type" : self.type
        }
    
    def parseToList(self, listKey: str) -> list:
        """Parse a list of IIIFItem ojects as a list of their collectData dicts."""

        returnList = []
        for item in getattr(self, listKey):
            if isinstance(item, dict):
                returnList.append(item)
            else:
                returnList.append(item.collectData())
        return returnList