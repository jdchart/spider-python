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

    def test_creation_language_attributes(self):
        # Create web:
        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : "temp"
        })

        # Check attributes:
        self.check_attribute(myWeb.language, list, ["en"])
        self.check_attribute(myWeb.title, dict, {"en" : "temp"})
        self.remove_web("temp")

        # Create web:
        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : {"fr": "temp"}
        })

        # Check attributes:
        self.check_attribute(myWeb.language, list, ["fr"])
        self.check_attribute(myWeb.title, dict, {"fr" : "temp"})
        self.remove_web("temp")

        # Create web:
        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "language" : ["fr"],
            "title" : "temp"
        })

        # Check attributes:
        self.check_attribute(myWeb.language, list, ["fr"])
        self.check_attribute(myWeb.title, dict, {"fr" : "temp"})
        self.remove_web("temp")

        # Create web:
        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "language" : ["fr"],
            "title" : {"sp": "temp"}
        })

        # Check attributes:
        self.check_attribute(myWeb.language, list, ["fr", "sp"])
        self.check_attribute(myWeb.title, dict, {"sp" : "temp", "fr" : ""})
        self.remove_web("temp")

        # Create web:
        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : "title",
            "subject" : "subject",
            "description" : "description",
            "type" : "type",
            "source" : "source",
            "creator" : "creator",
            "publisher" : "publisher",
            "contributor" : "contributor",
            "rights" : "rights",
            "audience" : "audience",
            "provenance" : "provenance",
            "rightsHolder" : "rightsHolder",
            "accrualMethod" : "accrualMethod",
            "accrualPeriodicity" : "accrualPeriodicity",
            "accrualPolicy" : "accrualPolicy"
        })

        # Check attributes:
        self.check_attribute(myWeb.language, list, ["en"])
        self.check_attribute(myWeb.title, dict, {"en" : "title"})
        self.check_attribute(myWeb.subject, dict, {"en" : "subject"})
        self.check_attribute(myWeb.description, dict, {"en" : "description"})
        self.check_attribute(myWeb.type, dict, {"en" : "type"})
        self.check_attribute(myWeb.source, dict, {"en" : "source"})
        self.check_attribute(myWeb.creator, dict, {"en" : "creator"})
        self.check_attribute(myWeb.publisher, dict, {"en" : "publisher"})
        self.check_attribute(myWeb.contributor, dict, {"en" : "contributor"})
        self.check_attribute(myWeb.rights, dict, {"en" : "rights"})
        self.check_attribute(myWeb.audience, dict, {"en" : "audience"})
        self.check_attribute(myWeb.provenance, dict, {"en" : "provenance"})
        self.check_attribute(myWeb.rightsHolder, dict, {"en" : "rightsHolder"})
        self.check_attribute(myWeb.accrualMethod, dict, {"en" : "accrualMethod"})
        self.check_attribute(myWeb.accrualPeriodicity, dict, {"en" : "accrualPeriodicity"})
        self.check_attribute(myWeb.accrualPolicy, dict, {"en" : "accrualPolicy"})
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