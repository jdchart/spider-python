from colana import *
import utils
import os

documentPaths = utils.collectFiles("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/DocData")


parsingMatrixPath = "/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/parsingMatrix.json"

testProject = Project(parsingMatrixPath)

testProject.addDocuments(documentPaths)

for doc in testProject.documents:
    print("\n" + doc.name + ":")
    
    fieldList = doc.parseFields()
    
    print("Loss: " + str(getFieldListLoss(fieldList)))

    doc.parseDocument(saveFile = os.path.join("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/Images", doc.name + ".png"))