import unittest
import spider as sp
import os
import shutil

class TestWeb(unittest.TestCase):
    def setUp(self):
        # Delete if already exists:
        self.remove_web("temp")
        self.remove_web("temp2")

    def tearDown(self):
        # Delete if exists:
        self.remove_web("temp")
        self.remove_web("temp2")

    def test_web_duplicate(self):
        # Create web:
        metadata = {
            "path" : os.path.join(os.getcwd(), "temp"),
            "title" : "test"
        }
        myWeb = sp.createWeb(metadata)

        myWeb.addNode({"title" : "node 1"})
        node2 = myWeb.addNode({"title" : "node 2"})
        myWeb.addNode({"title" : "node 3"})
        node2.addNode({"title" : "nested node single"})
        nestedNode2 = node2.addNode({"title" : "nested nested top"})
        nestedNode2.addNode({"title" : "nested nested bottom"})

        duplicated = myWeb.duplicate(os.path.join(os.getcwd(), "temp2"))
        self.assertIsNotNone(duplicated)
        self.assertNotEqual(myWeb.uuid, duplicated.uuid)
        self.check_direc_file_lists(
            os.getcwd(),
            ["temp2", "temp2/media", "temp2/web", "temp2/web/nodes", "temp2/web/edges", 
                "temp2/web/node_collections", "temp2/web/edge_collections"],
            ["temp2/metadata.json", "temp2/.gitignore"]
        )
        self.assertEqual(myWeb.title, duplicated.title)

        duplicatedNodeList = duplicated.getFullList("nodes", False)

        for node in duplicatedNodeList:
            loaded = duplicated.loadNode(node)
            self.assertTrue(loaded.title in [{'en': 'node 1'}, {'en': 'node 2'}, {'en': 'node 3'}])
            if loaded.title == {'en': 'node 2'}:
                nestedList = loaded.getFullList(False)
                for nested in nestedList:
                    loadedNested = duplicated.loadNode(nested)
                    self.assertTrue(loadedNested.title in [{'en': 'nested node single'}, {'en': 'nested nested top'}])
                    if loadedNested.title == {'en': 'nested nested top'}:
                        nestedNestedList = loadedNested.getFullList(False)
                        self.assertEqual(duplicated.loadNode(nestedNestedList[0]).title, {'en': 'nested nested bottom'})

    def test_node_duplicate(self):
        # Create web:
        myWeb = sp.createWeb({"path" : os.path.join(os.getcwd(), "temp")})
        originalNode = myWeb.addNode({"title" : "node 1"})
        duplicatedNode = myWeb.duplicateNode(originalNode.uuid)
        
        self.assertEqual(originalNode.title, duplicatedNode.title)
        self.assertNotEqual(originalNode.uuid, duplicatedNode.uuid)

        topLevelNode = myWeb.addNode({"title" : "Top level"})
        toBeDuplicated = myWeb.addNode({"title" : "Will be nested"})
        toBeDuplicated.addNode({"title" : "nested nested"})
        topLevelNode.duplicateNode(toBeDuplicated)

        for item in topLevelNode.getFullList():
            self.assertTrue(myWeb.loadNode(item).title in [{"en" : "Will be nested"}, {"en" : "nested nested"}])

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