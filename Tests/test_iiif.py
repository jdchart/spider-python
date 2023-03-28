import unittest
import spider as sp
import os
import utils

class TestWeb(unittest.TestCase):
    def setUp(self):
        # Delete if already exists:
        utils.remove_file(os.path.join(os.getcwd(), "Test-Manifest.json"))

    def tearDown(self):
        # Delete if exists:
        utils.remove_file(os.path.join(os.getcwd(), "Test-Manifest.json"))

    def test_iiif(self):
        manifest = sp.Manifest(
            writepath = os.getcwd(),
            path = "www.test.com",
            filename = "Test-Manifest.json"
        )

        manifest.write()

        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(), "Test-Manifest.json")))
        manifestFileRead = utils.readJson(os.path.join(os.getcwd(), "Test-Manifest.json"))
        self.assertIsNotNone(manifestFileRead)

# Run
if __name__ == "__main__":
    unittest.main()