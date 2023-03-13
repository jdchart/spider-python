from colana import *
import utils
import os

documentPaths = [
    "/Users/jacob/Documents/Git Repos/spider-python/Examples/ColAna/OUTPUT/Desire.json",
    "/Users/jacob/Documents/Git Repos/spider-python/Examples/ColAna/OUTPUT/Public Workshop.json"
]

parsingMatrixPath = "/Users/jacob/Documents/Git Repos/spider-python/Examples/ColAna/parsingMatrix.json"

testProject = Project(parsingMatrixPath)

testProject.addDocuments(documentPaths)

for doc in testProject.documents:
    print("\n" + doc.name + ":")
    
    fieldList = doc.parseFields()
    
    print("Loss: " + str(getFieldListLoss(fieldList)))

    doc.parseDocument()

    '''
    for item in fieldList:
        print("\t" + item["feature"] + ": " + str(item["matrix"]))
    '''