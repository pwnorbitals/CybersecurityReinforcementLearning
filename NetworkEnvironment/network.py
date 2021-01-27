import random
import time
import uuid
import networkx as nx
import matplotlib.pyplot as plt

random.seed(time.time)

def fromYedGraphML(path):
    res = nx.read_graphml(path)
    if res is None:
        raise "Couldn't load yEd GraphML file"
    print("Loaded nodes : ", len(res.nodes))
    return CyberNetwork(res)

# https://docs.bokeh.org/en/latest/docs/user_guide/graph.html
# https://networkx.org/documentation/stable/tutorial.html
class CyberNetwork:
    def __init__(self, *islands : nx.Graph):
        self.islands = islands  
        if len(islands) > 1:
            self.joined = nx.compose_all(*islands)
        else:
            self.joined = islands[0]
    

    def insertNode(self, left, right):
        # not between two nodes of an island
        pass

    def removeNode(self, node):
        # not a node from an island
        pass

    def insertLink(self, left, right):
        # not between two nodes of an island
        pass

    def removeLink(self, left, right):
        # not between two nodes of an island
        pass

    def pwnCount(self):
        pass

    def countNodes(self):
        pass

    def display(self):
        nx.draw(self.joined, with_labels=True, font_weight='bold')
        plt.show()

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
            


class CyberNode:
    def __init__(self, defValue, detectionValue, maxVectors = 10):
        self.defValue = defValue
        self.detectionValue = detectionValue
        self.atqVectors = [random.randint(0, maxDefValue) for i in range(random.randint(0, maxVectors))]

    def getLinked(self, network):
        return network.getNodes(self.links)

    def changeDetectionValue(self):
        pass

    def changeDefenseValue(self):
        pass

    def isPwned(self):
        pass

    









