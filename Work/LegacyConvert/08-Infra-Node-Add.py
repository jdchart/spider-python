''' ================================================================================
07 Infra Node Add
================================================================================ '''

import spider as sp
import utils
import os

web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")
oldSpiderWeb = utils.readJson("/Users/jacob/Documents/Git Repos/spider/Test Spiders/COESO-Dancing-Philosophy-annotations-full.json")
nodeMap = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Examples/LegacyConvert/node_map.json")
print()

def getDataField(key, fieldList):
    for item in fieldList:
        if key == item["key"]:
            return item["value"]

def legacyTimeToMs(legacyTime):
    return (legacyTime["seconds"] * 1000) + (legacyTime["minutes"] * 60000)

for item in oldSpiderWeb["nodes"]:
    if len(item["nodes"]) > 0:
        print("Treating " + item["name"] + " (has " + str(len(item["nodes"])) + " nested nodes).")
        newParentNode = web.loadNode(nodeMap[item["UUID"]])
        print(str(newParentNode.uuid))
        print("Adding nested nodes to " + newParentNode.title + "...")

        for nestedNode in item["nodes"]:
            print("Adding " + nestedNode["name"])
            nodeDims = getDataField("dims", nestedNode["data"]["fields"])

            newNodeData = {
                "title" : nestedNode["name"],
                "description" : nestedNode["description"],
                "instructionalMethod" : {
                    "color" : nestedNode["color"],
                    "annotationPaint" : True,
                    "annotationOverlay" : False,
                    "annotationDisplayPos" : [0, 0],
                    "annotationDisplayScale" : 1
                },
                "format" : {
                    "type" : "image",
                    "fileFormat" : getDataField("type", nestedNode["data"]["fields"]),
                    "fullDimensions" : [nodeDims[2], nodeDims[3]],
                    "region" : [-1],
                    "uri" : os.path.basename(getDataField("link", nestedNode["data"]["fields"]))
                },
                "relation" : {
                    "source" : str(newParentNode.uuid),
                    "sourceRegions" : [{
                        "start" : legacyTimeToMs(nestedNode["time"]["start_real"]),
                        "end" : legacyTimeToMs(nestedNode["time"]["end_real"])
                    }]
                }
            }

            newParentNode.addNode(newNodeData)

        print()