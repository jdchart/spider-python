''' ================================================================================
01 NODE COLLECTION
Make a collection of only main ressource nodes.
================================================================================ '''

import spider as sp

# Load web
web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")

nodeCollection = web.loadCollection("e931dafa-26c4-4a8f-aa21-0821d37837c9").contentToList()


toKeep = []

for node in nodeCollection:
    thisNode = web.loadNode(node)
    print(thisNode.title)
    ans = input("Keep? (y)")
    if ans == "y":
        toKeep.append(node)


newCollection = web.addCollection("node", {"title" : "Fond d'archive"})
newCollection.addContent(toKeep)

print(newCollection.uuid)
print(newCollection.path)