''' ================================================================================
05 Create Collections
================================================================================ '''

import spider as sp
import utils

web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")
oldSpiderWeb = utils.readJson("/Users/jacob/Documents/Git Repos/spider/Test Spiders/COESO-Dancing-Philosophy-annotations-full.json")
nodeMap = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Examples/LegacyConvert/node_map.json")
edgeMap = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Examples/LegacyConvert/edge_map.json")

nodeColelction = web.addCollection("node", {
    "title" : "Main legacy nodes",
    "description" : "Just the main nodes from the old version."
})
for item in nodeMap:
    nodeColelction.addContent(nodeMap[item])

edgeColelction = web.addCollection("edge", {
    "title" : "Legacy interdocumentary edges",
    "description" : "Just the interdocumentary edges between main nodes from the old version."
})
for item in edgeMap:
    edgeColelction.addContent(edgeMap[item])