''' ================================================================================
09 Add Main Network Manifest
================================================================================ '''

import spider as sp

# 1. Define your settings:
settings = {
    # The real path to the manifests:
    #"path" : "http://localhost:9000/data/COESO-Project-Network",
    "path" : "https://iiif.tetras-libre.fr/data/demo-content/Jacob/www-COESO-TEST/",

    # The place the MemoRekall network will be written to (None = webPath/mirador):
    #"writePath" : "/Users/jacob/Documents/Git Repos/POC-mirador/www/COESO-Project-Network",
    "writePath" : "/Users/jacob/Documents/Git Repos/demo-content/Jacob/www-COESO-TEST",

    "networkName" : "Automatic Network Configuration",

    "algo" : "circular"
}

# What to transform:
web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")
nodeCollection = web.loadCollection("e931dafa-26c4-4a8f-aa21-0821d37837c9")

#edgeCollection = web.loadCollection("7025a253-d8c6-4046-8b22-a4f0ca42587b")
edgeCollection = web.loadCollection("0fecdd7f-003e-4635-a0fc-553b962e6d16") # Automatic 

network = web.convertToNetwork(
    nodeList = nodeCollection, 
    edgeList = edgeCollection
)
#network.display()

#network.saveToImage()
network.saveToManifest(web, **settings)