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
    print("Loaded nodes : ", len(net.nodes))

    labelmapping = {n[0] :(n[0], CyberNode(int(n[1]["description"]), True if n[1]["label"] == "entry" else False)) \
        for n in net.nodes(data=True)} 
    newnet = nx.relabel_nodes(net, labelmapping)

    #for n in net.nodes(data=True):
    #    n[1] = CyberNode(n[1]["description"], True if n[1]["label"] == "entry" else False)

    return CyberNetwork(newnet)


class CyberNode:
    def __init__(self, defValue, isEntry, maxVectors = 10):
        self.defValue = defValue
        self.detectionValue = 0
        self.atqVectors = [0] * random.randint(0, maxVectors)
        self.isPwned = False
        self.isEntry = isEntry

    def changeDetectionValue(self, newValue):
        # to setter
        pass

    def changeDefenseValue(self, newValue):
        # to setter
        pass


# https://networkx.org/documentation/stable/tutorial.html
class CyberNetwork:
    def __init__(self, *islands : nx.Graph):
        self.islands = islands  
        if len(islands) > 1:
            self.joined = nx.compose_all(*islands)
        else:
            self.joined = islands[0]
        self.current = self.joined
    

    def insertNode(self, left, right, node : CyberNode):
        # not between two nodes of an island
        if left in joined and right in joined:
            raise "Cannot insert a node between two nodes of the original islands"
        self.current.remove_edge(left, right)
        newnode = self.current.add_node(node)
        self.current.add_edge(left, newnode)
        self.current.add_edge(newnode, right)

    def removeNode(self, node):
        # not a node from an island
        if node in joined:
            raise "Cannot remove an original node"
        self.current.remove_node(node)

    def insertLink(self, left, right):
        # not between two nodes of an island
        if left in joined and right in joined:
            raise "Cannot insert a link between two nodes of the original islands"
        self.current.add_edge(left, right)

    def removeLink(self, left, right):
        # not between two nodes of an island
        if left in joined and right in joined:
            raise "Cannot remove a link between two nodes of the original islands"
        self.current.remove_edge(left, right)
        pass

    def display(self):
        nx.draw(self.joined, with_labels=True, font_weight='bold')
        plt.show()

    def totalPwnValue(self):
        pwnValue = lambda node : node.defValue if node.isPwned else 0
        print([n[1].defValue for n in self.current.nodes])
        return sum(map(pwnValue, [n[1] for n in self.current.nodes]))

    def totalValue(self):
        return sum(map(lambda node : node[1].defValue, self.current.nodes))

    def isPlayable(self):
        # must have no islands, at least 1 entry node, at least 1 defensive value
        islandCount = nx.number_connected_components(self.joined)
        if islandCount != 1:  # quick check before looping on nodes if it's not needed
            return False

        entryCount = 0
        totalDef = 0
        for node, data in self.joined.nodes(data=True):
            if data.isEntry:
                entryCount += 1
            if data.defense:
                totalDef += data.defense

        return \
            islandCount == 1 and \
            entryCount > 0 and \
            totalDef > 0
            













