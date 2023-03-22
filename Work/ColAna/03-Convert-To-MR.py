''' ================================================================================
CONVERT TO MR
================================================================================ '''

import spider as sp
import utils

#web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")

'''
# 01 Create duplications of each of the concerned nodes:
documentList = utils.collectFiles("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/DocData")

nodeList = []
mapping = {}
for path in documentList:
    docData = utils.readJson(path)
    print(docData["node_uuid"])
    loadNode = web.loadNode(docData["node_uuid"])
    print(loadNode.title)
    
    duplicatedNode = web.duplicateNode(docData["node_uuid"])
    nodeList.append(str(duplicatedNode.uuid))
    mapping[docData["node_uuid"]] = str(duplicatedNode.uuid)

utils.writeJson(mapping, "/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/ConvertData/mapping.json")

newCollection = web.addCollection("node", {"title" : "Boullier Duplicated Nodes"})
newCollection.addContent(nodeList)

print("Collection: " + str(newCollection.uuid))
'''

'''
compositeNode = web.mediaToNode("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/Images/COMPOSITE.png", True)
compositeNode.title = "Composite collaboration analytics compass"

nodeCollection = web.loadCollection("b3792c3c-d267-45f1-bcc6-59ad7293bdaa")
nodeCollection.addContent(str(compositeNode.uuid))

comp = web.loadNode("c41b0c91-f735-41fa-83f0-d9f836bb9ca1")
comp.title = "Composite collaboration analytics compass"
comp.write()
'''



'''
# Calculate coordinates
imageDims = {
        "width" : 1000,
        "height" : 1000,
        "padding" : 10
    }
imageStyle = {
    "lineWidth" : 4,
    "pointSize" : 8
}

globalTypoData = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/Images/DATA.json")
nodeMapping = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/ConvertData/mapping.json")

documentList = utils.collectFiles("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/DocData")

finalData = {}

for path in documentList:
    entry = {}
    docData = utils.readJson(path)
    originalNode = docData["node_uuid"]

    correspondingNode = nodeMapping[originalNode]
    correspondingData = globalTypoData[docData["name"]]

    entry["correspondingData"] = correspondingData
    entry["name"] = docData["name"]

    x1 = utils.rescale(correspondingData["matrix"]["adaptive"], 0, 1, imageDims["width"] * 0.5, imageDims["padding"])
    y1 = utils.rescale(correspondingData["matrix"]["adaptive"], 0, 1, imageDims["height"] * 0.5, imageDims["padding"])
    x2 = utils.rescale(correspondingData["matrix"]["plan_oriented"], 0, 1, imageDims["width"] * 0.5, imageDims["padding"])
    y2 = utils.rescale(correspondingData["matrix"]["plan_oriented"], 0, 1, imageDims["height"] * 0.5, imageDims["height"] - imageDims["padding"])
    x3 = utils.rescale(correspondingData["matrix"]["institutional"], 0, 1, imageDims["width"] * 0.5, imageDims["width"] - imageDims["padding"])
    y3 = utils.rescale(correspondingData["matrix"]["institutional"], 0, 1, imageDims["height"] * 0.5, imageDims["height"] - imageDims["padding"])
    x4 = imageDims["width"] * 0.5
    y4 = imageDims["height"] * 0.5

    centroid = utils.getCentroid([[x1, y1], [x2, y2], [x3, y3], [x4, y4]])

    entry["shapeDims"] = [x1, y1, x2, y2, x3, y3, x4, y4]
    entry["centroid"] = centroid
    entry["centroidEllipse"] = [centroid[0] - (imageStyle["pointSize"]*0.5), centroid[1]- (imageStyle["pointSize"]*0.5), centroid[0] + (imageStyle["pointSize"]*0.5), centroid[1] + (imageStyle["pointSize"]*0.5)]

    finalData[correspondingNode] = entry

utils.writeJson(finalData, "/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/ConvertData/fullData.json")
'''






