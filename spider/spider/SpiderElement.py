import uuid
import datetime
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
            elif item in ["date", "startDateTime", "endDateTime"]:
                setattr(self, item, datetime.datetime.strptime(data[item], "%m-%d-%Y:%H:%M:%S"))
            elif item == "modificationDateTimes":
                finalArray = []
                for date in data[item]:
                    finalArray.append(datetime.datetime.strptime(date, "%m-%d-%Y:%H:%M:%S"))
                setattr(self, item, finalArray)
            else:
                setattr(self, item, data[item])
        
    def collectData(self):
        dataObj = super().collectData()
        dataObj["uuid"] = str(self.uuid)
        dataObj["path"] = self.path
        return dataObj