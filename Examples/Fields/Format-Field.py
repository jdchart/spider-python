''' ================================================================================
FORMAT FIELD
The Dublin Core `format` field looks to represent the physical or digital manifestation of the resource
Notably: media-type, dimensions, size, duration etc.
Spider will parse data into a single format entry which can be easily decoded.
You can set the format for any element, but it only really applies to nodes.
================================================================================ '''

import spider as sp
import os
import shutil

# 0. Script settings. 
# Set this to true to remove these test directories once you're done.
cleanUp = False

# 1. Create a web.
testWeb = sp.createWeb({"path" : "/Users/jacob/Documents/Git Repos/Spider Webs/Format test", "title" : "Format test web"})
print("Web format content:")
print(testWeb.format)
print()

# 2. Set format info
formatInfo = {
    "type" : "video",
    "fileFormat" : "mp4",
    "fullDuration" : 10000, # Full duration in ms
    "start" : -1, # The beginning of this item (-1 = the beginning)
    "end" : 5000, # The end of this item (-1 = the end)
    "fullDimensions" : [1080, 720], # Dimensions in px
    "region" : [-1], # The region this item covers. [-1] = the whole media, or [x, y, w, h]
    "uri" : "path/to/my/media",
    "pages" : 1 # For paged media, the number of pages it contains.
}

# 3. Create a node
myNode = testWeb.addNode({
    "title" : "A video",
    "format" : formatInfo
})
print("Node format content:")
print(myNode.format)
print()

# 4. Set attributes:
myNode.format.end = -1
print("Updated node format content:")
print(myNode.format)
print()
myNode.write()

# 5. Check that loading is working:
loadedWeb = sp.loadWeb(testWeb.path)
loadedNode = loadedWeb.loadNode(str(myNode.uuid))
print("Loaded node format content:")
print(loadedNode.format)
print()

# Cleanup
if cleanUp == True:
    if os.path.exists(testWeb.path):
        shutil.rmtree(testWeb.path)