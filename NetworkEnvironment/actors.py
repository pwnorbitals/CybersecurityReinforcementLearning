import random
import networkx as nx
import matplotlib.pyplot as plt

class CyberAttacker():
    def __init__(self):
        self.score = 0

    def act(self, gameState):
        pass

    def viewGame(self, gameState):
        pass

class CyberDefender():
    def __init__(self):
        self.score = 0
        pass

    def act(self, gameState):
        pass

    def viewGame(self, gameState):
        pass

class HumanDefender(CyberDefender):
    def act(self, gameState):
        print("The current game state is :")
        self.showState(gameState)
        print("Choose an action : ")
        print(" 1 - Improve detection for a node")
        print(" 2 - Improve defense for an attack vector")
        print(" 3 - Insert a node")
        print(" 4 - End modifications")
        action = int(input())
        calls = {1: self.improveDetection, 2: self.improveDefense, 3: self.insertNode, 4: gameState.endTurn}
        calls[action](gameState)

    def changeDetection(self, gameState):
        print("Choose a node :")
        nodeId = str(input())
        node = gameState.getNode(nodeId)
        print("Current detection value is " + node.detectionValue + ".")
        print("Choose how much to increase : ")
        increment = int(input())
        return gameState.reinforceDetection(node)


    def changeDefense(self):
        print("Choose a node :")
        nodeId = str(input())
        node = gameState.getNode(nodeId)
        print("Current defense values are " + node.defenseValues + ".")
        print("Choose the defense value to increase : ")
        value = int(input())
        print("Choose how much to increase : ")
        increment = int(input())
        return gameState.reinforceDefense(node, value, increment)

    def insertNode(self):
        print("choose a first node :")
        print("choose a second node :")
        # defensive value is zero
        print("choose the detection value :")
        print("The new node has X attack vectors")
        print("choose the defense values :")

        return 
    
    def showState(self, state):
        graph = nx.Graph()
        for node in state.nodes:
            graph.add_node(node)
        for link in state.links:
            graph.add_edge(link[0], link[1])
        nx.draw(graph, font_weight='bold')
        plt.show()

class HumanAttacker(CyberAttacker):
    def act(self, gameState):
        print("The current game state is :")
        print(gameState)
        print("Choose a node to attack :")
        print("Choose an attack vector :")

    def showState(self, state):
        print(vars(state))
        

class RandomAttacker(CyberAttacker):
    def act(self, gameState):
        target = random.randint(0, len(gameState.nodes)-1)
        if len(gameState.nodes[target].atqVectors)-1 < 0 :
            raise RuntimeError("This should never happen. The bug was fixed... !")
        vector = random.randint(0, len(gameState.nodes[target].atqVectors)-1)
        return gameState.attack(gameState.nodes[target], vector)

class RandomDefender(CyberDefender):
    def act(self, gameState):
        calls = {0: self.changeDefense, 1: self.changeDetection, 2: self.insertNode, 3: self.removeNode, 4: self.insertLink, 5: self.removeLink, 6: self.endTurn}
        action = random.randint(0, len(calls.keys())-1)
        return calls[action](gameState)

    def changeDefense(self, gameState):
        target = random.randint(0, len(gameState.nodes)-1)
        vector = random.randint(0, len(gameState.nodes[target].defense)-1)
        value = random.random() * 100
        return gameState.changeDefense(gameState.nodes[target], vector, value)

    def changeDetection(self, gameState):
        target = random.randint(0, len(gameState.nodes)-1)
        value = random.random() * 100
        return gameState.changeDetection(gameState.nodes[target], value)

    def insertNode(self, gameState):
        while True:
            left = random.randint(0, len(gameState.nodes)-1)
            right = random.randint(0, len(gameState.nodes)-1)
            if left != right:
                break
        return gameState.insertNode(gameState.nodes[left], gameState.nodes[right])


    def removeNode(self, gameState):
        target = random.randint(0, len(gameState.nodes)-1)
        return gameState.removeNode(gameState.nodes[target])

    def insertLink(self, gameState):
        while True:
            left = random.randint(0, len(gameState.nodes)-1)
            right = random.randint(0, len(gameState.nodes)-1)
            if left != right:
                break
        return gameState.insertLink(gameState.nodes[left], gameState.nodes[right])

    def removeLink(self, gameState):
        while True:
            left = random.randint(0, len(gameState.nodes)-1)
            right = random.randint(0, len(gameState.nodes)-1)
            if left != right:
                break
        return gameState.removeLink(gameState.nodes[left], gameState.nodes[right])

    def endTurn(self, gameState):
        return gameState.endTurn()