''' ================================================================================
INSTRUCTIONAL METHOD FIELD
The Dublin Core `instructionalMethod` field looks to represent a process, used to engender knowledge, attitudes and skills, that the resource is designed to support
We have interpreted this as a field indicating the method by which the ressource can be displayed/viewed/communicated.
Therefore this is where information pertaining to the display of the ressource is given.
Notably and options for MemoRekall conversion.
This data will have different meanings according to the element type (web, edge or node) and the way it is to be decoded.
Spider will parse data into a single instructionalMethod entry which can be easily decoded.
================================================================================ '''

import spider as sp
import os
import shutil

# 0. Script settings. 
# Set this to true to remove these test directories once you're done.
cleanUp = False

# 1. Instructional method for a web
# There isn't much to add here, but we can still add any of the available instructionalMethod fields
webDisplay = {
    "color" : "#88bddb",
    "important" : True
}
testWeb = sp.createWeb({
    "path" : "/Users/jacob/Documents/Git Repos/Spider Webs/Test Instruction Method",
    "title" : "My test display web",
    "instructionalMethod" : webDisplay
})
print("The created web:")
print(testWeb)
print()

# 2. Instructional method for a node
nodeDisplay = {
    "color" : "#67c781",
    "important" : True, # For MemoRekall parsing, this will indicate if it is a top-level manifest or not
    "annotationPaint" : True, # For MemoRekall parsing, indicate if the node is painted when it is an annotation
    "annotationOverlay" : True, # For MemoRekall parsing, indicate if the annotation is painted ontop of the main ressource or underneath.
    "annotationDisplayPos" : [0, 0], # For MemoRekall parsing, where to paint the ressourse on the canvas. (starting from top left if overlayed, starting from bottom of main ressource if not overlayed).
    "annotationDisplayScale" : 1 # For MemoRekall parsing, the scale of the ressource (1 = full size)
}
testNode = testWeb.addNode({"title" : "My display node", "instructionalMethod" : nodeDisplay})

# Set attributes:
testNode.instructionalMethod.annotationOverlay = False

print("Created node:")
print(testNode)
print()

# Cleanup
if cleanUp == True:
    if os.path.exists(testWeb.path):
        shutil.rmtree(testWeb.path)