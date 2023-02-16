from .utils import *

class Relation:
    def __init__(self, **kwargs):
        self.source = kwargs.get('source', None)
        self.target = kwargs.get('target', None)

        self.sourceRegions = kwargs.get('sourceRegions', [])
        self.targetRegions = kwargs.get('targetRegions', [])

        if kwargs.get('from_string', None) != None:
            self.fromString(kwargs.get('from_string'))

    def __str__(self):
        return str(self.collectData())

    def collectData(self):
        return {
            "source" : self.source,
            "target" : self.target,
            "sourceRegions" : self.sourceRegions,
            "targetRegions" : self.targetRegions
        }

    def toString(self):
        returnString = ""
        if self.source != None:
            returnString = returnString + "&source=" + self.source
        if self.target != None:
            returnString = returnString + "&target=" + self.target
        '''
        if len(self.sourceRegions) > 0:
            returnString = returnString + "&sourceRegions="
            for item in self.sourceRegions:
                returnString = returnString + "&start=" 
        '''


        return returnString

    def fromString(self, stringIn):
        mainSplit = stringKeySplit(
            ["&source=", "&target="], 
            stringIn
        )
        for i in range(len(mainSplit)):
            if mainSplit[i] == "&source=":
                self.source = mainSplit[i + 1]
            elif mainSplit[i] == "&target=":
                self.target = mainSplit[i + 1]