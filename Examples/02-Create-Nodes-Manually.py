''' ================================================================================
02 CREATE NODES MANUALLY
Add nodes to a web and serach for existing nodes
================================================================================ '''

import spider as sp
import os
import shutil

# 0. Script settings. 
# Set this to true to remove these test directories once you're done.
cleanUp = False

# 1. Create a new web:
testWeb = sp.createWeb({"path" : "/Users/jacob/Documents/Git Repos/Spider Webs/Test Nodes", "title" : "My test web"})

# 2. Set the node metadata.
# For a full list of fields and defaults, see /Docs/Metadata-fields.md.
nodeMetaData = {
    "title" : "A manually created node.",
    "description" : ""
}

# 3. Add the node to your web:
myNode = testWeb.addNode(nodeMetaData)
print(myNode)

# 4. Load a node using a search key (by default the uuid (recommened))
# Note, the search term must be a string (we need to convert the uuid to a string)
loadedNode = testWeb.loadNode(str(myNode.uuid))
print(loadedNode)

theSameNode = testWeb.loadNode(myNode.title, term = "title")
print(theSameNode)

# 5. You can also add nested nodes to other nodes:
nestedNode = loadedNode.addNode({"title" : "My nested node"})
print(nestedNode)

# You can use the same search function on a node's nested nodes:
loadedNestedNode = loadedNode.loadNode(str(nestedNode.uuid))
print(loadedNestedNode)

# Cleanup
if cleanUp == True:
    if os.path.exists(testWeb.path):
        shutil.rmtree(testWeb.path)