# spider-python
Python version of spider.

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
        web.addEdge({"relation" : {"source" : str(nodeList[i].uuid), "target" : str(nodeList[i + 1].uuid)}})
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
import networkx as nx
import matplotlib.pyplot as plt

network = web.convertToNetwork(
    nodeList = nodeCollection,
    edgeList = edgeCollection
)

pos = nx.spring_layout(network, seed=3068)
nx.draw(network, pos=pos, with_labels=True)
plt.show()

# Convert to a MemoRekall manifest network:
web.convertToMemoRekall(
    nodeList = nodeCollection,
    edgeList = edgeCollection,
    **settings
)
```