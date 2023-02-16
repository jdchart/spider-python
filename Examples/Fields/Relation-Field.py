''' ================================================================================
RELATION FIELD
The Dublin Core `relation` field looks to represent a reference to a related resource.
This is where spider puts information pertaining to an edge between two elements.
Note that the edge is itself an element and can be described in the same way as anything else.
Spider will parse data into a single relation entry which can be easily decoded.
================================================================================ '''

import spider as sp
import os
import shutil

# 0. Script settings. 
# Set this to true to remove these test directories once you're done.
cleanUp = False

# 1. Create a new web and some nodes:
testWeb = sp.createWeb({"path" : "/Users/jacob/Documents/Git Repos/Spider Webs/Test Edges", "title" : "My test web"})
nodes = []
for i in range(3):
    nodes.append(testWeb.addNode({"title" : "Node " + str(i + 1)}))

# 2. Set the relation data:
# The source and target values accept a UUUID string corresponding to the node.
# Note that an esge can have more than one region in it's source or target.
relationData = {
    "source" : str(nodes[0].uuid),
    "target" : str(nodes[1].uuid),
    "sourceRegions" : [
        {
            "start" : -1, # The start time in the source node for the edge in ms (-1 = beginning).
            "end" : 1000, # The end time in the source node for the edge in ms (-1 = the end).
            "dims" : [-1] # The coordinates the edge occupies for the source ([-1] = the whole of the ressource, or [x, y, w, h])
        }
    ],
    "targetRegions" : [
        {"dims" : [10, 10, 300, 400]},
        {"dims" : [20, 40, 300, 400]}
    ]
}

# 3. Create the edge:
myEdge = testWeb.addEdge({
    "title" : "My amazing edge",
    "relation" : relationData
})
print("The created edge:")
print(myEdge)
print()

# 4. Set attrributes:
myEdge.relation.source = str(nodes[2].uuid)
myEdge.relation.sourceRegions.append({"start" : -1, "end" : -1})
print("Modified edge:")
print(myEdge)
print()

# 5. Check that loading is working:
loadedEdge = testWeb.loadEdge(str(myEdge.uuid))
print("Loaded edge:")
print(myEdge)
print()

# Cleanup
if cleanUp == True:
    if os.path.exists(testWeb.path):
        shutil.rmtree(testWeb.path)