'''
# Create edges
# Composite node id: c41b0c91-f735-41fa-83f0-d9f836bb9ca1

fullData = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/ConvertData/fullData.json")
nodeCollection = web.loadCollection("b3792c3c-d267-45f1-bcc6-59ad7293bdaa")

edgeList = []
nodeList = nodeCollection.contentToList()
mainNode = web.loadNode("c41b0c91-f735-41fa-83f0-d9f836bb9ca1")
for item in nodeList:
    loaded = web.loadNode(item)
    if str(loaded.uuid) != "c41b0c91-f735-41fa-83f0-d9f836bb9ca1":
        # Create an edge:
        ellipseDims = fullData[str(loaded.uuid)]["centroidEllipse"]
        print()
        
        edgeData = {
            "title" : loaded.title + " - " + mainNode.title,
            "relation" : {
                "source" : str(mainNode.uuid),
                "target" : str(loaded.uuid),
                "sourceRegions" : [
                    {
                        "start" : -1,
                        "end" : -1,
                        "dims" : [int(ellipseDims[0]), int(ellipseDims[1]), 8, 8]
                    }
                ]
            }
        }

        newEdge = web.addEdge(edgeData)
        edgeList.append(str(newEdge.uuid))

edgeCollection = web.addCollection("edge", {"title" : "Boullier Collection edges"})
edgeCollection.addContent(edgeList)

print("EDGE COLLECTION UUID : " + str(edgeCollection.uuid))
'''


'''
mainNode = web.loadNode("c41b0c91-f735-41fa-83f0-d9f836bb9ca1")
mainNode.instructionalMethod.important = True
mainNode.write()
'''

'''
nodeCollection = web.loadCollection("b3792c3c-d267-45f1-bcc6-59ad7293bdaa")
edgeCollection = web.loadCollection("91e8dcbc-02a6-431a-99aa-af63b236334b")

network = web.convertToNetwork(nodeList = nodeCollection, edgeList = edgeCollection)
network.display()
'''

'''
web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")
nodeCollection = web.loadCollection("b3792c3c-d267-45f1-bcc6-59ad7293bdaa")
edgeCollection = web.loadCollection("91e8dcbc-02a6-431a-99aa-af63b236334b")

edgeList = edgeCollection.contentToList()
for edge in edgeList:
    loaded = web.loadEdge(edge)

    print(loaded.relation)
'''


'''
web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")
nodeCollection = web.loadCollection("b3792c3c-d267-45f1-bcc6-59ad7293bdaa")
edgeCollection = web.loadCollection("91e8dcbc-02a6-431a-99aa-af63b236334b")

nodeList = nodeCollection.contentToList()
for edge in nodeList:
    loaded = web.loadNode(edge)
    if loaded.title == "Organic (Graffione's description)":
        loaded.title = {
            "en" : "Organic (Graffione's description)",
            "fr" : "Organic (Graffione's description)"
        }
    loaded.write()


    print(loaded.relation)
'''




'''
# 1. Define your settings:
settings = {
    # Path to the manifest to convert:
    "webPath" : "/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project", 

    # The real path to the manifests:
    "path" : "http://localhost:9000/data/COESO-Project-Network", 
    #"path" : "https://iiif.tetras-libre.fr/data/demo-content/Jacob/www-COESO-TEST/",

    # The place the MemoRekall network will be written to (None = webPath/mirador):
    "writePath" : "/Users/jacob/Documents/Git Repos/POC-mirador/www/COESO-Project-Network",
    #"writePath" : "/Users/jacob/Documents/Git Repos/demo-content/Jacob/www-COESO-TEST",

    # If a manifest network already exists, remove it before creation [manifests, media]:
    "removePrevious" : [True, True],

    # Copy all node media to the write location (note that this also controls PDF conversion):
    "copyMedia" : True,

    "lang" : "en"
}

# 2. Load the web:
toConvert = sp.loadWeb(settings["webPath"])

# 3. Get collections and check sanity:
nodeCollection = toConvert.loadCollection("b3792c3c-d267-45f1-bcc6-59ad7293bdaa")
edgeCollection = toConvert.loadCollection("91e8dcbc-02a6-431a-99aa-af63b236334b")

# 3. Convert to MemoRekall:
toConvert.convertToMemoRekall(nodeList = nodeCollection, edgeList = edgeCollection, **settings)
'''