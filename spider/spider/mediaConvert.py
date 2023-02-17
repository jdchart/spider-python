import os
import cv2
from PyPDF2 import PdfReader

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
            "title" : os.path.splitext(os.path.basename(path))[0],
            "format" : {
                "type" : typeParse[1],
                "fileFormat" : typeParse[0],
                "uri" : path
            },
            "instructionalMethod" : {
                "annotationDisplayScale" : 1,
                "annotationDisplayPos" : [0, 0],
                "annotationOverlay" : False,
                "annotationPaint" : True,
                "important" : False
            }
        }

        if(returnData["format"]["type"] == "video"):
            returnData = parseVideo(returnData)
        elif(returnData["format"]["type"] == "image"):
            returnData = parseImage(returnData)
        elif(returnData["format"]["type"] == "document"):
            returnData = parseDocument(returnData)

        return returnData
    else:
        return None

def getMediaType(path, accpetedFormats):
    ext = os.path.splitext(path)[1][1:]
    for item in accpetedFormats:
        if ext == item["extension"]:
            return [ext, item["type"]]
    return None

def parseVideo(retData):
    openCVvideo = cv2.VideoCapture(retData["format"]["uri"])
    
    frames = openCVvideo.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = openCVvideo.get(cv2.CAP_PROP_FPS)
    duration = int(round(frames / fps) * 1000)
    width = int(openCVvideo.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(openCVvideo.get(cv2.CAP_PROP_FRAME_HEIGHT))

    retData["format"]["fullDuration"] = duration
    retData["format"]["start"] = -1
    retData["format"]["end"] = -1
    retData["format"]["fullDimensions"] = [width, height]
    retData["format"]["region"] = [-1]

    return retData

def parseImage(retData):
    openCVimg = cv2.imread(retData["format"]["uri"], cv2.IMREAD_UNCHANGED)

    retData["format"]["fullDimensions"] = [int(openCVimg.shape[1]), int(openCVimg.shape[0])]
    retData["format"]["region"] = [-1]

    return retData

def parseDocument(retData):
    pdfFile = PdfReader(retData["format"]["uri"])
    maxWid = pdfFile.pages[0].mediabox.width
    maxHeight = pdfFile.pages[0].mediabox.height

    for page in pdfFile.pages:
        if page.mediabox.width > maxWid:
            maxWid = page.mediabox.width
        if page.mediabox.height > maxHeight:
            maxHeight = page.mediabox.height

    retData["format"]["fullDimensions"] = [int(maxWid), int(maxHeight)]
    retData["format"]["region"] = [-1]
    retData["format"]["pages"] = len(pdfFile.pages)

    return retData