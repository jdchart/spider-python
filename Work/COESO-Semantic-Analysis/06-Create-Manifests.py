import spider as sp

# 1. Define your settings:
settings = {
    # Path to the manifest to convert:
    "webPath" : "/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project", 

    # The real path to the manifests:
    #"path" : "http://localhost:9000/data/COESO-Project-Network", 
    "path" : "https://iiif.tetras-libre.fr/data/demo-content/Jacob/www-COESO-TEST/",

    # The place the MemoRekall network will be written to (None = webPath/mirador):
    #"writePath" : "/Users/jacob/Documents/Git Repos/POC-mirador/www/COESO-Project-Network",
    "writePath" : "/Users/jacob/Documents/Git Repos/demo-content/Jacob/www-COESO-TEST",

    # If a manifest network already exists, remove it before creation [manifests, media]:
    "removePrevious" : [False, False],

    # Copy all node media to the write location (note that this also controls PDF conversion):
    "copyMedia" : False,

    "lang" : "fr"
}

# 2. Load the web:
toConvert = sp.loadWeb(settings["webPath"])

# 3. Get collections and check sanity:
nodeCollection = toConvert.loadCollection("edd3e266-839d-4980-bd5f-c947267a8540")
edgeCollection = toConvert.loadCollection("17dd7dcc-b864-4657-b9df-04773bd1b3b5")

'''
configSanity = sp.checkCollectionSanity(toConvert, nodeCollection, edgeCollection)
if configSanity == True:
    print("Sane collection config :)")
else:
    print("Error! Collection config failed sanity check.")
'''

# 3. Convert to MemoRekall:
toConvert.convertToMemoRekall(nodeList = nodeCollection, edgeList = edgeCollection, **settings)