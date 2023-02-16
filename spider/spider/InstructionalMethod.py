from .utils import *

class InstructionalMethod:
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', None)
        self.important = kwargs.get('important', None)
        self.annotationPaint = kwargs.get('annotationPaint', None)
        self.annotationOverlay = kwargs.get('annotationOverlay', None)
        self.annotationDisplayPos = kwargs.get('annotationDisplayPos', None)
        self.annotationDisplayScale = kwargs.get('annotationDisplayScale', None)

        if kwargs.get('from_string', None) != None:
            self.fromString(kwargs.get('from_string'))

    def __str__(self):
        return str(self.collectData())

    def collectData(self):
        return {
            "color" : self.color,
            "important" : self.important,
            "annotationPaint" : self.annotationPaint,
            "annotationOverlay" : self.annotationOverlay,
            "annotationDisplayPos" : self.annotationDisplayPos,
            "annotationDisplayScale" : self.annotationDisplayScale
        }

    def toString(self):
        returnString = ""
        if self.color != None:
            returnString = returnString + "&color=" + self.color
        if self.important != None:
            returnString = returnString + "&important=" + str(self.important)
        if self.annotationPaint != None:
            returnString = returnString + "&annotationPaint=" + str(self.annotationPaint)
        if self.annotationOverlay != None:
            returnString = returnString + "&annotationOverlay=" + str(self.annotationOverlay)
        if self.annotationDisplayPos != None:
            returnString = returnString + "&annotationDisplayPos=" + str(self.annotationDisplayPos[0]) + "," + str(self.annotationDisplayPos[1])
        if self.annotationDisplayScale != None:
            returnString = returnString + "&annotationDisplayScale=" + str(self.annotationDisplayScale)
        return returnString

    def fromString(self, stringIn):
        mainSplit = stringKeySplit(
            ["&color=", "&important=", "&annotationPaint=", "&annotationOverlay=", "&annotationDisplayPos=", "&annotationDisplayScale="], 
            stringIn
        )
        for i in range(len(mainSplit)):
            if mainSplit[i] == "&color=":
                self.color = mainSplit[i + 1]
            if mainSplit[i] == "&important=":
                if mainSplit[i + 1] == "True":
                    self.important = True
                elif mainSplit[i + 1] == "False":
                    self.important = False
            if mainSplit[i] == "&annotationPaint=":
                if mainSplit[i + 1] == "True":
                    self.annotationPaint = True
                elif mainSplit[i + 1] == "False":
                    self.annotationPaint = False
            if mainSplit[i] == "&annotationOverlay=":
                if mainSplit[i + 1] == "True":
                    self.annotationOverlay = True
                elif mainSplit[i + 1] == "False":
                    self.annotationOverlay = False
            if mainSplit[i] == "&annotationDisplayPos=":
                posSplit = mainSplit[i + 1].split(",")
                self.annotationDisplayPos = [int(posSplit[0]), int(posSplit[1])]
            if mainSplit[i] == "&annotationDisplayScale=":
                self.color = float(mainSplit[i + 1])