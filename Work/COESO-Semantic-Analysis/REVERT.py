import spider as sp
import utils

webPath = "/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project"
# Load web
web = sp.loadWeb(webPath)

mappingDataOld = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Examples/COESO-Semantic-Analysis/OUTPUT/Capsule-mapping.json")
mappingDataFucked = utils.readJson("/Users/jacob/Documents/Git Repos/spider-python/Examples/COESO-Semantic-Analysis/OUTPUT/Capsule-mapping-DUPLICATED.json")

count = 0
for item in mappingDataOld:
    print(item)
    loadNode = web.loadNode(item)
    loadNode.uuid = item
    #loadNode.path = "/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project/web/nodes" + loadNode.uuid + "node.json"
    loadNode.write()

    count = count + 1