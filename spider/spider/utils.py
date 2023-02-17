import os
import json
import re
from pdf2image import convert_from_path
from pathlib import Path

def makeDirsRecustive(pathList):
    for item in pathList:
        if os.path.isdir(item) == False:
            path = Path(item)
            path.mkdir(parents=True)

def writeJson(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def readJson(path):
    with open(path, 'r') as f:
        return json.load(f)

def findElement(path, searchTerm, searchKey, type):
    '''
    Given a path, search recusively for an element and return the file path
    '''
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if searchKey == "uuid":
                if dir == searchTerm:
                    return os.path.join(root, dir + "/" + type + ".json")
            else:
                queryPath = os.path.join(root, dir + "/" + type + ".json")
                if os.path.isfile(queryPath):
                    toQuery = readJson(queryPath)
                    if toQuery[searchKey] == searchTerm:
                        return queryPath

def stringKeySplit(keyList, stringIn):
    expression = ""
    for i in range(len(keyList)):
        expression = expression + '(' + keyList[i] + ")"
        if i != len(keyList) - 1:
            expression = expression + "|"
    stringSplit = re.split(expression, stringIn)
    finalSplit = []
    for item in stringSplit:
        if isinstance(item, str):
            finalSplit.append(item)
    return finalSplit

def makeGitignoreFile(path, content):
    f = open(path, "w")
    for item in content:
        f.write(item + "\n")
    f.close()

def convertPDF(pathIn, pathOut, numPages, createFile):
    if createFile:
        images = convert_from_path(pathIn)
    filename = os.path.splitext(os.path.basename(pathIn))[0]
    fileList = []
    for i in range(numPages):
        if createFile:
            images[i].save(os.path.join(pathOut, filename + "_page_" + str(i + 1) +'.jpg'), 'JPEG')
        fileList.append(filename + "_page_" + str(i + 1) +'.jpg')
    return fileList