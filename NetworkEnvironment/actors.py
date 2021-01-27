class CyberAttacker():
    def __init__(self):
        self.score = 0

    def act(self, gameState):
        pass

class CyberDefender():
    def __init__(self):
        self.score = 0
        pass

    def act(self, gameState):
        pass

class HumanDefender(CyberDefender):
    def act(self, gameState):
        print("The current game state is :")
        self.showState(gameState)
        print("Choose an action : ")
        print(" 1 - Improve detection for a node")
        print(" 2 - Improve defense for an attack vector")
        print(" 3 - Insert a node")
        print(" 4 - End modificationss")
        action = int(input())
        calls = {1: self.improveDetection, 2: self.improveDefense, 3: self.insertNode, 4: gameState.endTurn}
        calls[action](gameState)

    def improveDetection(self, gameState):
        print("Choose a node :")
        nodeId = str(input())
        node = gameState.getNode(nodeId)
        print("Current detection value is " + node.detectionValue + ".")
        print("Choose how much to increase : ")
        increment = int(input())
        gameState.reinforceDetection(node)


    def improveDefense(self):
        print("Choose a node :")
        nodeId = str(input())
        node = gameState.getNode(nodeId)
        print("Current defense values are " + node.defenseValues + ".")
        print("Choose the defense value to increase : ")
        value = int(input())
        print("Choose how much to increase : ")
        increment = int(input())
        gameState.reinforceDefense(node, value, increment)

    def insertNode(self):
        print("choose a first node :")
        print("choose a second node :")
        # defensive value is zero
        print("choose the detection value :")
        print("The new node has X attack vectors")
        print("choose the defense values :")

class HumanAttacker(CyberAttacker):
    def act(self, gameState):
        print("The current game state is :")
        print(gameState)
        print("Choose a node to attack :")
        print("Choose an attack vector :")

    def showState(self, state):
        print(gameState)

class RandomAttacker(CyberAttacker):
    pass

class RandomDefender(CyberDefender):
    pass