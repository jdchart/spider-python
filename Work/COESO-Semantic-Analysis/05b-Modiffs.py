import spider as sp
web = sp.loadWeb("/Users/jacob/Documents/Git Repos/Spider Webs/COESO-Project")

loaded = web.loadNode("b212ce06-53f7-4640-8cfb-8fe5213831fe")

loaded.instructionalMethod.important = True
loaded.write()