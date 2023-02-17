''' ================================================================================
05 NETWORK VISUALIZATION
View a web as a network.
================================================================================ '''

import spider as sp
import os
import shutil
import networkx as nx
import matplotlib.pyplot as plt

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

# 2. Convert to a networkx network:
network = web.convertToNetwork()

# 3. Draw the network using matplotlib
pos = nx.spring_layout(network, seed=3068)
nx.draw(network, pos=pos, with_labels=True)
plt.show()

# Cleanup
if cleanUp == True:
    if os.path.exists(web.path):
        shutil.rmtree(web.path)