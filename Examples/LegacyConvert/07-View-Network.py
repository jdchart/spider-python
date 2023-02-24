''' ================================================================================
07 View Network
================================================================================ '''

import spider as sp

web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")
nodeCollection = web.loadCollection("e931dafa-26c4-4a8f-aa21-0821d37837c9")
edgeCollection = web.loadCollection("7025a253-d8c6-4046-8b22-a4f0ca42587b")
#edgeCollection = web.loadCollection("0fecdd7f-003e-4635-a0fc-553b962e6d16") # Automatic 

network = web.convertToNetwork(nodeList = nodeCollection, edgeList = edgeCollection)
network.display(
    #algo = "spring"
    #algo = "circular"
    #algo = "fr"
    algo = "spectral"
    #algo = "random"
)