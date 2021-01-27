from . import network
import random

class CyberGameSettings:
    def __init__(self):
        self.defUnitPunition = 1
        self.nodePwnThreshold = 0.25
        self.attackCost = 10
        self.maxAtqPower = 10

class CyberGame:
    def __init__(self, attacker, defender, network, settings=CyberGameSettings()):
        self.network = network
        self.attacker = attacker
        self.defender = defender
        self.stepHooks = []
        self.endHooks = []

        self.settings = settings
        self.state = CyberGameState(self) 

    def getState(self):
        return self.state

    def getAttackState(self):
        return AttackerGameState(self)

    def getDefenseState(self):
        return DefenderGameState(self)

    def gameEnd(self):
        self.defender.punish(self.settings.defUnitPunition * self.state.elapsedTime)
        self.state.gameOverRecorded = True
        for hook in self.endHooks:
            hook()

    def isGameOver(self):
        return \
            self.network.totalPwnValue() / self.network.totalValue() \
            >= \
            self.settings.nodePwnThreshold

    def step(self):
        action = self.attacker.act(self.getAttackState())
        self.registerAction(action)

    def addStepHook(self, hook):
        self.stepHooks.append(hook)

    def addEndHook(self, hook):
        self.endHooks.append(hook)

    def run(self):
        while not self.isGameOver() :
            self.step()
            for hook in self.stepHooks:
                hook(self.state)
        self.gameEnd()
        return self.state



    def registerAction(self, action):
        if action["type"] == "attack":
            attackedNode = self.network.findNodeFromAttacker(action["target"])
            if len(attackedNode) != 1:
                raise RuntimeError("Error in finding node from attacker : " + str(len(attackedNode)) + " results")
            attackedNode = attackedNode[0]
            if attackedNode.defense[action["vector"]] > attackedNode.atqVectors[action["vector"]]:
                attackedNode.isPwned = True
            else:
                attackedNode.atqVectors[action["vector"]] += random.randint(0, self.settings.maxAtqPower)
            self.attacker.score -= self.settings.attackCost

        elif action["type"] == "changeDefense":
            pass

        elif action["type"] == "changeDetection":
            pass

        elif action["type"] == "insertNode":
            pass

        elif action["type"] == "removeNode": 
            pass

        else:
            raise "No such action !"


class CyberGameState:
    def __init__(self, game):
        self.elapsedTime = 0
        self.gameOverRecorded = False
        self.network = game.network


class AttackerGameState(CyberGameState):
    def __init__(self, game):
        # node is visible if is pwned or is neighbour of a pwned node or is entry node
        isNodeVisible = \
            lambda node : node.isPwned or \
                          node.isEntry or \
                          game.network.nodeHasNeighbour(lambda n : n.isPwned)
        visibleNodes = [network.NodeForAttacker(node) for node in game.network.nodes() if isNodeVisible(node)] 

        isLinkVisible = lambda link : link[0].isPwned and link[1].isPwned
        visibleLinks = [link for link in game.network.links() if isLinkVisible(link)]

        self.nodes = visibleNodes
        self.links = visibleLinks

    def attack(self, node, vector):
        return {"type": "attack", "target": node, "vector": vector}
        

class DefenderGameState(CyberGameState):
    def __init__(self, gameState):
        pass

    def changeDefense(self, node, vector, value):
        return {"type": "changeDefense", "target": node, "vector": vector, "value": value}

    def changeDetection(self, node, value):
        return {"type": "changeDetection", "target": node, "value": value}

    def insertNode(self, left, right):
        return {"type": "insertNode", "left": left, "right": right}

    def removeNode(self, node):
        return {"type": "removeNode", "target": node}

    def endTurn(self):
        return {"type": "endTurn"}