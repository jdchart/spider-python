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
        if len(self.sourceRegions) > 0:
            returnString = returnString + "&sourceRegions="
            for item in self.sourceRegions:
                returnString = returnString + "&newRegion="
                if "start" in item:
                    returnString = returnString + "&start=" + str(item["start"])
                if "end" in item:
                    returnString = returnString + "&end=" + str(item["end"])
                if "dims" in item:
                    if item["dims"][0] == -1:
                        returnString = returnString + "&dims=" + str(item["dims"][0])
                    else:
                        returnString = returnString + "&dims=" + str(item["dims"][0]) + ',' + str(item["dims"][1]) + ',' + str(item["dims"][2]) + ',' + str(item["dims"][3])
        if len(self.targetRegions) > 0:
            returnString = returnString + "&targetRegions="
            for item in self.targetRegions:
                if "start" in item:
                    returnString = returnString + "&start=" + str(item["start"])
                if "end" in item:
                    returnString = returnString + "&end=" + str(item["end"])
                if "dims" in item:
                    if item["dims"][0] == -1:
                        returnString = returnString + "&dims=" + str(item["dims"][0])
                    else:
                        returnString = returnString + "&dims=" + str(item["dims"][0]) + ',' + str(item["dims"][1]) + ',' + str(item["dims"][2]) + ',' + str(item["dims"][3])
        return returnString

    def fromString(self, stringIn):
        mainSplit = stringKeySplit(
            ["&source=", "&target=", "&sourceRegions=", "&targetRegions="], 
            stringIn
        )
        for i in range(len(mainSplit)):
            if mainSplit[i] == "&source=":
                self.source = mainSplit[i + 1]
            elif mainSplit[i] == "&target=":
                self.target = mainSplit[i + 1]
            elif mainSplit[i] == "&sourceRegions=":
                regionsSplit = stringKeySplit(["&newRegion="], mainSplit[i + 1])
                for j in range(len(regionsSplit)):
                    if regionsSplit[j] == "&newRegion=":
                        toAdd = {}
                        thisRegionSplit = stringKeySplit(["&start=", "&end=", "&dims="], regionsSplit[j + 1])
                        for k in range(len(thisRegionSplit)):
                            if thisRegionSplit[k] == "&start=":
                                toAdd["start"] = int(thisRegionSplit[k + 1])
                            if thisRegionSplit[k] == "&end=":
                                toAdd["end"] = int(thisRegionSplit[k + 1])
                            if thisRegionSplit[k] == "&dims=":
                                if thisRegionSplit[k + 1][0] == "-":
                                    toAdd["dims"] = [-1]
                                else:
                                    dimSplit = thisRegionSplit[k + 1].split(",")
                                    toAdd["dims"] = [int(dimSplit[0]), int(dimSplit[1]), int(dimSplit[2]), int(dimSplit[3])]
                        self.sourceRegions.append(toAdd)
            elif mainSplit[i] == "&targetRegions=":
                regionsSplit = stringKeySplit(["&newRegion="], mainSplit[i + 1])
                for j in range(len(regionsSplit)):
                    if regionsSplit[j] == "&newRegion=":
                        toAdd = {}
                        thisRegionSplit = stringKeySplit(["&start=", "&end=", "&dims="], regionsSplit[j + 1])
                        for k in range(len(thisRegionSplit)):
                            if thisRegionSplit[k] == "&start=":
                                toAdd["start"] = int(thisRegionSplit[k + 1])
                            if thisRegionSplit[k] == "&end=":
                                toAdd["end"] = int(thisRegionSplit[k + 1])
                            if thisRegionSplit[k] == "&dims=":
                                if thisRegionSplit[k + 1][0] == "-":
                                    toAdd["dims"] = [-1]
                                else:
                                    dimSplit = thisRegionSplit[k + 1].split(",")
                                    toAdd["dims"] = [int(dimSplit[0]), int(dimSplit[1]), int(dimSplit[2]), int(dimSplit[3])]
                        self.targetRegions.append(toAdd)