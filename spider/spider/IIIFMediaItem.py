from .IIIFItem import *
from .IIIFMediaItemBody import *

class MediaItem(IIIFItem):
    def __init__(self, **kwargs):
        super().__init__(id = kwargs.get("id", ""), type = "Annotation")
        self.motivation = kwargs.get("motivation", "painting")
        
        self.targetID = kwargs.get('targetID', "")
        self.target = ""
        self.body = MediaItemBody()

        self.parseMediaInfo(kwargs.get("mediaInfo", {}))

    def parseMediaInfo(self, info):
        for item in info:
            setattr(self.body, item, info[item])
        
        self.target = self.targetID
        hadDims = False
        if "targetDims" in info:
            self.target = self.target + "#xywh="
            self.target = self.target + str(info["targetDims"][0]) + ","
            self.target = self.target + str(info["targetDims"][1]) + ","
            self.target = self.target + str(info["targetDims"][2]) + ","
            self.target = self.target + str(info["targetDims"][3])
            hadDims = True
        if 'targetStart' in info:
            if hadDims == True:
                self.target = self.target + "&t="
            else:
                self.target = self.target + "#t="
            self.target = self.target + str(info["targetStart"]) + ","
            self.target = self.target + str(info["targetEnd"])
        
    def collectData(self):
        collectedSuper = super().collectData()
        collectedSuper["motivation"] = self.motivation
        collectedSuper["target"] = self.target
        collectedSuper["body"] = self.body.collectData()

        return collectedSuper