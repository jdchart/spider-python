''' ================================================================================
02 Node Map
================================================================================ '''

import spider as sp
import utils
import os

web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")
oldSpiderWeb = utils.readJson("/Users/jacob/Documents/Git Repos/spider/Test Spiders/COESO-Dancing-Philosophy-annotations-full.json")

newNodeList = web.getFullList("nodes")

nodeMap = {}

for oldNode in oldSpiderWeb["nodes"]:
    print("\nProcessing " + oldNode["name"] + " (" + oldNode["UUID"] + "):")
    
    fileName = None
    for field in oldNode["data"]["fields"]:
        if field["key"] == "link":
            fileName = os.path.basename(field["value"]).replace(" ", "_")
            root, ext = os.path.splitext(fileName)
            if not ext:
                ext = '.pdf'
            fileName = root + ext
    print("Media file name: " + fileName)

    foundMatch = False
    for newNodeUUID in newNodeList:
        thisNode = web.loadNode(newNodeUUID)
        thisFileName = os.path.basename(thisNode.format.uri)
        if thisFileName == fileName:
            print("Found match with \"" + thisNode.title + "\", confirm ?")
            answer = input()
            if answer == "y":
                print("Added to node map.")
                nodeMap[oldNode["UUID"]] = newNodeUUID
                foundMatch = True

    if foundMatch == False:
        print("Please manually supply the UUID of the new node:")
        suppliedUUID = input()
        nodeMap[oldNode["UUID"]] = suppliedUUID
        print("Added manually !")

utils.writeJson(nodeMap, os.path.join(os.getcwd(), "node_map.json"))