'''
SEARCH FOLDERS OF MANIFESTS, CHECK IF MAIN ITEM IS THE SAME SIZE OF CANVAS, IF NOT, CREATE NEW RESIZED ITEM AND LINK TO IT.
'''
from moviepy.editor import *
import utils

folderToChange = "/Users/jacob/Documents/Git Repos/POC-mirador/www/COESO-Project-Network"
mediaFolder = os.path.join(folderToChange, "media")
suffix = "_RESIZE_compass"

def absoluteFilePaths(directory):
    fileList = []
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            fileList.append(os.path.abspath(os.path.join(dirpath, f)))
    return fileList

def isEven(num):
    if num % 2 == 0:
        return True
    else:
        return False

lis = absoluteFilePaths(folderToChange)

def resizeVideo(inPath, outPath, newSize):
    videoClip = VideoFileClip(inPath)
    originalSize = videoClip.size

    toAddRight = newSize[0] - originalSize[0]
    toAddBottom = newSize[1] - originalSize[1]

    # Borders msut be even for some reason...
    clip_with_borders = videoClip.margin(top=0, bottom=toAddBottom, left=0, right=toAddRight, color=(255, 255, 255)) 

    clip_with_borders.write_videofile(outPath)

for item in lis:
    ext = os.path.splitext(item)[1].replace(".","")

    if ext == "json":
        manifestData = utils.readJson(item)
        mainItem = manifestData["items"][0]["items"][0]["items"][0]
        canvasSize = [manifestData["items"][0]["width"], manifestData["items"][0]["height"]]
        mainItemSize = [mainItem["body"]["width"], mainItem["body"]["height"]]

        if canvasSize[0] > mainItemSize[0] or canvasSize[1] > mainItemSize[1]:
            print("\nResizing..." + mainItem["body"]["id"] + "...")

            if isEven(canvasSize[0]) == False:
                canvasSize[0] = canvasSize[0] + 1
            if isEven(canvasSize[1]) == False:
                canvasSize[1] = canvasSize[1] + 1


            filename = os.path.basename(mainItem["body"]["id"])
            originalPath = os.path.join(mediaFolder, filename)
            filenameSplit = os.path.splitext(filename)
            resizePath = os.path.join(mediaFolder, filenameSplit[0] + suffix + filenameSplit[1])

            if mainItem["body"]["type"] == "Video":
                resizeVideo(originalPath, resizePath, canvasSize)


                mediaDirec = os.path.dirname(manifestData["items"][0]["items"][0]["items"][0]["body"]["id"])
                pathToAdd = os.path.join(mediaDirec, filenameSplit[0] + suffix + filenameSplit[1])
                print(pathToAdd)  

                manifestData["items"][0]["items"][0]["items"][0]["body"]["id"] = pathToAdd
                
                thisTarget = manifestData["items"][0]["items"][0]["items"][0]["target"]
                targetSplit = thisTarget.split("#xywh=")

                timeSplit = targetSplit[1].split("&t=")
                finalTarget = targetSplit[0] + "#xywh=0,0," + str(canvasSize[0]) + "," + str(canvasSize[1])

                if len(timeSplit) > 1:
                    finalTarget = finalTarget + "&t=" + timeSplit[1]

                manifestData["items"][0]["items"][0]["items"][0]["target"] = finalTarget
                manifestData["items"][0]["items"][0]["items"][0]["body"]["width"] = canvasSize[0]
                manifestData["items"][0]["items"][0]["items"][0]["body"]["height"] = canvasSize[1]



        utils.writeJson(manifestData, item)