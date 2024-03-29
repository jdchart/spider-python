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

    def test_network(self):
        # Create web:
        myWeb = utils.create_basic_web("temp", "test network", 10)

        net = sp.webToNetworkx(myWeb)
        self.assertIsNotNone(net)

# Run
if __name__ == "__main__":
    unittest.main()