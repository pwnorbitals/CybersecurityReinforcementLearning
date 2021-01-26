import random
import time
import uuid

random.seed(time.time)

def genUUID():
    return uuid.uuid4()

# https://docs.bokeh.org/en/latest/docs/user_guide/graph.html
class CyberNetwork:
    def __init__(self, NodeList, LinkList):
        self.nodes = NodeList
        self.links = LinkList

    def getNodes(self, UUIDlist):
        return filter(lambda node : node.uuid in UUIDlist, self.nodes)

    def insertNode(self, left, right):
        pass

    def removeNode(self, node):
        # ok if not in initialNodes
        pass

    def pwnCount(self):
        pass

    def countNodes(self):
        pass

class CyberNode:
    def __init__(self, atqValue, defValue, maxVectors = 10):
        self.links = []
        self.uuid = genUUID()
        self.defValue = defValue
        self.atqVectors = [random.randint(0, maxVectors)

    def addLink(self, uuid):
        self.links.append(uuid)

    def removeLink(self, uuid):
        self.links.remove(uuid)

    def getLinked(self, network):
        return network.getNodes(self.links)









