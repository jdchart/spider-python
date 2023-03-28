import unittest
import spider as sp
import os
import utils

class TestWeb(unittest.TestCase):
    def setUp(self):
        # Delete if already exists:
        utils.remove_web("temp")

    def tearDown(self):
        # Delete if exists:
        utils.remove_web("temp")

    def test_tags(self):
        # Create web:
        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : "temp"
        })

        utils.check_attribute(self, myWeb.tags, dict, {"en" : []})
        utils.remove_web("temp")

        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : "temp",
            "tags" : "myTag"
        })

        utils.check_attribute(self, myWeb.tags, dict, {"en" : ["myTag"]})
        utils.remove_web("temp")

        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : "temp"
        })

        myWeb.tags = "newTag"
        utils.check_attribute(self, myWeb.tags, dict, {"en" : ["newTag"]})
        myWeb.tags = "anotherTag"
        utils.check_attribute(self, myWeb.tags, dict, {"en" : ["anotherTag"]})
        myWeb.tags = ["tag1", "tag2"]
        utils.check_attribute(self, myWeb.tags, dict, {"en" : ["tag1", "tag2"]})

        myWeb.tags = {"en" : "hello world"}
        utils.check_attribute(self, myWeb.tags, dict, {"en" : ["hello world"]})
        myWeb.tags = {"en" : ["hello world", "anotherTag"]}
        utils.check_attribute(self, myWeb.tags, dict, {"en" : ["hello world", "anotherTag"]})

        myWeb.tags = {"en" : ["aTag", "anotherTag"], "fr" : "enFrancais"}
        utils.check_attribute(self, myWeb.tags, dict, {"en" : ["aTag", "anotherTag"], "fr" : ["enFrancais"]})
        utils.check_attribute(self, myWeb.language, list, ["en", "fr"])
        utils.check_attribute(self, myWeb.title, dict, {"en" : "temp", "fr" : ""})

        myWeb.appendTag("appendedTag")
        utils.check_attribute(self, myWeb.tags, dict, {"en" : ["aTag", "anotherTag", "appendedTag"], "fr" : ["enFrancais"]})
        myWeb.appendTag(["1", "2"])
        utils.check_attribute(self, myWeb.tags, dict, {"en" : ["aTag", "anotherTag", "appendedTag", "1", "2"], "fr" : ["enFrancais"]})
        myWeb.appendTag({
            "fr" : "unAutre",
            "sp" : ["un", "dos"]
        })
        utils.check_attribute(self, myWeb.tags, dict, {"en" : ["aTag", "anotherTag", "appendedTag", "1", "2"], "fr" : ["enFrancais", "unAutre"], "sp" : ["un", "dos"]})
        utils.check_attribute(self, myWeb.language, list, ["en", "fr", "sp"])
        utils.remove_web("temp")

        # TODO: Add unittesting for language removal here...
        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : "temp"
        })
        utils.remove_web("temp")

# Run
if __name__ == "__main__":
    unittest.main()