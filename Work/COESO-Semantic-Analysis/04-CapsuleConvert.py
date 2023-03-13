''' ================================================================================
03 CAPSULE CONVERT
================================================================================ '''
import utils
import spider as sp

#mappingData = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Examples/COESO-Semantic-Analysis/OUTPUT/Capsule-mapping.json")
mappingData = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Examples/COESO-Semantic-Analysis/OUTPUT/Capsule-mapping-DUPLICATED.json")
#mainVideoUUID = "7a9b0199-6acc-4db1-82e8-97139b79594d"
#mainVideoUUID = "5556487a-604d-44bc-a976-fb6aa44f329f"
webPath = "/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project"


# COLLECTION UUID ===== bfd8cbda-4ff5-46d6-b7a9-52d203bf6115

# Load web
web = sp.loadWeb(webPath)

'''
# Create node collection:
newCollection = web.addCollection("node", {"title" : "MemoRekall Legacy Capsule"})
nodeList = [mainVideoUUID]
for item in mappingData:
    nodeList.append(item)
newCollection.addContent(nodeList)
print(newCollection.uuid)
'''
#nodeCollection = web.loadCollection("36ddd647-1970-4b91-98c1-88915a098786")


nodeCollection = web.loadCollection("bfd8cbda-4ff5-46d6-b7a9-52d203bf6115")
nodeList = nodeCollection.contentToList()
for item in nodeList:
    print(item)
    print(web.loadNode(item).title)


#nodeList = nodeCollection.contentToList()


'''
newMapping = {}

duplicatedList = []
for item in mappingData:
    print("Duplicating... " + web.loadNode(item).title)

    duplicatedNode = web.duplicateNode(item)
    
    duplicatedList.append(str(duplicatedNode.uuid))
    theData = mappingData[item]
    newMapping[str(duplicatedNode.uuid)] = theData

mainDuplicated = web.duplicateNode(mainVideoUUID)
duplicatedList.append(str(mainDuplicated.uuid))

duplicatedCollection = web.addCollection("node", {"title" : "MemoRekall Legacy Capsule (duplicated - final)"})
duplicatedCollection.addContent(duplicatedList)


print(newMapping)
print("COLLECTION UUID: " + str(duplicatedCollection.uuid))
utils.writeJson(newMapping, "/Users/jacob/Documents/Git Repos/spider-python/Examples/COESO-Semantic-Analysis/OUTPUT/Capsule-mapping-DUPLICATED.json")

'''
'''

newMapping = {}

duplicatedList = []
nodeList = nodeCollection.contentToList()
for item in nodeList:
    if item != "7a9b0199-6acc-4db1-82e8-97139b79594d":
        duplicatedNode = web.duplicateNode(item)
        duplicatedList.append(str(duplicatedNode.uuid))

        theData = mappingData[item]
        newMapping[str(duplicatedNode.uuid)] = theData
    else:
        duplicatedNode = web.duplicateNode(item)
        duplicatedList.append(str(duplicatedNode.uuid))
        print("MAIN VID : " + str(duplicatedNode.uuid))


utils.writeJson(newMapping, "/Users/jacob/Documents/Git Repos/spider-python/Examples/COESO-Semantic-Analysis/OUTPUT/Capsule-mapping-DUPLICATED.json")



duplicatedCollection = web.addCollection("node", {"title" : "MemoRekall Legacy Capsule (duplicated)"})
duplicatedCollection.addContent(duplicatedList)
print(duplicatedCollection.uuid)

'''



'''
nodeList = nodeCollection.contentToList()
for item in nodeList:
    thisNode = web.loadNode(item)
    print(thisNode.title)
'''

'''
edgeList = []
for item in mappingData:
    srcNode = web.loadNode(mainVideoUUID)
    targetNode = web.loadNode(item)
    startTime = int(float(mappingData[item]["timeStart"]) * 1000)
    endTime = int(float(mappingData[item]["timeEnd"]) * 1000)

    edgeData = {
        "title" : targetNode.title + " - " + srcNode.title,
        "relation" : {
            "source" : str(srcNode.uuid),
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


'''
edgeCollection = web.loadCollection("55d36fdb-e9ce-4889-adc2-09ad1cd9c402")

network = web.convertToNetwork(nodeList = nodeCollection, edgeList = edgeCollection)
network.display()
'''


