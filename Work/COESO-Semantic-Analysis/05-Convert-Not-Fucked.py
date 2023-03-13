import spider as sp
import utils

web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")

'''
# Check all nodes load
checkList = web.getFullList("nodes")
for item in checkList:
    loadNode = web.loadNode(item)
    print(loadNode.title)
'''

'''
# Duplcate and remap
mappingData = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Work/COESO-Semantic-Analysis/OUTPUT/Capsule-mapping.json")

newMap = {}
nodeList = []
for item in mappingData:
    loadNode = web.loadNode(item)
    print(loadNode.title)

    duplicatedNode = web.duplicateNode(item)
    nodeList.append(str(duplicatedNode.uuid))
    newMap[str(duplicatedNode.uuid)] = mappingData[item]

utils.writeJson(newMap, "/Users/jacob/Documents/Git Repos/spider-python/Work/COESO-Semantic-Analysis/OUTPUT/DUPLICATED-capsule-mapping.json")

originalVid = web.loadNode("7a9b0199-6acc-4db1-82e8-97139b79594d")
duplicatedVid = web.duplicateNode(str(originalVid.uuid))

nodeList.append(str(duplicatedVid.uuid))

newCollection = web.addCollection("node", {"title" : "MemoRekall Legacy Capsule (Duplicated nodes)"})
newCollection.addContent(nodeList)

print("Vid: " + str(duplicatedVid.uuid))
print("Collection: " + str(newCollection.uuid))
'''

'''
# Create edges
mappingData = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Work/COESO-Semantic-Analysis/OUTPUT/DUPLICATED-capsule-mapping.json")
mainVideo = web.loadNode("b212ce06-53f7-4640-8cfb-8fe5213831fe")
print(mainVideo.title + "\n")

nodeCollection = web.loadCollection("edd3e266-839d-4980-bd5f-c947267a8540")


nodeList = nodeCollection.contentToList()
edgeList = []
for item in nodeList:
    if item != "b212ce06-53f7-4640-8cfb-8fe5213831fe":
        targetNode = web.loadNode(item)
        startTime = int(float(mappingData[item]["timeStart"]) * 1000)
        endTime = int(float(mappingData[item]["timeEnd"]) * 1000)

        edgeData = {
            "title" : targetNode.title + " - " + mainVideo.title,
            "relation" : {
                "source" : str(mainVideo.uuid),
                "target" : str(targetNode.uuid),
                "sourceRegions" : [
                    {"start" : startTime, "end" : endTime}
                ]
            }
        }

        newEdge = web.addEdge(edgeData)
        edgeList.append(str(newEdge.uuid))

edgeCollection = web.addCollection("edge", {"title" : "MemoRekall Legacy Capsule Edges (duplicated)"})
edgeCollection.addContent(edgeList)
print(str(edgeCollection.uuid))
'''

nodeCollection = web.loadCollection("edd3e266-839d-4980-bd5f-c947267a8540")
edgeCollection = web.loadCollection("17dd7dcc-b864-4657-b9df-04773bd1b3b5")

network = web.convertToNetwork(nodeList = nodeCollection, edgeList = edgeCollection)
network.display()