''' ================================================================================
DOCUMENT CATEGORIZATION INTERFACE
================================================================================ '''

from colana import *
import utils
import os

# Provide the document name:
documentName = "Ferrando's Notes"

# Provide paths to Boullier's metrics:
parsingMatrix = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/parsingMatrix.json")
featureIndicatorMatrix = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/featureIndicatorMatrix.json")

# Create a colana project and add a new document to it:
myProject = Project("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/parsingMatrix.json")
myDoc = myProject.addNewDocument(
    name = documentName
)

# A function for parsing typologies to display to the user:
def getTypologyString(entry):
    returnString = ""
    for field in entry:
        for term in entry[field]:
            returnString = returnString + term + "; "
    return returnString

# Iterate through the different cooperation features:
for item in parsingMatrix:
    print("\nFeature: " + item)
    print("\tTypologies: " + getTypologyString(parsingMatrix[item]))
    print("Indicators:")
    for indic in featureIndicatorMatrix[item]:
        print("\t" + indic + ": ")
        for dataSource in featureIndicatorMatrix[item][indic]:
            print("\t- " + dataSource)

    # For each categorical value, ask the user if it applies to the document:
    for field in parsingMatrix[item]:
        for term in parsingMatrix[item][field]:
            inCmd = input(term + "(y) ?")
            if inCmd == 'y':
                # If it applies, ask why:
                expl = input("Please give explination...")
                if getattr(myDoc, item) == None:
                    setattr(myDoc, item, [])
                    getattr(myDoc, item).append({"typology" : term, "explanation" : expl})
                else:
                    getattr(myDoc, item).append({"typology" : term, "explanation" : expl})
    
    # Temporarily save the document after each input
    myDoc.write(os.path.join(os.getcwd(), "temp_out.json"))

# Write the document to file:
myDoc.write(os.path.join("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/DocData", documentName + ".json"))