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
        # Test web:
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

        # Test nodes
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
        self.remove_web("temp")
        self.remove_web("temp2")

        # Test edges
        metadata = {"path" : os.path.join(os.getcwd(), "temp")}
        myWeb = sp.createWeb(metadata)
        node1 = myWeb.addNode({"title" : "source"})
        node2 = myWeb.addNode({"title" : "target"})
        testEdge = myWeb.addEdge({
            "title" : "test edge",
            "relation" : {
                "source" : node1.uuid,
                "target" : node2.uuid
            }
        })

        duplicated = myWeb.duplicate(os.path.join(os.getcwd(), "temp2"))
        duplicatedEdgeList = duplicated.getFullList("edges")
        duplicatedEdge = duplicated.loadEdge(duplicatedEdgeList[0])
        
        self.assertNotEqual(testEdge.uuid, duplicatedEdge.uuid)
        self.assertEqual(testEdge.title, duplicatedEdge.title)
        self.assertNotEqual(testEdge.relation.source, duplicatedEdge.relation.source)
        self.assertNotEqual(testEdge.relation.target, duplicatedEdge.relation.target)
        self.assertEqual(myWeb.loadNode(testEdge.relation.source).title, duplicated.loadNode(duplicatedEdge.relation.source).title)
        self.assertEqual(myWeb.loadNode(testEdge.relation.target).title, duplicated.loadNode(duplicatedEdge.relation.target).title)

        self.remove_web("temp")
        self.remove_web("temp2")

        # Test collections:
        myWeb = sp.createWeb({"path" : os.path.join(os.getcwd(), "temp")})
        nodeList = []
        edgeList = []
        for i in range(10):
            nodeList.append(myWeb.addNode({"title" : "node" + str(i)}).uuid)
        for i in range(9):
            edgeList.append(myWeb.addEdge({"title" : "edge" + str(i), "relation" : {"source" : nodeList[i], "target" : nodeList[i + 1]}}).uuid)
        nodeCollection = myWeb.addCollection("node", {"title" : "node collection"})
        nodeCollection.addContent(nodeList)
        edgeCollection = myWeb.addCollection("edge", {"title" : "edge collection"})
        edgeCollection.addContent(edgeList)
        duplicatedWeb = myWeb.duplicate(os.path.join(os.getcwd(), "temp2"))

        duplicatedNodeCollection = duplicatedWeb.loadCollection(duplicatedWeb.getFullList("node_collections")[0])
        duplicatedEdgeCollection = duplicatedWeb.loadCollection(duplicatedWeb.getFullList("edge_collections")[0])

        self.assertNotEqual(nodeCollection.uuid, duplicatedNodeCollection.uuid)
        self.assertEqual(nodeCollection.title, duplicatedNodeCollection.title)
        self.assertNotEqual(edgeCollection.uuid, duplicatedEdgeCollection.uuid)
        self.assertEqual(edgeCollection.title, duplicatedEdgeCollection.title)

    # PROBLEM
        for item in duplicatedNodeCollection.contentToList():
            self.assertFalse(item in nodeList)
            wasFound = False
            thisNode = duplicatedWeb.loadNode(item)
            for oldNode in nodeList:
                oldNodeLoaded = myWeb.loadNode(oldNode)
                if oldNodeLoaded.title == thisNode.title:
                    wasFound = True
            self.assertTrue(wasFound)

        for item in duplicatedEdgeCollection.contentToList():
            self.assertFalse(item in edgeList)
            wasFound = False
            thisEdge = duplicatedWeb.loadEdge(item)
            for oldEdge in edgeList:
                oldEdgeLoaded = myWeb.loadNode(oldEdge)
                if oldEdgeLoaded.title == thisEdge.title:
                    wasFound = True
            self.assertTrue(wasFound)


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

    def test_edge_duplicate(self):
        myWeb = sp.createWeb({"path" : os.path.join(os.getcwd(), "temp")})
        srcNode = myWeb.addNode({"title" : "src"})
        tarNode = myWeb.addNode({"title" : "tar"})
        origEdge = myWeb.addEdge({"title" : "original edge", "relation" : {"source" : srcNode.uuid, "target" : tarNode.uuid}})

        duplicatedEdge = myWeb.duplicateEdge(origEdge.uuid, update_nodes = False, node_id_map = {})
        duplicatedEdge2 = myWeb.duplicateEdge(origEdge.uuid, update_nodes = True, node_id_map = {srcNode.uuid : "foo", tarNode.uuid : "bar"})

        self.assertNotEqual(origEdge.uuid, duplicatedEdge.uuid)
        self.assertNotEqual(origEdge.uuid, duplicatedEdge2.uuid)

        self.assertEqual(origEdge.title, duplicatedEdge.title)
        self.assertEqual(origEdge.title, duplicatedEdge2.title)

        self.assertEqual(origEdge.relation.source, duplicatedEdge.relation.source)
        self.assertEqual(origEdge.relation.target, duplicatedEdge.relation.target)
        self.assertEqual(duplicatedEdge2.relation.source, "foo")
        self.assertEqual(duplicatedEdge2.relation.target, "bar")

    def test_collection_duplicate(self):
        # Test collections:
        myWeb = sp.createWeb({"path" : os.path.join(os.getcwd(), "temp")})
        nodeList = []
        edgeList = []
        for i in range(10):
            nodeList.append(myWeb.addNode({"title" : "node" + str(i)}).uuid)
        for i in range(9):
            edgeList.append(myWeb.addEdge({"title" : "edge" + str(i), "relation" : {"source" : nodeList[i], "target" : nodeList[i + 1]}}).uuid)
        nodeCollection = myWeb.addCollection("node", {"title" : "node collection"})
        nodeCollection.addContent(nodeList)
        edgeCollection = myWeb.addCollection("edge", {"title" : "edge collection"})
        edgeCollection.addContent(edgeList)

        duplicatedNodeCollection = myWeb.duplicateCollection(nodeCollection.uuid)
        duplicatedEdgeCollection = myWeb.duplicateCollection(edgeCollection.uuid)

        self.assertNotEqual(nodeCollection.uuid, duplicatedNodeCollection.uuid)
        self.assertEqual(nodeCollection.title, duplicatedNodeCollection.title)
        self.assertNotEqual(edgeCollection.uuid, duplicatedEdgeCollection.uuid)
        self.assertEqual(edgeCollection.title, duplicatedEdgeCollection.title)

        #print("NODE COLLECTION LENGTH")
        #print(duplicatedNodeCollection.contentToList())
        for item in duplicatedNodeCollection.contentToList():
            self.assertFalse(item in nodeList)
            wasFound = False
            thisNode = myWeb.loadNode(item)
            for oldNode in nodeList:
                oldNodeLoaded = myWeb.loadNode(oldNode)
                if oldNodeLoaded.title == thisNode.title:
                    wasFound = True
            self.assertTrue(wasFound)

        for item in duplicatedEdgeCollection.contentToList():
            self.assertFalse(item in edgeList)
            wasFound = False
            thisEdge = myWeb.loadEdge(item)
            for oldEdge in edgeList:
                oldEdgeLoaded = myWeb.loadNode(oldEdge)
                if oldEdgeLoaded.title == thisEdge.title:
                    wasFound = True
            self.assertTrue(wasFound)

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