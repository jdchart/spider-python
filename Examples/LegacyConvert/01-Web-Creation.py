''' ================================================================================
01 Web creation
================================================================================ '''

import spider as sp
import datetime
import utils

# 1. Create a web:
web = sp.createWeb({
    "path" : "/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project", 
    "title" : "COESO Project",
    "subject" : "COESO project;research project;contemporary dance;philosophy",
    "description" : "A network describing the work that occured around the COESO project Pilot 2: Dancing Philosophy.",
    "type" : "document network",
    "source" : "various",
    "creator" : "Jacob Hart, Clarisse Bardiot, Sébastien Hildebrand",
    "rights" : "open source",
    "language" : "en",
    "audience" : "Those interested in the COESO project, contemporary dance and philosophy.",
    "provenance" : "various",
    "coverage" : {
        "region" : "Europe (France and Italy)",
        "startDateTime" : datetime.datetime(2021, 1, 1),
        "endDateTime" : datetime.datetime(2023, 12, 31)
    }
})

# 2. Get a list of media files:
fileList = utils.collectFiles("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-source")

# 3. Convert files with the mediaToNode(path, copyMedia) function:
for item in fileList:
    web.mediaToNode(item, True)