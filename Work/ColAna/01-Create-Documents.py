from colana import *
import utils
import os

documentName = ""
nodeUUID = ""

parsingMatrixPath = "/Users/jacob/Documents/Git Repos/spider-python/Examples/ColAna/parsingMatrix.json"
featureIndicatorMatrixPath = "/Users/jacob/Documents/Git Repos/spider-python/Examples/ColAna/featureIndicatorMatrix.json"

testProject = Project(parsingMatrixPath)

myDoc = testProject.addNewDocument(
    name = documentName,
    node_uuid = nodeUUID
)

def getTypologyString(entry):
    returnString = ""
    for field in entry:
        for term in entry[field]:
            returnString = returnString + term + "; "
    return returnString

parsingMatrix = utils.readJson(parsingMatrixPath)
featureIndicatorMatrix = utils.readJson(featureIndicatorMatrixPath)

for item in parsingMatrix:
    print("\nFeature: " + item)


    print("\tTypologies: " + getTypologyString(parsingMatrix[item]))
    print("Indicators:")
    for indic in featureIndicatorMatrix[item]:
        print("\t" + indic + ": ")
        for dataSource in featureIndicatorMatrix[item][indic]:
            print("\t- " + dataSource)

    for field in parsingMatrix[item]:
        for term in parsingMatrix[item][field]:
            inCmd = input(term + "(y) ?")
            if inCmd == 'y':
                expl = input("Please give explination...")
                if getattr(myDoc, item) == None:
                    setattr(myDoc, item, [])
                    getattr(myDoc, item).append({"typology" : term, "explanation" : expl})
                else:
                    getattr(myDoc, item).append({"typology" : term, "explanation" : expl})
    
    myDoc.write(os.path.join(os.getcwd(), "temp_out.json"))

myDoc.write(os.path.join("/Users/jacob/Documents/Git Repos/spider-python/Examples/ColAna/OUTPUT", documentName + ".json"))