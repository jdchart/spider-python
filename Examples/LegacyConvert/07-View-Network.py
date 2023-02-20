''' ================================================================================
07 View Network
================================================================================ '''

import spider as sp
import networkx as nx
import matplotlib.pyplot as plt

web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")
nodeCollection = web.loadCollection("e931dafa-26c4-4a8f-aa21-0821d37837c9")
edgeCollection = web.loadCollection("7025a253-d8c6-4046-8b22-a4f0ca42587b")

network = web.convertToNetwork(nodeList = nodeCollection, edgeList = edgeCollection)

pos = nx.spring_layout(network, seed=3068)
nx.draw(network, pos=pos, with_labels=True)
plt.show()