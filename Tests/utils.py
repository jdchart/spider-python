import json
import os
import shutil
import spider as sp

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