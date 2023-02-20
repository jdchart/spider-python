''' ================================================================================
03 Edge Convert
================================================================================ '''

import spider as sp
import utils
import os

web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")
oldSpiderWeb = utils.readJson("/Users/jacob/Documents/Git Repos/spider/Test Spiders/COESO-Dancing-Philosophy-annotations-full.json")
nodeMap = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Examples/LegacyConvert/node_map.json")

edgeMap = {}

def oldTimeToMs(oldTime):
    return (oldTime["seconds"] * 1000) + (oldTime["minutes"] * 60000)

for oldEdge in oldSpiderWeb["edges"]:
    print(oldEdge["name"])
    checkPrint = False
    edgeData = {
        "title" : oldEdge["name"],
        "description" : oldEdge["description"],
        "instructionalMethod" : {
            "color" : oldEdge["color"]
        },
        "relation" : {
            "source" : nodeMap[oldEdge["source"]],
            "target" : nodeMap[oldEdge["target"]]
        }
    }

    if "source_time" in oldEdge:
        if "timed" in oldEdge["source_time"]:
            if oldEdge["source_time"]["timed"] == True:
                checkPrint = True
                edgeData["relation"]["sourceRegions"] = [
                    {
                        "start" : oldTimeToMs(oldEdge["source_time"]["start_real"]),
                        "end" : oldTimeToMs(oldEdge["source_time"]["end_real"]),
                        "dims" : [-1]
                    }
                ]
    if "target_time" in oldEdge:
        if "timed" in oldEdge["target_time"]:
            if oldEdge["target_time"]["timed"] == True:
                checkPrint = True
                edgeData["relation"]["targetRegions"] = [
                    {
                        "start" : oldTimeToMs(oldEdge["target_time"]["start_real"]),
                        "end" : oldTimeToMs(oldEdge["target_time"]["end_real"]),
                        "dims" : [-1]
                    }
                ]

    newEdge = web.addEdge(edgeData)

    edgeMap[oldEdge["UUID"]] = str(newEdge.uuid)

utils.writeJson(edgeMap, os.path.join(os.getcwd(), "edge_map.json"))