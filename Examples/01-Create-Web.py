''' ================================================================================
01 CREATE WEB
Create a new spider web.
================================================================================ '''

import spider as sp
import os
import shutil

# 0. Script settings. 
# Set this to true to remove these test directories once you're done.
cleanUp = False

# 1. Set metadata (set the fields you want to set, the rest will be set to default).
# For a full list of fields and defaults, see /Docs/Metadata-fields.md.
# Note: path and identifier are interchangeable
metadata = {
    "path" : "/Users/jacob/Documents/Git Repos/Spider Webs/Test",
    "title" : "A test",
    "creator" : "Shelob"
}

# 2. Create the web.
myWeb = sp.createWeb(metadata)
print("The created web:")
print(myWeb)
print()

# 3. Load a web from file by giving the path to the web's folder.
loadedWeb = sp.loadWeb(myWeb.path)
print("The loaded web:")
print(loadedWeb)
print()

# Cleanup
if cleanUp == True:
    if os.path.exists(myWeb.path):
        shutil.rmtree(myWeb.path)