''' ================================================================================
CONVERT WEB TO MEMOREKALL
Convert a web structure to a network of IIIF manifests.
We load the web we want to convert, then call the convertToMemoRekall() function.
================================================================================ '''

import spider as sp

# 1. Define your settings:
settings = {
    # Path to the manifest to convert:
    "webPath" : "/Users/jacob/Documents/Git Repos/Spider Webs/Media Web", 

    # The real path to the manifests:
    "path" : "http://localhost:9000/data/Media_web_test", 

    # The place the MemoRekall network will be written to (None = webPath/mirador):
    "writePath" : "/Users/jacob/Documents/Git Repos/POC-mirador/www/Media_web_test", 

    # If a manifest network already exists, remove it before creation [manifests, media]:
    "removePrevious" : [True, False],

    # Copy all node media to the write location (note that this also controls PDF conversion):
    "copyMedia" : False
}

# 2. Load the web:
toConvert = sp.loadWeb(settings["webPath"])

# 3. Convert to MemoRekall:
toConvert.convertToMemoRekall(**settings)