''' ================================================================================
02 EXPORT TO CSV
Export the collection tov csv to see what we're dealing with
================================================================================ '''

import spider as sp

# Load web
web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")

nodeCollection = web.loadCollection("0f465f8c-d89b-452a-a056-5fb96c31d114")

nodeCollection.collectionToCSV(
    web, 
    "/Users/jacob/Desktop/node_collection.csv",
    fields = ["title", "date", "coverage", "uuid", "format"]
)