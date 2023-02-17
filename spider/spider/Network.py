import networkx as nx

def webToNetworkX(web, **kwargs):
    G = nx.Graph()
    
    nodeList = kwargs.get('nodeList', web.getFullList("nodes"))
    edgeList = kwargs.get('edgeList', web.getFullList("edges"))

    if isinstance(nodeList, list) == False:
        nodeList = nodeList.contentToList()
    if isinstance(edgeList, list) == False:
        edgeList = edgeList.contentToList()

    relabelMap = {}

    for nodeUUIDString in nodeList:
        node = web.loadNode(nodeUUIDString)
        relabelMap[nodeUUIDString] = node.title
        G.add_node(str(node.uuid))

    for edgeUUIDString in edgeList:
        edge = web.loadEdge(edgeUUIDString)
        G.add_edge(edge.relation.source, edge.relation.target)

    G = nx.relabel_nodes(G, relabelMap)

    return G