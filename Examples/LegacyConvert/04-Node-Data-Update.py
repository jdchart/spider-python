''' ================================================================================
04 Node data update
================================================================================ '''

import spider as sp
import utils

web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")
oldSpiderWeb = utils.readJson("/Users/jacob/Documents/Git Repos/spider/Test Spiders/COESO-Dancing-Philosophy-annotations-full.json")
nodeMap = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Examples/LegacyConvert/node_map.json")

def getOldNode(webData, nodeUUID):
    for node in webData["nodes"]:
        if node["UUID"] == nodeUUID:
            return node

for item in nodeMap:
    loadedNode = web.loadNode(nodeMap[item])
    oldNode = getOldNode(oldSpiderWeb, item)
    print("Updating " + loadedNode.title + "\n")

    loadedNode.title = oldNode["name"]
    loadedNode.instructionalMethod.color = oldNode["color"]
    if "description" in oldNode:
        loadedNode.description = oldNode["description"]
    
    loadedNode.write()