import utils

manifestpath = "/Users/jacob/Desktop/c41b0c91-f735-41fa-83f0-d9f836bb9ca1.json"
fulldatapath = "/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/ConvertData/fullData.json"

manifestData = utils.readJson(manifestpath)
fulldata = utils.readJson(fulldatapath)

fullDataKeyList = list(fulldata.keys())


count = 0
for annotation in manifestData["items"][0]["annotations"][0]["items"]:
    print()
    

    thisdata = fulldata[fullDataKeyList[count]]
    print(thisdata)

    originalTarget = annotation["target"]
    targetStart = originalTarget.split("#t=-0.001,-0.001")[0]
    newtarget = targetStart + "#xywh=" + str(thisdata["centroidEllipse"][0]) + ',' + str(thisdata["centroidEllipse"][1]) + ",8,8"
    print(originalTarget)
    print(targetStart)
    print(newtarget)

    annotation["target"] = newtarget
    count = count + 1


utils.writeJson(manifestData, "/Users/jacob/Documents/Git Repos/spider-python/Work/ColAna/OUTPUT/ConvertData/NEWMAINMANIF.json")