import random
import time
import uuid
import networkx as nx
import copy
import matplotlib.pyplot as plt

random.seed(time.time)

def fromYedGraphML(path):
    res = nx.read_graphml(path)
    if res is None:
        raise "Couldn't load yEd GraphML file"
    net = nx.Graph(res)

    labelmapping = {n[0] : CyberNode(int(n[1]["label"]), True if n[1]["description"] == "entry" else False) \
        for n in net.nodes(data=True)} 
    newnet = nx.relabel_nodes(net, labelmapping)

    print("Loaded nodes : ", len(newnet.nodes()))

    #for n in net.nodes(data=True):
    #    n[1] = CyberNode(n[1]["description"], True if n[1]["label"] == "entry" else False)

    return CyberNetwork(newnet)

class GraphError(Exception):
    pass

class CyberNode:
    def __init__(self, value, isEntry, maxVectors = 10):
        self.detection = 0
        self.atqVectors = [0] * random.randint(1, maxVectors)
        self.defense = [0] * len(self.atqVectors)
        self.value = value
        self.isPwned = False
        self.isEntry = isEntry

    def changeDetectionValue(self, newValue):
        # to setter
        pass

    def changeDefenseValue(self, newValue):
        # to setter
        pass

class NodeForAttacker:
    def __init__(self, node):
        self.atqVectors = node.atqVectors
        self.nid = id(node)

class NodeForDefender:
    def __init__(self, node):
        self.detection = node.detection
        self.defense = node.defense
        self.value = node.value
        self.isPwned = node.isPwned
        self.isEntry = node.isEntry
        self.nid = id(node)

# https://networkx.org/documentation/stable/
class CyberNetwork:
    def __init__(self, *islands : nx.Graph):
        self.islands = islands  
        if len(islands) > 1:
            self.joined = nx.compose_all(*islands)
        else:
            self.joined = islands[0]
        self.current = self.joined
    

    def insertNode(self, left, right):
        # not between two nodes of an island
        if left in self.joined and right in self.joined and left in self.joined.neighbors(right):
            raise GraphError("Cannot insert a node between two nodes of the same original islands")
        if self.current.has_edge(left, right):
            self.current.remove_edge(left, right)
        newnode = CyberNode(0, False)
        self.current.add_node(newnode)
        self.current.add_edge(left, newnode)
        self.current.add_edge(newnode, right)

    def removeNode(self, node):
        # not a node from an island
        if node in self.joined:
            raise GraphError("Cannot remove an original node")
        self.current.remove_node(node)

    def insertLink(self, left, right):
        # not between two nodes of the same island
        if left in self.joined and right in self.joined and left in self.joined.neighbors(right):
            raise GraphError("Cannot insert a link between two nodes of the same original islands")
        self.current.add_edge(left, right)

    def removeLink(self, left, right):
        # not between two nodes of the same island
        if left in self.joined and right in self.joined and left in self.joined.neighbors(right):
            raise GraphError("Cannot remove a link between two nodes of the same original islands")
            return
        if self.current.has_edge(left, right):
            self.current.remove_edge(left, right)
        else:  
            raise GraphError("Trying to remove an edge where none exist !")

    def display(self):
        nx.draw(self.current, with_labels=False, font_weight='bold')
        plt.show()

    def totalPwnValue(self):
        return sum(map(lambda node : node.value if node.isPwned else 0, self.current.nodes))

    def totalValue(self):
        return sum(map(lambda node : node.value, self.current.nodes))

    def nodes(self):
        return [n for n in self.current.nodes()]

    def links(self):
        return [(u, v) for u,v in self.current.edges()]

    def isPlayable(self):
        # must have no islands, at least 1 entry node, at least 1 defensive value
        islandCount = nx.number_connected_components(self.current)
        if islandCount != 1:  # quick check before looping on nodes if it's not needed
            return False

        entryCount = 0
        totalValue = 0
        for node in self.nodes():
            if node.isEntry:
                entryCount += 1
            totalValue += node.value
            
        return \
            islandCount == 1 and \
            entryCount > 0 and \
            totalValue > 0

    def nodeHasNeighbour(self, condition):
        return [n if condition(n) else None for n in self.nodes()]
            
    def findNodeFromAttacker(self, node):
        return next(n for n in self.current.nodes() if id(n) == node.nid)

    def findNodeFromDefender(self, node):
        return next(n for n in self.current.nodes() if id(n) == node.nid)











