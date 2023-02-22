import uuid
from .DublinCore import *

class SpiderElement(Resource):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.uuid = kwargs.get('uuid', uuid.uuid4())
        self.tags = kwargs.get('tags', [])
        self.color = kwargs.get('color', "#000000")
        self.important = kwargs.get('important', False)
    
    def __str__(self):
        return str(self.collectData())

    def setFromReadData(self, data):
        for item in data:
            if item == "uuid":
                setattr(self, item, uuid.UUID(data["uuid"]))
            else:
                setattr(self, item, data[item])

        super().setFromReadData(data)
        
    def collectData(self):
        dataObj = super().collectData()
        dataObj["uuid"] = str(self.uuid)
        dataObj["path"] = self.path
        dataObj["tags"] = self.tags
        return dataObj