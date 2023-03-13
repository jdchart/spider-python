''' ================================================================================
10 Translations
================================================================================ '''

import spider as sp

def processItem(item, fieldsToProcess):
    print("Treating \"" + item.title + "\", proceed? (y/n)")
    userCmd = input()
    if userCmd == "y":
        item.language = ["en", "fr"]
        for field in fieldsToProcess:
            getTranslation(item, field)
    item.write()
    print()

def getTranslation(item, field):
    print("Setting " + field + " (perviously: \"" + str(getattr(item, field)) + "\").")
    original = str(getattr(item, field))
    
    setData = {"en" : "","fr" : ""}
    print("In English:")
    userCmd = input()
    if userCmd == "c":
        setData["en"] = original
    else:
        setData["en"] = userCmd
    
    print("In French:")
    userCmd = input()
    if userCmd == "c":
        setData["fr"] = original
    else:
        setData["fr"] = userCmd

    setattr(item, field, setData)

def processEdgeTitle(web, edge):
    sourceNode = web.loadNode(edge.relation.source)
    targetNode = web.loadNode(edge.relation.target)
    finalTitle = {
        "en" : sourceNode.getFromLang("title", "en") + " -- " + targetNode.getFromLang("title", "en"),
        "fr" : sourceNode.getFromLang("title", "fr") + " -- " + targetNode.getFromLang("title", "fr")
    }
    edge.title = finalTitle
    print("Automatically set title to:")
    print(str(finalTitle["en"]) + " (english).")
    print(str(finalTitle["fr"]) + " (french).")

web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")
#processItem(web, ["provenance", "source", "type"])

'''
nodeList = web.getFullList("nodes")
for item in nodeList:
    myNode = web.loadNode(item)
    print(myNode.format.uri)
    processItem(myNode, ["title", "description"])
'''

edgeList = web.getFullList("edges")
for i in range(len(edgeList)):
    myEdge = web.loadEdge(edgeList[i])
    print(str(i + 1) + "/" + str(len(edgeList)))
    processEdgeTitle(web, myEdge)
    processItem(myEdge, ["description"])