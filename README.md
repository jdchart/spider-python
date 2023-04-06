# spider-python
Spider is primarily used to make network structures of elements that have temporal dimensions.

_Note that this is still actively in development, give me a minute :)_

1. [Examples](/Examples/)
2. [Running](/docs/Running.md)
3. [Metadata Fields](/docs/Metatdata-Fields.md)
4. [Roadmap and To-Do](/docs/Roadmap-ToDo-Issues.md)

## Usage

A brief introduction on how to use `spider`. For more detailed examples, see the [Examples](/Examples/) folder.

### Creating and loading elements

```python
import spider as sp

# Web:
web = sp.createWeb({"title" : "My Web"})

# Nodes:
nodeList = []
for i in range(10):
    nodeList.append(
        web.addNode({"title" : "Node " + str(i)})
    )

# Edges:
edgeList = []
for i in range(9):
    edgeList.append(
        web.addEdge({"relation" : {"source" : nodeList[i].uuid, "target" : nodeList[i + 1].uuid}})
    )

# Collections:
nodeCollection = web.addCollection("node", {"title" : "My node collection"})
nodeCollection.addContent(nodeList)
edgeCollection = web.addCollection("edge", {"title" : "My edge collection"})
edgeCollection.addContent(edgeList)
```

### Media conversion:

```python
fileList = utils.collectFiles("/my/media/folder")

for item in fileList:
    web.mediaToNode(item, True)
```

### Visualization:

```python
# As a networkx network:
network = web.convertToNetwork(
    nodeList = nodeCollection,
    edgeList = edgeCollection
)

network.display()

# Convert to a MemoRekall manifest network:
web.convertToMemoRekall(
    nodeList = nodeCollection,
    edgeList = edgeCollection,
    **settings
)
```