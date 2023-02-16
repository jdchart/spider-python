from .utils import *

class Format:
    def __init__(self, **kwargs):
        self.type = kwargs.get('type', None)
        self.fileFormat = kwargs.get('fileFormat', None)
        self.uri = kwargs.get('uri', None)
        
        self.fullDuration = kwargs.get('fullDuration', None)
        self.start = kwargs.get('start', None)
        self.end = kwargs.get('end', None)
        
        self.fullDimensions = kwargs.get('fullDimensions', None)
        self.region = kwargs.get('region', None)

        self.pages = kwargs.get('pages', None)

        self.parseDuration()
        self.parseDimensions()
        
        if kwargs.get('from_string', None) != None:
            self.fromString(kwargs.get('from_string'))

    def __str__(self):
        return str(self.collectData())

    def collectData(self):
        return {
            "type" : self.type,
            "fileFormat" : self.fileFormat,
            "fullDuration" : self.fullDuration,
            "start" : self.start,
            "end" : self.end,
            "fullDimensions" : self.fullDimensions,
            "region" : self.region,
            "uri" : self.uri,
            "pages" : self.pages
        }

    def parseDuration(self):
        if self.fullDuration == None:
            if self.start != None and self.end != None:
                self.fullDuration = self.end - self.start
            elif self.end != None:
                self.duration = self.end
                self.start = -1

    def parseDimensions(self):
        if self.fullDimensions == None and self.region != None:
            if len(self.region) > 1:
                self.fullDimensions = [self.region[2], self.region[3]]
        if self.region == None and self.fullDimensions != None:
            self.region = [-1]

    def toString(self):
        returnString = ""
        if self.type != None:
            returnString = returnString + "&type=" + self.type
        if self.fileFormat != None:
            returnString = returnString + "&fileformat=" + self.fileFormat
        if self.fullDuration != None:
            returnString = returnString + "&duration-full=" + str(self.fullDuration)
        if self.start != None:
            returnString = returnString + "&duration-start=" + str(self.start)
        if self.end != None:
            returnString = returnString + "&duration-end=" + str(self.end)
        if self.fullDimensions != None:
            returnString = returnString + "&dimensions-full=" + str(self.fullDimensions[0]) + "," + str(self.fullDimensions[1])
        if self.region != None:
            if(self.region[0] == -1):
                returnString = returnString + "&dimensions-region=" + str(self.region[0])
            else:
                returnString = returnString + "&dimensions-region=" + str(self.region[0]) + "," + str(self.region[1]) + "," + str(self.region[2]) + "," + str(self.region[3])
        if self.uri != None:
            returnString = returnString + "&uri=" + self.uri
        if self.pages != None:
            returnString = returnString + "&pages=" + str(self.pages)
        return returnString

    def fromString(self, stringIn):
        mainSplit = stringKeySplit(
            ["&type=", "&fileformat=", "&duration-full=", "&duration-start=", "&duration-end=", "&dimensions-full=", "&dimensions-region=", "&uri=", "&pages="], 
            stringIn
        )
        for i in range(len(mainSplit)):
            if mainSplit[i] == "&type=":
                self.type = mainSplit[i + 1]
            elif mainSplit[i] == "&fileformat=":
                self.fileFormat = mainSplit[i + 1]
            elif mainSplit[i] == "&duration-full=":
                self.fullDuration = int(mainSplit[i + 1])
            elif mainSplit[i] == "&duration-start=":
                self.start = int(mainSplit[i + 1])
            elif mainSplit[i] == "&duration-end=":
                self.end = int(mainSplit[i + 1])
            elif mainSplit[i] == "&dimensions-full=":
                fullDimSplit = mainSplit[i + 1].split(',')
                self.fullDimensions = [int(fullDimSplit[0]), int(fullDimSplit[1])]
            elif mainSplit[i] == "&dimensions-region=":
                if mainSplit[i + 1][0] == '-':
                    self.region = [-1]
                else:
                    regionSplit = mainSplit[i + 1].split(',')
                    self.region = [int(regionSplit[0]), int(regionSplit[1]), int(regionSplit[2]), int(regionSplit[3])]
            elif mainSplit[i] == "&uri=":
                self.uri = mainSplit[i + 1]
            elif mainSplit[i] == "&pages=":
                self.pages = int(mainSplit[i + 1])