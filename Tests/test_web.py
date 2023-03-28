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

    def test_create(self):
        # Create web:
        metadata = {"path" : os.path.join(os.getcwd(), "temp")}
        myWeb = sp.createWeb(metadata)

        # Check the web object got created
        self.assertIsNotNone(myWeb)
        
        # Check directories and files were created
        utils.check_direc_file_lists(self, 
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

# Run
if __name__ == "__main__":
    unittest.main()