import unittest
import spider as sp
import os
import shutil

class TestWeb(unittest.TestCase):
    def setUp(self):
        # Delete if already exists:
        self.remove_web("temp")

    def tearDown(self):
        # Delete if exists:
        self.remove_web("temp")

    def test_tags(self):
        # Create web:
        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : "temp"
        })

        self.check_attribute(myWeb.tags, dict, {"en" : []})
        self.remove_web("temp")

        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : "temp",
            "tags" : "myTag"
        })

        self.check_attribute(myWeb.tags, dict, {"en" : ["myTag"]})
        self.remove_web("temp")

        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : "temp"
        })

        myWeb.tags = "newTag"
        self.check_attribute(myWeb.tags, dict, {"en" : ["newTag"]})
        myWeb.tags = "anotherTag"
        self.check_attribute(myWeb.tags, dict, {"en" : ["anotherTag"]})
        myWeb.tags = ["tag1", "tag2"]
        self.check_attribute(myWeb.tags, dict, {"en" : ["tag1", "tag2"]})

        myWeb.tags = {"en" : "hello world"}
        self.check_attribute(myWeb.tags, dict, {"en" : ["hello world"]})
        myWeb.tags = {"en" : ["hello world", "anotherTag"]}
        self.check_attribute(myWeb.tags, dict, {"en" : ["hello world", "anotherTag"]})

        myWeb.tags = {"en" : ["aTag", "anotherTag"], "fr" : "enFrancais"}
        self.check_attribute(myWeb.tags, dict, {"en" : ["aTag", "anotherTag"], "fr" : ["enFrancais"]})
        self.check_attribute(myWeb.language, list, ["en", "fr"])
        self.check_attribute(myWeb.title, dict, {"en" : "temp", "fr" : ""})

        myWeb.appendTag("appendedTag")
        self.check_attribute(myWeb.tags, dict, {"en" : ["aTag", "anotherTag", "appendedTag"], "fr" : ["enFrancais"]})
        myWeb.appendTag(["1", "2"])
        self.check_attribute(myWeb.tags, dict, {"en" : ["aTag", "anotherTag", "appendedTag", "1", "2"], "fr" : ["enFrancais"]})
        myWeb.appendTag({
            "fr" : "unAutre",
            "sp" : ["un", "dos"]
        })
        self.check_attribute(myWeb.tags, dict, {"en" : ["aTag", "anotherTag", "appendedTag", "1", "2"], "fr" : ["enFrancais", "unAutre"], "sp" : ["un", "dos"]})
        self.check_attribute(myWeb.language, list, ["en", "fr", "sp"])
        self.remove_web("temp")

        # TODO: Add unittesting for language removal here...
        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : "temp"
        })
        self.remove_web("temp")

    def check_attribute(self, attr, attributeType, attributeValue):
        self.assertIsInstance(attr, attributeType)
        self.assertEqual(attr, attributeValue)

    def remove_web(self, webFolder):
        if os.path.isdir(os.path.join(os.getcwd(), webFolder)):
            shutil.rmtree(os.path.join(os.getcwd(), webFolder))

    def check_direc_file_lists(self, prefix, direcList, fileList):
        for item in direcList:
            self.assertTrue(os.path.isdir(os.path.join(prefix, item)))
        for item in fileList:
            self.assertTrue(os.path.isfile(os.path.join(prefix, item)))

# Run
if __name__ == "__main__":
    unittest.main()