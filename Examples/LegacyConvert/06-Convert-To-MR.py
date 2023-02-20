''' ================================================================================
05 Convert to MR
================================================================================ '''

import spider as sp

# 1. Define your settings:
settings = {
    # Path to the manifest to convert:
    "webPath" : "/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project", 

    # The real path to the manifests:
    "path" : "http://localhost:9000/data/COESO-Project-Network", 

    # The place the MemoRekall network will be written to (None = webPath/mirador):
    "writePath" : "/Users/jacob/Documents/Git Repos/POC-mirador/www/COESO-Project-Network", 

    # If a manifest network already exists, remove it before creation [manifests, media]:
    "removePrevious" : [True, True],

    # Copy all node media to the write location (note that this also controls PDF conversion):
    "copyMedia" : True
}

# 2. Load the web:
toConvert = sp.loadWeb(settings["webPath"])

# 3. Get collections and check sanity:
nodeCollection = toConvert.loadCollection("e931dafa-26c4-4a8f-aa21-0821d37837c9")
edgeCollection = toConvert.loadCollection("7025a253-d8c6-4046-8b22-a4f0ca42587b")

configSanity = sp.checkCollectionSanity(toConvert, nodeCollection, edgeCollection)
if configSanity == True:
    print("Sane collection config :)")
else:
    print("Error! Collection config failed sanity check.")

# 3. Convert to MemoRekall:
toConvert.convertToMemoRekall(nodeList = nodeCollection, edgeList = edgeCollection, **settings)