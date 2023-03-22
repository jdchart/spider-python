''' ================================================================================
LEGACY CAPSULE CONVERSION
================================================================================ '''
from MRLegacy import MRCapsule
import utils
import spider as sp

# Convert the file to an OOP structure and write to file (see Appendix 4.2)
capsuleFile = "/Users/jacob/Documents/Git Repos/spider-python/Examples/COESO-Semantic-Analysis/DATA/COESO_capsule.php"
capsule = MRCapsule(capsuleFile)
capsule.write("/Users/jacob/Documents/Git Repos/spider-python/Examples/COESO-Semantic-Analysis/OUTPUT/CAPSULE-OUT.json")

# Manually supply the UUID of existing nodes:
mapping = {}
for item in capsule.elements:
    entry = {}
    print()
    print(item.collectData())
    cmdIn = input("Please give uuid:")
    mapping[cmdIn] = item.collectData()
utils.writeJson(mapping, "/Users/jacob/Documents/Git Repos/spider-python/Examples/COESO-Semantic-Analysis/OUTPUT/Capsule-mapping.json")

web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")

# Duplicate existing nodes (creating a new node collection) and remap:
newMap = {}
nodeList = []
for item in mapping:
    loadNode = web.loadNode(item)
    print(loadNode.title)

    duplicatedNode = web.duplicateNode(item)
    nodeList.append(str(duplicatedNode.uuid))
    newMap[str(duplicatedNode.uuid)] = mapping[item]

utils.writeJson(newMap, "/Users/jacob/Documents/Git Repos/spider-python/Work/COESO-Semantic-Analysis/OUTPUT/DUPLICATED-capsule-mapping.json")

originalVid = web.loadNode("7a9b0199-6acc-4db1-82e8-97139b79594d")
duplicatedVid = web.duplicateNode(str(originalVid.uuid))

nodeList.append(str(duplicatedVid.uuid))

newCollection = web.addCollection("node", {"title" : "MemoRekall Legacy Capsule (Duplicated nodes)"})
newCollection.addContent(nodeList)

# Create edges (and create a new edge collection)
mappingData = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Work/COESO-Semantic-Analysis/OUTPUT/DUPLICATED-capsule-mapping.json")
mainVideo = web.loadNode("b212ce06-53f7-4640-8cfb-8fe5213831fe")

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