import json
import os
import shutil

def readJson(path):
    with open(path, 'r') as f:
        return json.load(f)
    
def remove_file(path):
    if os.path.isfile(path):
        os.remove(path)

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