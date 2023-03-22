'''
SEARCH FOLDERS OF MANIFESTS, RENAME ANNOTATIONS TO CONVENTION
'''
from moviepy.editor import *
import utils

folderToChange = "/Users/jacob/Documents/Git Repos/POC-mirador/www/COESO-Project-Network"
toChangePrefix = 'http://localhost:9000/data/COESO-Project-Network/'
localPath = "/Users/jacob/Documents/Git Repos/POC-mirador/www/COESO-Project-Network/"

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
        manifestFileName = os.path.basename(item)
        justID = os.path.splitext(manifestFileName)[0]

        with open(item, 'r') as f:
            data = f.read()
            data = data.replace(
                '"id": "' + toChangePrefix + 'canvas',
                '"id": "' + toChangePrefix + justID + "/canvas"
            )
            data = data.replace(
                '"target": "' + toChangePrefix + 'canvas',
                '"target": "' + toChangePrefix + justID + "/canvas"
            )
            data = data.replace(
                '"id": "' + toChangePrefix + 'lower',
                '"id": "' + toChangePrefix + justID + "/lower"
            )
            data = data.replace(
                '"target": "' + toChangePrefix + 'lower',
                '"target": "' + toChangePrefix + justID + "/lower"
            )
        
        with open(item, 'w') as f:
            f.write(data)
        

        manifestData = utils.readJson(item)

        relPath = item.split(localPath)[1]
        finalPath = toChangePrefix + relPath

        manifestData["id"] = finalPath


        utils.writeJson(manifestData, item)