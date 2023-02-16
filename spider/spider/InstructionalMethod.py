from .utils import *

class InstructionalMethod:
    def __init__(self, **kwargs):
        self.color = kwargs.get('color', None)
        self.important = kwargs.get('important', None)

        if kwargs.get('from_string', None) != None:
            self.fromString(kwargs.get('from_string'))

    def __str__(self):
        return str(self.collectData())

    def collectData(self):
        return {
            "color" : self.color,
            "important" : self.important
        }

    def toString(self):
        returnString = ""
        if self.color != None:
            returnString = returnString + "&color=" + self.color
        if self.important != None:
            returnString = returnString + "&important=" + str(self.important)
        return returnString

    def fromString(self, stringIn):
        mainSplit = stringKeySplit(
            ["&color=", "&important="], 
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