''' ================================================================================
09 Add Main Network Manifest
================================================================================ '''

import spider as sp

# 1. Define your settings:
settings = {
    # The real path to the manifests:
    "path" : "http://localhost:9000/data/COESO-Project-Network",

    # The place the MemoRekall network will be written to (None = webPath/mirador):
    "writePath" : "/Users/jacob/Documents/Git Repos/POC-mirador/www/COESO-Project-Network",

    "networkName" : "Config 1"
}

# What to transform:
web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")
nodeCollection = web.loadCollection("e931dafa-26c4-4a8f-aa21-0821d37837c9")
edgeCollection = web.loadCollection("7025a253-d8c6-4046-8b22-a4f0ca42587b")

network = web.convertToNetwork(
    nodeList = nodeCollection, 
    edgeList = edgeCollection
)
#network.display()

#network.saveToImage()
network.saveToManifest(web, **settings)