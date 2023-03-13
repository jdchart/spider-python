import spider as sp
import os

web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")

nodeList = web.getFullList("nodes")

for item in nodeList:
    thisNode = web.loadNode(item)
    thisSource = thisNode.format.uri
    if thisSource.isascii() == False:
        oldSource = thisSource
        thisSource = ascii(thisSource)[1:-1]
        #thisSource = thisSource.strip('\t')
        thisSource = thisSource.replace("\t", "")
        thisSource = thisSource.replace('\\', '')  
        print()
        print(thisSource)
        thisNode.format.uri = thisSource
        if os.path.isfile(oldSource):
            os.rename(oldSource, thisSource)
        thisNode.write()








'''
import os

webPath = "/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project"


for root, dirs, files in os.walk(webPath):
    for file in files:
        print("Treating " + file + "...")
        fullPath = os.path.join(root, file)
        ext = os.path.splitext(file)[1]
        
        if ext == ".json":
            data = None
            with open(fullPath, 'r') as f:
                data = f.read()
                if data.isascii() == False:
                    print("Contents not ascii!")
            with open(fullPath, "w") as f:
                f.write(ascii(data)[1:-1])
        
        if fullPath.isascii() == False:
            print("Filename not ascii!")
            print()
            print(os.path.join(root, ascii(file)[1:-1]))
            print()
            os.rename(fullPath, os.path.join(root, ascii(file)[1:-1]))
'''