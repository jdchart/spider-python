import json
import os
import shutil
import spider as sp
import random

def readJson(path):
    with open(path, 'r') as f:
        return json.load(f)
    
def remove_file(path):
    if os.path.isfile(path):
        os.remove(path)

def remove_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)

def remove_web(webFolder):
    if os.path.isdir(os.path.join(os.getcwd(), webFolder)):
        shutil.rmtree(os.path.join(os.getcwd(), webFolder))

def check_attribute(testObj, attr, attributeType, attributeValue):
    testObj.assertIsInstance(attr, attributeType)
    testObj.assertEqual(attr, attributeValue)

def check_direc_file_lists(testObj, prefix, direcList, fileList):
    for item in direcList:
        testObj.assertTrue(os.path.isdir(os.path.join(prefix, item)))
    for item in fileList:
        testObj.assertTrue(os.path.isfile(os.path.join(prefix, item)))

def makeTestFile(path):
    f = open(path, "w")
    f.close()  

def create_basic_web(folderName, title, numNodes):
    web = sp.createWeb({"path" : os.path.join(os.getcwd(), folderName), "title" : title})
    nodeList = []
    for i in range(numNodes):
        nodeList.append(str(web.addNode({"title" : "Node " + str(i)}).uuid))
    for i in range(len(nodeList) - 1):
        web.addEdge({"title" : "Edge " + str(i + 1), "relation" : {"source" : nodeList[i], "target" : nodeList[i + 1]}})
    web.addEdge({"title" : "Edge", "relation" : {"source" : nodeList[3], "target" : nodeList[5]}})

    return web

def create_web_from_media(folderOfMediaFiles, webFolderName):
    mediaFiles = collectFiles(folderOfMediaFiles)
    metadata = {"path" : os.path.join(os.getcwd(), webFolderName)}
    web = sp.createWeb(metadata)
    
    # Create nodes
    nodeList = []
    imgNodes = []
    for item in mediaFiles:
        thisNode = web.mediaToNode(item, True)
        nodeList.append(thisNode.uuid)
        if thisNode.format.type == "image":
            imgNodes.append(thisNode.uuid)

    # Create inters
    for node in nodeList:
        for target in nodeList:
            if node != target:
                web.addEdge({
                    "title" : "test edge",
                    "relation" : {
                        "source" : node,
                        "target" : target
                    }
                })

        # Create non-media nested:
        loaded = web.loadNode(node)
        loaded.addNode({
            "title" : "Nested test"
        })

        # Create non-media nested with dimensions:
        loaded.addNode({
            "title" : "Nested test with dimensions",
            "instructionalMethod" : {
                "annotationPaint" : True,
                "annotationOverlay" : True,
                "annotationDisplayPos" : [10, 10]
            },
            "format" : {
                "fullDimensions" : [50, 50]
            }
        })

        if loaded.format.type == "video":
            # Create non-media nested with dimensions and time:
            loaded.addNode({
                "title" : "Nested test with dimensions and time",
                "instructionalMethod" : {
                    "annotationPaint" : True,
                    "annotationOverlay" : True,
                    "annotationDisplayPos" : [60, 60]
                },
                "format" : {
                    "fullDimensions" : [50, 50]
                },
                "relation" : {
                    "sourceRegions" : [{
                        "start" : 1000,
                        "end" : 5000
                    }]
                }
            })
        
        # Create image nested node 
        if len(imgNodes) > 0:
            loadedRandomImg = web.loadNode(random.choice(imgNodes))
            newNestedImgNode = loaded.duplicateNode(loadedRandomImg, duplicateNested = False)
            newNestedImgNode.title = "Image nested annotation"
            newNestedImgNode.write()

    
    return web

def collectFiles(path):
    acceptedFormats = ["mp4", "png", "jpg", "jpeg", "pdf"]

    finalList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            extension = os.path.splitext(file)[1][1:]
            if extension in acceptedFormats:
                finalList.append(os.path.join(root, file))
    return finalList