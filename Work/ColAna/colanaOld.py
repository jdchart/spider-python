# Collection of elements
import uuid
import utils

class Project:
    def __init__(self, parsingMatrixPath):
        self.parsingMatrix = utils.readJson(parsingMatrixPath)
        self.profiles = []

    def addProfile(self, **kwargs):
        self.profiles.append(Profile(**kwargs))

    def parseCollectiveCategoricalFeature(self, feature):
        returnMatrix = getEmptyMatrix(self.parsingMatrix[feature])

        for profile in self.profiles:
            individualResult = profile.parseCategoricalFeature(feature, self.parsingMatrix)
            for item in individualResult.keys():
                returnMatrix[item] = returnMatrix[item] + individualResult[item]
        
        return returnMatrix

class Profile:
    def __init__(self, **kwargs):
        self.name = kwargs.get("name", "")
        self.uuid = kwargs.get('uuid', str(uuid.uuid4()))

        self.skills = kwargs.get("skills", None)
        self.disciplines = kwargs.get("disciplines", None)

    def parseCategoricalFeature(self, feature, parsingMatrix):
        categoryList = parsingMatrix[feature].keys()
        returnMatrix = getEmptyMatrix(parsingMatrix[feature])

        if getattr(self, feature) != None:
            for item in getattr(self, feature):
                for category in categoryList:
                    associatedTerms = parsingMatrix[feature][category]
                    for term in associatedTerms:
                        if item == term:
                            returnMatrix[category] = returnMatrix[category] + 1

        return returnMatrix
    
    def parseCompositeFeature(self, feature):
        if(feature == "diversity"):
            pass
    
def getEmptyMatrix(parsingMatrix):
    categoryList = parsingMatrix.keys()
    returnMatrix = {}
    for item in categoryList:
        returnMatrix[item] = 0
    return returnMatrix