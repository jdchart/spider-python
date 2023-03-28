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

    def test_create(self):
        # Create web:
        metadata = {"path" : os.path.join(os.getcwd(), "temp")}
        myWeb = sp.createWeb(metadata)

        # Check the web object got created
        self.assertIsNotNone(myWeb)
        
        # Check directories and files were created
        self.check_direc_file_lists(
            os.getcwd(),
            ["temp", "temp/media", "temp/web", "temp/web/nodes", "temp/web/edges", 
                "temp/web/node_collections", "temp/web/edge_collections"],
            ["temp/metadata.json", "temp/.gitignore"]
        )

    def test_load(self):
        # Create web:
        metadata = {
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : "hello world"
        }
        myWeb = sp.createWeb(metadata)
        loaded = sp.loadWeb(os.path.join(os.getcwd(), "temp"))
        
        self.assertIsNotNone(loaded)

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