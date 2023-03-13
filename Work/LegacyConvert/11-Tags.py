''' ================================================================================
11 Tags
================================================================================ '''

import spider as sp

createTags = True

web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")
globalTagList = []

def gatherTags(node):
    print("Enter tags (d = done)")
    finished = False
    tagList = []
    while finished == False:
        thisTage = input()
        if thisTage == "d":
            finished = True
        else:
            tagList.append(thisTage)
    node.tags = {
        "en" : tagList
    }

    node.write()

def addToGlobal(node):
    for item in node.tags:
        if item not in globalTagList:
            globalTagList.append(item)

nodeList = web.getFullList("nodes")
for item in nodeList:
    myNode = web.loadNode(item)
    if createTags:
        print(myNode.title)
        print(myNode.description)
        print("Proceed ? (y/n)")
        toProceed = input()
        if toProceed == "y":
            gatherTags(myNode)
    addToGlobal(myNode)
    print()

translationMap = {}
for item in globalTagList:
    print("Please translate: " + item)
    trans = input()
    translationMap[item] = trans

print()
print(translationMap)
print()

for item in nodeList:
    myNode = web.loadNode(item)

    listToAdd = []
    originalTags = myNode.tags
    for item in originalTags:
        listToAdd.append(translationMap[item])

    finalThing = {
        "en" : originalTags,
        "fr" : listToAdd
    }

    myNode.tags = finalThing

    myNode.write()