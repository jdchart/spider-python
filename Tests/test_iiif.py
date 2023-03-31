import unittest
import spider as sp
import os
import utils

class TestWeb(unittest.TestCase):
    def setUp(self):
        # Delete if already exists:
        utils.remove_file(os.path.join(os.getcwd(), "Test-Manifest.json"))
        utils.remove_web("tempNetCon")
        utils.remove_web("tempFromMedia")
        utils.remove_dir(os.path.join(os.getcwd(), "testManifestNetwork"))

    def tearDown(self):
        # Delete if exists:
        utils.remove_file(os.path.join(os.getcwd(), "Test-Manifest.json"))
        utils.remove_web("tempNetCon")
        utils.remove_web("tempFromMedia")
        utils.remove_dir(os.path.join(os.getcwd(), "testManifestNetwork")) 

    def test_iiif(self):
        manifest = sp.Manifest(
            writepath = os.getcwd(),
            path = "www.test.com",
            filename = "Test-Manifest.json",
            label = {
                "en" : ["Test Manifest"],
                "fr" : ["Manifest Test"]
            }
        )

        canvas1 = manifest.addCanvas(
            width = 100,
            height = 100,
            duration = 10
        )

        annotPage1 = canvas1.addAnnotationPage(
            type = "page"
        )

        mediaItem1 = annotPage1.addMediaItem()

        manifest.write()

        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(), "Test-Manifest.json")))
        manifestFileRead = utils.readJson(os.path.join(os.getcwd(), "Test-Manifest.json"))
        self.assertIsNotNone(manifestFileRead)
    
    def test_network_to_manifest(self):
        # 1. Create a web with some content:
        web = utils.create_basic_web("tempNetCon", "test network", 10)

        # Create the network
        network = sp.webToNetworkx(web)

        # Network to manifest:
        manifest = sp.networkxToManifest(network, web, path = "http://localhost:9000/data/", writePath = os.getcwd(), networkName = "test network")

        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(), "test_network.json")))
        self.assertTrue(os.path.isfile(os.path.join(os.getcwd(), "media/test_network.png")))

        manifestFileRead = utils.readJson(os.path.join(os.getcwd(), "test_network.json"))
        self.assertIsNotNone(manifestFileRead)

        # TODO : Do some checking on the manifest object here...

        # Clean up
        utils.remove_file(os.path.join(os.getcwd(), "test_network.json"))
        utils.remove_dir(os.path.join(os.getcwd(), "media"))

    def test_web_to_iiif(self):
        web = utils.create_web_from_media(
            "/Users/jacob/Documents/Git Repos/spider-python/Examples/Example-Media",
            "tempFromMedia"
        )

        sp.webToMemoRekall(
            web,
            writePath = os.path.join(os.getcwd(), "testManifestNetwork"),
            path = "http://localhost:9000/data/",
            removePrevious = [True, True],
            copyMedia = True
        )

# Run
if __name__ == "__main__":
    unittest.main()