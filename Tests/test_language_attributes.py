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

    def test_creation_language_attributes(self):
        # Create web:
        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : "temp"
        })

        # Check attributes:
        utils.check_attribute(self, myWeb.language, list, ["en"])
        utils.check_attribute(self, myWeb.title, dict, {"en" : "temp"})
        utils.remove_web("temp")

        # Create web:
        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : {"fr": "temp"}
        })

        # Check attributes:
        utils.check_attribute(self, myWeb.language, list, ["fr"])
        utils.check_attribute(self, myWeb.title, dict, {"fr" : "temp"})
        utils.remove_web("temp")

        # Create web:
        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "language" : ["fr"],
            "title" : "temp"
        })

        # Check attributes:
        utils.check_attribute(self, myWeb.language, list, ["fr"])
        utils.check_attribute(self, myWeb.title, dict, {"fr" : "temp"})
        utils.remove_web("temp")

        # Create web:
        myWeb = sp.createWeb({
            "path" : os.path.join(os.getcwd(), "temp"),
            "language" : ["fr"],
            "title" : {"sp": "temp"}
        })

        # Check attributes:
        utils.check_attribute(self, myWeb.language, list, ["fr", "sp"])
        utils.check_attribute(self, myWeb.title, dict, {"sp" : "temp", "fr" : ""})
        utils.remove_web("temp")

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
        utils.check_attribute(self, myWeb.language, list, ["en"])
        utils.check_attribute(self, myWeb.title, dict, {"en" : "title"})
        utils.check_attribute(self, myWeb.subject, dict, {"en" : "subject"})
        utils.check_attribute(self, myWeb.description, dict, {"en" : "description"})
        utils.check_attribute(self, myWeb.type, dict, {"en" : "type"})
        utils.check_attribute(self, myWeb.source, dict, {"en" : "source"})
        utils.check_attribute(self, myWeb.creator, dict, {"en" : "creator"})
        utils.check_attribute(self, myWeb.publisher, dict, {"en" : "publisher"})
        utils.check_attribute(self, myWeb.contributor, dict, {"en" : "contributor"})
        utils.check_attribute(self, myWeb.rights, dict, {"en" : "rights"})
        utils.check_attribute(self, myWeb.audience, dict, {"en" : "audience"})
        utils.check_attribute(self, myWeb.provenance, dict, {"en" : "provenance"})
        utils.check_attribute(self, myWeb.rightsHolder, dict, {"en" : "rightsHolder"})
        utils.check_attribute(self, myWeb.accrualMethod, dict, {"en" : "accrualMethod"})
        utils.check_attribute(self, myWeb.accrualPeriodicity, dict, {"en" : "accrualPeriodicity"})
        utils.check_attribute(self, myWeb.accrualPolicy, dict, {"en" : "accrualPolicy"})
        utils.remove_web("temp")

# Run
if __name__ == "__main__":
    unittest.main()