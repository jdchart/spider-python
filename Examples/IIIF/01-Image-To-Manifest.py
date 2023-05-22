''' ================================================================================
IIIF - 01 - Image to Manifest
Take an image and convert it to a IIIF Manifest file.
The source image and the produced manifest will need to be placed at the root
of the address set as the prefix.
================================================================================ '''
import spider as sp
import os

# 1: Set the prefix for data on the server:
prefix = "http://localhost:9000/data/"

# 2: Set the source image and collect data:
imageFile = "/Users/jacob/Documents/Git Repos/spider-python/Examples/Example-Media/exampleImage.jpeg"

mediaFileObject = sp.MediaFile(imageFile)
rawImageData = mediaFileObject.parseToSpiderNode()


parsedImageData = {
    "uri" : os.path.join(prefix, os.path.basename(imageFile)),
    "fileformat" : rawImageData["format"]["fileFormat"],
    "width" : rawImageData["format"]["fullDimensions"][0],
    "height" : rawImageData["format"]["fullDimensions"][1]
}

# 3: Create the manifest
manifest = sp.Manifest(
    writepath = "/Users/jacob/Documents/Git Repos/spider-python/Examples/IIIF/Output",
    filename = "Image_Manifest.json",
    path = prefix,
    label = {"en" : ["An Image"], "fr" : ["Une Image"]}
)

# 4: Create canvas
canvas = manifest.addCanvas(width = parsedImageData["width"], height = parsedImageData["height"])

# 5: Create media item
canvas.addAnnotationPage().addMediaItem(mediaInfo = sp.parseImageDataToMediaInfo(parsedImageData))

# Save the manifest
manifest.write()