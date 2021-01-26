import network

class CyberGame:
    def __init__(self, network, attacker, defender, settings={}):
        self.baseNetwork = network
        self.attacker = attacker
        self.defender = defender
        self.stepHooks = []
        self.endHooks = []

        defaultSettings = {defUnitPunition : 1}
        self.settings = settings if settings else defaultSettings
        self.state = {elapsedTime : 0, gameOverRecorded: false, network: network}

    def getState(self):
        return self.state

    def getAttackState():
        return AttackerGameState(self.state)

    def getDefenseState():
        return DefenderGameState(self.state)

    def gameEnd(self):
        self.defender.punish(self.settings.defUnitPunition * self.state.elapsedTime)
        self.state.gameOverRecorded = True
        for hook in self.endHooks:
            hook()

    def isGameOver(self):
        return \
            self.network.totalPwnValue() / self.network.totalValue() \
            >= \
            self.gameSettings.NodePwnThreshold

    def step(self):
        if self.isGameOver():
            if not self.state.gameOverRecorded:
                self.gameEnd()
            else:
                return

        attacker.act(self.getAttackState())

        for hook in self.stepHooks:
            hook()

    def addStepHook(self, hook):
        self.stepHooks.append(hook)

    def addEndHook(self, hook):
        self.endHooks.append(hook)


class CyberGameState:
    def __init__(self, game):
        pass

class AttackerGameState(CyberGameState):
    def __init__(self, gameState):

        # node is visible if is pwned or is neighbour of a pwned node or is entry node
        isNodeVisible = lambda node : node.isPwned() or node.isEntry() or node.hasNeighbour(lambda n : n.isPwned())
        visibleNodes = [node for node in gameState.network.nodes if isNodeVisible(node)] 

        isLinkVisible = lambda link : link.left().isPwned() and link.right().isPwned()
        visibleLinks = [link for link in gameState.network.links if isLinkVisible(link)]



        

    def attack(self, node):
        pass

class DefenderGameState(CyberGameState):
    def __init__(self, gameState):
        pass

    def reinforceDefense(self, node, increment):
        pass

    def reinforceDetection(self, node, increment):
        pass

    def insertNode(self, left, right, stuff, stuff, stuff):
        pass

    def endTurn(self):
        pass