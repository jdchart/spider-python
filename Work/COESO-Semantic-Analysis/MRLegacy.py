from xml.dom import minidom
import utils

class MRCapsule:
    def __init__(self, capsulePath):
        self.capsuleFile = minidom.parse(capsulePath)
        self.keyList = self.getKeyList(self.capsuleFile)
        self.elements = self.populateElements()

        self.capsulemeta = {
            "xmlfile" : capsulePath
        }

        self.acceptedMeta = {
            "Title" : "title",
            "Author" : "author",
            "Email" : "email",
            "comments" : "comments"
        }

        self.updateMeta()
        self.orderElements()

    def orderElements(self):
        newlist = sorted(self.elements, key=lambda d: d.timeStart) 
        self.elements = newlist

    def getKeyList(self, domFile):
        fullList = []
        for proj in domFile.getElementsByTagName('project'):
            for child in proj.childNodes:
                if child.attributes != None:
                    if doesAttrExist(child, "key"):
                        thisKey = child.attributes['key'].value
                        if thisKey not in fullList:
                            fullList.append(thisKey)
                    if child.tagName == "document":
                        for docChild in child.childNodes:
                            if docChild.attributes != None:
                                if doesAttrExist(docChild, "ctg"):
                                    if docChild.attributes['ctg'].value == "key":
                                        thisKey = docChild.attributes['cnt'].value
                                        if thisKey not in fullList:
                                            fullList.append(thisKey)
        return fullList
    
    def updateMeta(self):
        for tag in self.capsuleFile.getElementsByTagName('projectMeta'):
            attrList = tag.attributes.items()
            if doesAttrExist(tag, "ctg"):
                if attrList[0][0] == 'ctg':
                    if tag.attributes["ctg"].value in self.acceptedMeta.keys():
                        self.capsulemeta[self.acceptedMeta[tag.attributes["ctg"].value]] = tag.attributes["cnt"].value
        for tag in self.capsuleFile.getElementsByTagName('video'):
            self.capsulemeta["videourl"] = tag.attributes['url'].value
    
    def write(self, path):
        writeData = {
            "capsuleMeta" : self.capsulemeta
        }
        elementList = []
        for element in self.elements:
            elementList.append(element.collectData())
       
        writeData["elements"] = elementList

        utils.writeJson(writeData, path)
    
    def populateElements(self):
        finalList = []
        for thisKey in self.keyList:
            newElement = MRElement(key = thisKey)
            finalList.append(newElement)
            newElement.updateElement(self.capsuleFile)
        return finalList

class MRElement:
    def __init__(self, **kwargs):
        self.key = kwargs.get("key", "")
        self.timeStart = None
        self.timeEnd = None
        self.name = None
        self.comments = None
        self.labels = None
        self.type = None
        self.author = None
        self.datatime = None
        self.importdate = None
        self.username = None
        self.locationname = None
        self.locationgps = None
        self.keywords = None
        self.visibility = None
        self.flag = None
        self.group = None
        self.highlight = None
        self.link = None

        self.file_extension = None
        self.file_basename = None
        self.file_name = None
        self.file_type = None
        self.file_mimetype = None
        self.file_owner = None
        self.file_thumbnail = None

        self.acceptedAttributes = ["timeStart", "timeEnd"]
        self.metadataKeyMap = {
            "Rekall->Name" : "name",
            "Rekall->Comments" : "comments",
            "Rekall->Labels" : "labels",
            "Rekall->Type" : "type",
            "Rekall->Author" : "author",
            "Rekall->Date/Time" : "datatime",
            "Rekall->Import Date" : "importdate",
            #"Rekall->User Name" : "username",
            #"Rekall->Location Name" : "locationname",
            #"Rekall->Location GPS" : "locationgps",
            "Rekall->Keywords" : "keywords",
            "Rekall->Visibility" : "visibility",
            "Rekall->Flag" : "flag",
            "Rekall->Group" : "group",
            "Rekall->Highlight" : "highlight",
            "Rekall->Link" : "link",

            "File->Extension" : "file_extension",
            "File->Basename" : "file_basename",
            "File->File Name" : "file_name",
            "File->File Type" : "file_type",
            "File->MIME Type" : "file_mimetype",
            "File->Owner" : "file_owner",
            "File->Thumbnail" : "file_thumbnail" 
        }

    def collectData(self):
        toReturn = {
            "key" : self.key
        }
        for item in self.acceptedAttributes:
            if getattr(self, item) != None:
                toReturn[item] = getattr(self, item)
        for item in self.metadataKeyMap:
            if getattr(self, self.metadataKeyMap[item]) != None:
                toReturn[self.metadataKeyMap[item]] = getattr(self, self.metadataKeyMap[item])

        return toReturn

    def updateElement(self, domFile):
        #print("\nUpdating " + self.key)
        
        for proj in domFile.getElementsByTagName('project'):
            for child in proj.childNodes:
                if child.attributes != None:
                    if doesAttrExist(child, "key"):
                        thisKey = child.attributes['key'].value
                        if thisKey == self.key:
                            self.parseAttributes(child)
                        
                    if child.tagName == "document":
                        isMatch = False
                        for docChild in child.childNodes:
                            if docChild.attributes != None:
                                if doesAttrExist(docChild, "ctg"):
                                    if docChild.attributes['ctg'].value == "key":
                                        thisKey = docChild.attributes['cnt'].value
                                        if thisKey == self.key:
                                            isMatch = True
                        if doesAttrExist(child, "key"):
                            if child.attributes['key'].value == self.key:
                                isMatch = True

                        if isMatch == True:
                            for docChild in child.childNodes:
                                if docChild.attributes != None:
                                    if doesAttrExist(docChild, "ctg"):
                                        if docChild.attributes['ctg'].value != "key":
                                            self.parseAttributes(docChild)
    
    def parseAttributes(self, node):
        attrList = node.attributes.items()
        if attrList[0][0] == 'ctg':
            if node.attributes["ctg"].value in self.metadataKeyMap.keys():
                setattr(self, self.metadataKeyMap[node.attributes["ctg"].value], node.attributes["cnt"].value)
        else:
            for item in attrList:
                if item[0] in self.acceptedAttributes:
                    setattr(self, item[0], item[1])
                if item[0] == "metadataKey":
                    if item[1] in self.metadataKeyMap.keys():
                        val = node.attributes["metadataValue"].value
                        setattr(self, self.metadataKeyMap[item[1]], val)

def doesAttrExist(node, attrName):
    attrList = node.attributes.items()
    for item in attrList:
        if item[0] == attrName:
            return True
    return False