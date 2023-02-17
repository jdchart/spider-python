import datetime
from .utils import *

class Coverage:
    def __init__(self, **kwargs):
        self.startDateTime = kwargs.get('startDateTime', None)
        self.endDateTime = kwargs.get('endDateTime', None)
        self.modificationDateTimes = kwargs.get('modificationDateTimes', [])
        self.region = kwargs.get('region', None)

        if kwargs.get('from_string', None) != None:
            self.fromString(kwargs.get('from_string'))

    def __str__(self):
        return str(self.collectData())

    def collectData(self):
        return {
            "startDateTime" : self.startDateTime,
            "endDateTime" : self.endDateTime,
            "modificationDateTimes" : self.modificationDateTimes,
            "region" : self.region,
        }
    
    def toString(self):
        returnString = ""
        if self.startDateTime != None:
            returnString = returnString + "&start=" + self.startDateTime.strftime("%m-%d-%Y:%H:%M:%S.%f")
        if self.endDateTime != None:
            returnString = returnString + "&end=" + self.endDateTime.strftime("%m-%d-%Y:%H:%M:%S.%f")
        if len(self.modificationDateTimes) > 0:
            returnString = returnString + "&modifications="
            for i in range(len(self.modificationDateTimes)):
                returnString = returnString + "&datetime=" + self.modificationDateTimes[i]["datetime"].strftime("%m-%d-%Y:%H:%M:%S.%f")
                returnString = returnString + "&title=" + self.modificationDateTimes[i]["title"].replace(" ", "&&_&&")
                returnString = returnString + "&description=" + self.modificationDateTimes[i]["description"].replace(" ", "&&_&&")
        if self.region != None:
            returnString = returnString + "&region=" + self.region.replace(" ", "&&_&&")
        return returnString

    def fromString(self, stringIn):
        mainSplit = stringKeySplit(["&start=", "&end=", "&modifications=", "&region="], stringIn)
        for i in range(len(mainSplit)):
            if mainSplit[i] == "&start=":
                self.startDateTime = datetime.datetime.strptime(mainSplit[i + 1], "%m-%d-%Y:%H:%M:%S.%f")
            if mainSplit[i] == "&end=":
                self.endDateTime = datetime.datetime.strptime(mainSplit[i + 1], "%m-%d-%Y:%H:%M:%S.%f")
            if mainSplit[i] == "&region=":
                self.region = mainSplit[i + 1].replace("&&_&&", " ")
            if mainSplit[i] == "&modifications=":
                modificationsSplit = stringKeySplit(["&datetime=", "&title=", "&description="], mainSplit[i + 1])
                toAdd = {}
                for j in range(len(modificationsSplit)):
                    if modificationsSplit[j] == "&datetime=":
                        toAdd["datetime"] = datetime.datetime.strptime(modificationsSplit[j + 1], "%m-%d-%Y:%H:%M:%S.%f")
                    elif modificationsSplit[j] == "&title=":
                        toAdd["title"] = modificationsSplit[j + 1].replace("&&_&&", " ")
                    elif modificationsSplit[j] == "&description=":
                        toAdd["description"] = modificationsSplit[j + 1].replace("&&_&&", " ")
                        self.modificationDateTimes.append(toAdd)
                        toAdd = {}