import json
import os
from shapely.geometry import Polygon

def writeJson(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def readJson(path):
    with open(path, 'r') as f:
        return json.load(f)
    
def rescale(val, oldMin, oldMax, a, b):
    return a + (((val - oldMin) * (b - a)) / (oldMax - oldMin))

def getCentroid(pointList):
    P = Polygon(pointList)
    cent = P.centroid.coords
    return [cent[0][0], cent[0][1]]

def collectFiles(path, acceptedFormats):

    finalList = []
    for root, dirs, files in os.walk(path):
        for file in files:
            extension = os.path.splitext(file)[1][1:]
            if extension in acceptedFormats:
                finalList.append(os.path.join(root, file))
    return finalList