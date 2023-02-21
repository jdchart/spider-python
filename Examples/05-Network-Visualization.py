''' ================================================================================
05 NETWORK VISUALIZATION
View a web as a network.
================================================================================ '''

import spider as sp
import os
import shutil


# 0. Script settings. 
# Set this to true to remove these test directories once you're done.
cleanUp = True

# 1. Create a web with some content:
web = sp.createWeb({"path" : "/Users/jacob/Documents/Git Repos/Spider Webs/Network Test", "title" : "Test web"})
nodeList = []
for i in range(10):
    nodeList.append(str(web.addNode({"title" : "Node " + str(i)}).uuid))
for i in range(len(nodeList) - 1):
    web.addEdge({"title" : "Edge " + str(i + 1), "relation" : {"source" : nodeList[i], "target" : nodeList[i + 1]}})

web.addEdge({"title" : "Edge", "relation" : {"source" : nodeList[3], "target" : nodeList[5]}})


# 2. Convert to a networkx network:
network = web.convertToNetwork()

# 3. Draw the network:
network.display()

# 4. Save the network as an image.
network.saveToImage()

# Cleanup
if cleanUp == True:
    if os.path.exists(web.path):
        shutil.rmtree(web.path)