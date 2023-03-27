import uuid
from .DublinCore import *

class SpiderElement(Resource):
    """
    A basic Spider element (base for webs, nodes, edges and collection.)

    The base class for any spider element. Built upon the Dublin Core Rersource class.

    Attributes
    ----------
    uuid : str
        a unique identifier for the element as a string.

    path : str
        the path to the element on disk.

    tags : dict
        a dict of values (one entry for each language code).
        
    Methods
    ----------
    setFromReadData(data: dict) -> None
        set this object's attributes from a read dict.

    collectData() -> None
        collect this object's data into a dict.

    appendTag(value: str | list | dict) -> None
        append a new tag without removing old ones.
    """

    def __init__(self, **kwargs):
        # Init Dublin Core Resource class:
        super().__init__(**kwargs)

        # UUID converted to string:
        self.uuid = kwargs.get('uuid', str(uuid.uuid4()))
        
        # Private tags class:
        self._tags = {}
        self._tags = self._setTags(kwargs.get('tags', {}))
    
    def __str__(self):
        return str(self.collectData())

    def setFromReadData(self, data: dict) -> None:
        """Set this onject's attributes from a read dict"""
        
        for item in data:
            if item in ["uuid", "tags", "path"]:
                if item == "uuid":
                    setattr(self, item, uuid.UUID(data["uuid"]))
                if item == "tags":
                    setattr(self, "_" + item, data[item])
                else:
                    setattr(self, item, data[item])

        # Set the Dublin Core Resource's data:
        super().setFromReadData(data)

    def collectData(self) -> None:
        """Collect this object's data into a dict"""
        
        # Collect Dublin Core Resource's data:
        dataObj = super().collectData()
        
        # Collect this object's data:
        dataObj["uuid"] = self.uuid
        dataObj["path"] = self.path
        dataObj["tags"] = self._tags
        return dataObj


    def _setTags(self, value: str | list | dict, mode: str = "set") -> dict:
        """Parse variable input to tags"""

        # Sanitize the tags object according to langugage:
        originalTags = self._sanitizeTags()
        keyList = list(originalTags.keys())

        if type(value) == str:
            if mode == "set":
                originalTags[keyList[0]] = [value]
            elif mode == "append":
                originalTags[keyList[0]].append(value)
        elif type(value) == list:
            if mode == "set":
                originalTags[keyList[0]] = value
            elif mode == "append":
                for toAdd in value:
                    originalTags[keyList[0]].append(toAdd)
        elif type(value) == dict:
            for item in value:
                if item not in keyList:
                    originalTags[item] = []
                if type(value[item]) == str:
                    if mode == "set":
                        originalTags[item] = [value[item]]
                    elif mode == "append":
                        originalTags[item].append(value[item])
                elif type(value[item]) == list:
                    if mode == "set":
                        originalTags[item] = value[item]
                    elif mode == "append":
                        for toAdd in value[item]:
                            originalTags[item].append(toAdd)
            
            # Append missing languages.
            self.appendLanguage(list(value.keys()))
        
        return originalTags
    
    def appendTag(self, value: str | list | dict) -> None:
        """Append a new tag without removing old ones"""

        self._tags = self._setTags(value, "append")

    def _sanitizeTags(self) -> dict:
        """Sanitize tags according to language"""

        originalTags = self._tags

        for lang in self._language:
            if lang not in list(originalTags.keys()):
                originalTags[lang] = []

        return originalTags

    # Public tags attribute:
    @property
    def tags(self):
        return self._tags
    @tags.setter
    def tags(self, value):
        self._tags = self._setTags(value)