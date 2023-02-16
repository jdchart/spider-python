import os

def getMediaData(path):
    accepted = [
        {"extension" : "mp4", "type" : "video"},
        {"extension" : "png", "type" : "image"},
        {"extension" : "jpg", "type" : "image"},
        {"extension" : "pdf", "type" : "document"}
    ]

    typeParse = getMediaType(path, accepted)
    if typeParse != None:
        returnData = {
            "path" : path,
            "extension" : typeParse[0],
            "type" : typeParse[1],
            "name" : os.path.splitext(os.path.basename(path))[0]
        }
        return returnData
    else:
        return None

def getMediaType(path, accpetedFormats):
    ext = os.path.splitext(path)[1][1:]
    for item in accpetedFormats:
        if ext == item["extension"]:
            return [ext, item["type"]]
    return None