import utils
import os

imageFolder = "/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/Images"
fullData = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/ConvertData/fullData.json")

lowerfiles = utils.collectFiles("/Users/jacob/Desktop/Collaboration-Analytics/lower", "json")

emptyAnnot = {
    "id": "http://localhost:9000/data/COESO-Project-Network/lower/canvas/1/annotation/1/1",
    "type": "Annotation",
    "motivation": "commenting",
    "target": "http://localhost:9000/data/COESO-Project-Network/lower/canvas/1",
    "body": {
        "id": "",
        "type": "Image",
        "format": "image/png",
        "width": 1000,
        "height": 1000,
        "value": "Document collaboration analytics compass"
    }
}

for item in lowerfiles:
    nodeUUID = os.path.basename(os.path.splitext(item)[0])

    associatedData = fullData[nodeUUID]
    associatedImage = associatedData["name"] + ".png"

    manifestData = utils.readJson(item)

    mainDims = [
        manifestData["items"][0]["items"][0]["items"][0]["body"]["width"],
        manifestData["items"][0]["items"][0]["items"][0]["body"]["height"]
    ]

    emptyAnnot["body"]["id"] = os.path.join("http://localhost:9000/data/COESO-Project-Network/media", associatedImage).replace(" ", "_")
    emptyAnnot["target"] = "http://localhost:9000/data/COESO-Project-Network/lower/canvas/1" + "#xywh=0," + str(mainDims[1]) + ",1000,1000"
    if manifestData["items"][0]["items"][0]["items"][0]["body"]["type"] == "Video":
        emptyAnnot["target"] = emptyAnnot["target"] + "&t=0," + str(manifestData["items"][0]["items"][0]["items"][0]["body"]["duration"])

    manifestData["items"][0]["annotations"][0]["items"].append(emptyAnnot)
    manifestData["items"][0]["height"] = manifestData["items"][0]["height"] + mainDims[1]

    print(emptyAnnot)

    utils.writeJson(manifestData, os.path.join("/Users/jacob/Desktop/NEwers", nodeUUID + ".json"))