from colana import *

''' ================================================================================
01 Define a project
(Provide a path to the parsing matrix)
================================================================================ '''
myProject = Project(
    "/Users/jacob/Documents/Git Repos/spider-python/Examples/ColAna/parsingMatrix.json"
)

''' ================================================================================
Add profiles to the project
================================================================================ '''
myProject.addProfile(**{
    "name" : "Cosetta Graffione",

    "skills" : ["experimental"],
    "disciplines" : ["dance"],
    "languagesSpoken" : ["italian", "french", "english"]
})

myProject.addProfile(**{
    "name" : "Stefania Ferrando",

    "skills" : ["experimental", "academic-expert"],
    "disciplines" : ["philosophy"],
    "languagesSpoken" : ["french", "english"]
})

''' ================================================================================
Indicators
================================================================================ '''

# Skill type (individual):
print("\nSkill type (individual):")
for profile in myProject.profiles:
    score = profile.parseCategoricalFeature("skills", myProject.parsingMatrix)
    print("\t" + str(score))

# Diversity score (individual):
print("\nDiversity score (individual):")
for profile in myProject.profiles:
    score = profile.parseCompositeFeature("diversity")
    print("\t" + str(score))

# Collective skill diversity (collective):
print("\nCollective skill diversity (collective):")
score = myProject.parseCollectiveCategoricalFeature("skills")
print("\t" + str(score))