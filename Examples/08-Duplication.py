import spider as sp
import os
import shutil

# 0. Script settings. 
# Set this to true to remove these test directories once you're done.
cleanUp = True

# 1. Create a new web:
testWeb = sp.createWeb({"path" : "/Users/jacob/Documents/Git Repos/Spider Webs/Test Nodes Duplicate", "title" : "My test web"})




testNode = testWeb.addNode({
    "title" : "My test node"
})

print(testNode)
print()

duplicated = testWeb.duplicateNode(str(testNode.uuid))

print(duplicated)


# Cleanup
if cleanUp == True:
    if os.path.exists(testWeb.path):
        shutil.rmtree(testWeb.path)