'''
REPLACE STRINGS IN A JSON FILES IN A FOLDER AND IT'S SUBFOLDERS
'''
import os

folderToChange = "/Users/jacob/Documents/Git Repos/coeso-deliverable"

replaceMap = [
    {
        "oldString" : "http://localhost:9000/data/COESO-Project-Network",
        "newString" : "https://coeso.tetras-libre.fr/data/coeso-deliverable"
    }
]

'''
replaceMap = [
    {
        "oldString" : "https://iiif.tetras-libre.fr/data/demo-content/Jacob/www-COESO-TEST",
        "newString" : "https://coeso.tetras-libre.fr/data/coeso-deliverable"
    },
    {
        "oldString" : "http://localhost:9000/data/COESO-Project-Network",
        "newString" : "https://coeso.tetras-libre.fr/data/coeso-deliverable"
    },
    {
        "oldString" : "Capsule_Convert_Network",
        "newString" : "Capsule_Convert_Network_modified"
    }
]
'''

def absoluteFilePaths(directory):
    fileList = []
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            fileList.append(os.path.abspath(os.path.join(dirpath, f)))
    return fileList

lis = absoluteFilePaths(folderToChange)

for item in lis:
    ext = os.path.splitext(item)[1].replace(".","")

    if ext == "json":
        print("Treating " + item + "...")

        with open(item, 'r') as f:
            data = f.read()
            for mapping in replaceMap:
                data = data.replace(mapping["oldString"], mapping["newString"])
        
        with open(item, 'w') as f:
            f.write(data)