''' ================================================================================
11 Atomatic Edges
================================================================================ '''

import spider as sp

createTags = True

web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")

terms = ["Graffione", "Ferrando", "centre", "sober", "truth", "organic", "intentions"]

edgeList = []
count = 0
alreadyMade = []

nodeList = web.getFullList("nodes")
for i in range(len(nodeList)):
    myNode = web.loadNode(nodeList[i])
    for item in terms:
        if item in myNode.title or item in myNode.description:
            for j in range(len(nodeList)):
                if j != i:
                    queriedNode = web.loadNode(nodeList[j])
                    for queriedItem in terms:
                        if queriedItem in queriedNode.title or queriedItem in queriedNode.description:
                            # Create
                            edgeData = {
                                "title" : {
                                    "en" : myNode.getFromLang("title", "en") + " -- " + queriedNode.getFromLang("title", "en"),
                                    "fr" : myNode.getFromLang("title", "fr") + " -- " + queriedNode.getFromLang("title", "fr")
                                },
                                "description" : {
                                    "en" : "Created automatically: \"" + item + "\" found in " + myNode.getFromLang("title", "en") + " and \"" + queriedItem + "\" found in " + queriedNode.getFromLang("title", "en") + '.',
                                    "fr" : "Crée automatiquement: \"" + item + "\" trouvé dans " + myNode.getFromLang("title", "fr") + " et \"" + queriedItem + "\" trouvé dans " + queriedNode.getFromLang("title", "fr") + '.'
                                },
                                "relation" : {
                                    "source" : str(myNode.uuid),
                                    "target" : str(queriedNode.uuid)
                                }
                            }
                            if str(myNode.uuid) + str(queriedNode.uuid) not in alreadyMade:
                                if str(queriedNode.uuid) + str(myNode.uuid) not in alreadyMade:
                                    print(edgeData)

                                    createdEdge = web.addEdge(edgeData)
                                    edgeList.append(str(createdEdge.uuid))
                                    alreadyMade.append(str(myNode.uuid) + str(queriedNode.uuid))
                                    count = count + 1

print()
print("Found " + str(count) + " edges.")

edgeColl = web.addCollection("edge", {"title" : "Automatic edge creation"})
edgeColl.addContent(edgeList)
print(str(edgeColl.uuid))