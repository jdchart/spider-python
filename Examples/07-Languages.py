''' ================================================================================
07 LANGUAGES
A spider element can have multiple languages for its content.
Here's how it works.
================================================================================ '''

import spider as sp
import os
import shutil

# 0. Script settings. 
# Set this to true to remove these test directories once you're done.
cleanUp = False

# 1. Create a web, and set a field's language with an object like so:
web = sp.createWeb({
    "path" : "/Users/jacob/Documents/Git Repos/Spider Webs/Language Test",
    "language" : ["en", "fr"], 
    "title" : {
            "en" : "Language Web",
            "fr" : "Une toile de langage"
        },
    "description" : {
        "en" : "A web with multiple languages.",
        "fr" : "Une toile avec plusieurs langues."
    },
    "tags" : {
        "en" : ["web", "languages"],
        "fr" : ["toile", "langues"]
    }
})

# 2. By default, we access the first item:
print(web.title)

# 3. Use the getFromLang() method to access other languages:
print(web.getFromLang("title", "en"))
print(web.getFromLang("title", "fr"))

# 4. Here is a full list of attributes that have langiuage functionality:
# "title", "subject", "description", "type", "source", "creator", "publisher",
# "contributor", "rights", "identifier", "audience", "provenance", "rightsHolder",
# "accrualMethod", "accrualPeriodicity", "accrualPolicy", "tags"

print(web.description)
print(web.getFromLang("description", "fr"))

print()
print(web.tags)

# Return the full object with "full" as language inptu:
print(web.getFromLang("title", "full"))

# Cleanup
if cleanUp == True:
    if os.path.exists(web.path):
        shutil.rmtree(web.path)