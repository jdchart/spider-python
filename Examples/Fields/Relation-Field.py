''' ================================================================================
RELATION FIELD
The Dublin Core `relation` field looks to represent the extent or scope of the content of the resource.
Notably: time period and geographic location.
Spider will parse data into a single coverage entry which can be easily decoded.
================================================================================ '''

import spider as sp
import datetime
import time
import os
import shutil

# 0. Script settings. 
# Set this to true to remove these test directories once you're done.
cleanUp = False

# 1. Setting the coverage of the entire web:
# Note that if the string value contains "_", this will be converted to " " on load.
coverageData = {
        "startDateTime" : datetime.datetime.now(),
        "endDateTime" : datetime.datetime.now(),
        "modificationDateTimes" : [
            {"datetime" : datetime.datetime.now(), "title" : "Modif 1", "description" : "My modification 1"},
            {"datetime" : datetime.datetime.now(), "title" : "Modif 2", "description" : "My modification 2"}
        ],
        "region" : "Bretagne, France."
}

testWeb = sp.createWeb({
    "path" : "/Users/jacob/Documents/Git Repos/Spider Webs/Coverage test", 
    "title" : "Coverage test web",
    "coverage" : coverageData
})

# 3. Set attributes:
time.sleep(2)
testWeb.coverage.endDateTime = datetime.datetime.now()
testWeb.write()
print("Web coverage:")
print(testWeb.coverage)
print()

# 4. Check that loading is working:
loadedWeb = sp.loadWeb(testWeb.path)
print("Loaded web coverage:")
print(loadedWeb.coverage)
print()

# 5. Do the same with nodes and edges:
aNode = testWeb.addNode({"title" : "My node", "coverage" : {"startDateTime" : datetime.datetime.now()}})
print("Node coverage:")
print(aNode.coverage)
print()

# Cleanup
if cleanUp == True:
    if os.path.exists(testWeb.path):
        shutil.rmtree(testWeb.path)