from . import network

class CyberGameSettings:
    def __init__(self, defUnitPunition=1, nodePwnThreshold=0.25):
        self.defUnitPunition = defUnitPunition
        self.nodePwnThreshold = nodePwnThreshold

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
        self.attacker.act(self.getAttackState())

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
        visibleNodes = [node for node in game.network.nodes() if isNodeVisible(node)] 

        isLinkVisible = lambda link : link[0].isPwned and link[1].isPwned
        visibleLinks = [link for link in game.network.links() if isLinkVisible(link)]



        

    def attack(self, node):
        pass

class DefenderGameState(CyberGameState):
    def __init__(self, gameState):
        pass

    def reinforceDefense(self, node, increment):
        pass

    def reinforceDetection(self, node, increment):
        pass

    def insertNode(self, left, right):
        pass

    def endTurn(self):
        pass