''' ================================================================================
04 CONVERT MEDIA TO NODES
You can automatically populate a web with nodes that are converted from media files.
================================================================================ '''

import spider as sp
import os
import shutil
import utils

# 0. Script settings. 
# Set this to true to remove these test directories once you're done.
cleanUp = True

# 1. Create a web:
web = sp.createWeb({"path" : "/Users/jacob/Documents/Git Repos/Spider Webs/Media Web", "title" : "My Media Web"})

# 2. Get a list of media file paths you wish to convert:
fileList = utils.collectFiles("/Users/jacob/Documents/Git Repos/Spider Webs/testMedia")

# 3. Convert files with the mediaToNode() function:
for item in fileList:
    web.mediaToNode(item)

# 4. View the created nodes:
web.printContent("nodes", ["title", "format"])

# Cleanup
if cleanUp == True:
    if os.path.exists(web.path):
        shutil.rmtree(web.path)