''' ================================================================================
03 CAPSULE CONVERT MAPPING
================================================================================ '''
from MRLegacy import MRCapsule
import utils

capsuleFile = "/Users/jacob/Documents/Git Repos/spider-python/Examples/COESO-Semantic-Analysis/DATA/COESO_capsule.php"
#capsuleFile = "/Users/jacob/Documents/Git Repos/spider-python/Examples/COESO-Semantic-Analysis/DATA/flucoma-test-capsule.php"
capsule = MRCapsule(capsuleFile)

print("Found " + str(len(capsule.elements)) + " elements.")

capsule.write("/Users/jacob/Documents/Git Repos/spider-python/Examples/COESO-Semantic-Analysis/OUTPUT/CAPSULE-OUT.json")

mapping = {}

for item in capsule.elements:
    entry = {}
    print()
    print(item.collectData())
    cmdIn = input("Please give uuid:")
    mapping[cmdIn] = item.collectData()

utils.writeJson(mapping, "/Users/jacob/Documents/Git Repos/spider-python/Examples/COESO-Semantic-Analysis/OUTPUT/Capsule-mapping.json")