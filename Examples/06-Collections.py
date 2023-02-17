''' ================================================================================
06 COLLECTIONS
You can create collections of nodes and edges.
This means that you can have several configurations of the web data
without having to keep duplicates of the same data.
We create collections of nodes and of edges so that they can grow independently.
================================================================================ '''

import spider as sp
import os
import shutil
import networkx as nx
import matplotlib.pyplot as plt

# 0. Script settings. 
# Set this to true to remove these test directories once you're done.
cleanUp = False

# 1. Create a web with some content:
web = sp.createWeb({"path" : "/Users/jacob/Documents/Git Repos/Spider Webs/Collections Test", "title" : "Test web"})
nodeList = []
for i in range(10):
    nodeList.append(str(web.addNode({"title" : "Node " + str(i)}).uuid))
edgeList = []
for i in range(len(nodeList) - 1):
    edgeList.append(str(web.addEdge({"title" : "Edge " + str(i + 1), "relation" : {"source" : nodeList[i], "target" : nodeList[i + 1]}}).uuid))

# 2. Create a collection of nodes:
myNodeCollection = web.addCollection("node", {"title" : "My node collection"})
print("Created collection:")
print(myNodeCollection)
print()

# (You can load collections in the same way as nodes and edges):
loadedCollection = web.loadCollection(str(myNodeCollection.uuid))
print("Loaded collection:")
print(loadedCollection)
print()

# 3. We can add items to the collection using the addContent() function.
# Either provide a uuid string, or an array of uuid strings
myNodeCollection.addContent(nodeList)

# 4. Lets create a collection of edges using all the edges, and another using only one:
myEdgeCollection = web.addCollection("edge", {})
myEdgeCollection.addContent(edgeList)

mySecondEdgeCollection = web.addCollection("edge", {})
mySecondEdgeCollection.addContent(edgeList[0])

# 4. Use collections for things like network visualisation:
# We make one using the first edge collection, and another using the second
network = web.convertToNetwork(nodeList = myNodeCollection, edgeList = myEdgeCollection)
network2 = web.convertToNetwork(nodeList = myNodeCollection, edgeList = mySecondEdgeCollection)

# Visualise the collections:
pos = nx.spring_layout(network, seed=3068)
nx.draw(network, pos=pos, with_labels=True)
plt.show()

pos = nx.spring_layout(network2, seed=3068)
nx.draw(network2, pos=pos, with_labels=True)
plt.show()

# Cleanup
if cleanUp == True:
    if os.path.exists(web.path):
        shutil.rmtree(web.path)