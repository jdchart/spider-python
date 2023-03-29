''' ================================================================================
IIIF - 02 - Video to Manifest
Take a video and convert it to a IIIF Manifest file.
The source video and the produced manifest will need to be placed at the root
of the address set as the prefix.
================================================================================ '''
import spider as sp
import os

# 1: Set the prefix for data on the server:
prefix = "http://localhost:9000/data/"

# 2: Set the source video and collect data:
videoFile = "/Users/jacob/Documents/Git Repos/spider-python/Examples/Example-Media/exampleVideo.mp4"

rawVideoData = sp.getMediaData(videoFile)
parsedVideoData = {
    "uri" : os.path.join(prefix, os.path.basename(videoFile)),
    "fileformat" : rawVideoData["format"]["fileFormat"],
    "width" : rawVideoData["format"]["fullDimensions"][0],
    "height" : rawVideoData["format"]["fullDimensions"][1],
    "duration" : rawVideoData["format"]["fullDuration"] / 1000
}

# 3: Create the manifest
manifest = sp.Manifest(
    writepath = "/Users/jacob/Documents/Git Repos/spider-python/Examples/IIIF/Output",
    filename = "Video_Manifest.json",
    path = prefix,
    label = {"en" : ["A Video"], "fr" : ["Une Vidéo"]}
)

# 4: Create canvas
canvas = manifest.addCanvas(width = parsedVideoData["width"], height = parsedVideoData["height"], duration = parsedVideoData["duration"])

# 5: Create media item
canvas.addAnnotationPage().addMediaItem(mediaInfo = sp.parseVideoDataToMediaInfo(parsedVideoData))

# Save the manifest
manifest.write()