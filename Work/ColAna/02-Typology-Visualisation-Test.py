from colana import *
import utils


documentPaths = utils.collectFiles("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/DocData")
parsingMatrixPath = "/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/parsingMatrix.json"

testProject = Project(parsingMatrixPath)
testProject.addDocuments(documentPaths)

testProject.parseProject(
    draw = True,
    outputDir = "/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/Images"
)