''' ================================================================================
03 CREATE EDGES MANUALLY
Add edges to a web and search for existing edges.
================================================================================ '''

import spider as sp
import os
import shutil

# 0. Script settings. 
# Set this to true to remove these test directories once you're done.
cleanUp = False

# 1. Create a new web and some nodes:
testWeb = sp.createWeb({"path" : "/Users/jacob/Documents/Git Repos/Spider Webs/Test Edges", "title" : "My test web"})
for i in range(2):
    testWeb.addNode({"title" : "Node " + str(i + 1)})

# 2. Create an edge between two nodes.
# First, lets take two nodes as a  source and a target:
sourceNode = testWeb.loadNode("Node 1", term = "title")
targetNode = testWeb.loadNode("Node 2", term = "title")

# Set the edge metadata.
# For a full list of fields and defaults, see /Docs/Metadata-fields.md.
edgeData = {
    "title" : "My first edge",
    "relation" : {
        "source" : str(sourceNode.uuid),
        "target" : str(targetNode.uuid)
    }
}

# And create the edge:
myEdge = testWeb.addEdge(edgeData)
print("The created edge:")
print(myEdge)
print()

# 3. Load esges in the same way as nodes using a search key (by default the uuid (recommened))
# Note, the search term must be a string (we need to convert the uuid to a string)
loadedEdge = testWeb.loadEdge(str(myEdge.uuid))
print("The loaded edge:")
print(loadedEdge)
print()

print("The same edge:")
theSameEdge = testWeb.loadEdge(myEdge.title, term = "title")
print(theSameEdge)
print()

# Cleanup
if cleanUp == True:
    if os.path.exists(testWeb.path):
        shutil.rmtree(testWeb.path)