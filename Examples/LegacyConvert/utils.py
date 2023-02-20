import os
import json

def collectFiles(path):
    acceptedFormats = ["mp4", "png", "jpg", "pdf"]

    finalList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            extension = os.path.splitext(file)[1][1:]
            if extension in acceptedFormats:
                finalList.append(os.path.join(root, file))
    return finalList

def readJson(path):
    with open(path, 'r') as f:
        return json.load(f)

def writeJson(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)