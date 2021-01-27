from . import network
import random

class CyberGameSettings:
    def __init__(self):
        self.defUnitPunition = 1
        self.nodePwnThreshold = 0.25
        self.attackCost = 10
        self.maxAtqPower = 10
        self.wrongEndTurnPunition = 10
        self.wrongGraphActionPunition = 10
        self.insertNodePunition = 10
        self.removeNodePunition = -10
        self.insertLinkPunition = 10
        self.removeLinkPunition = -10
        self.inspectGameFrequencyAtq = 1 # %
        self.inspectGameFrequencyDef = 1 # %

class CyberGame:
    def __init__(self, attacker, defender, network, settings=CyberGameSettings()):
        self.network = network
        self.attacker = attacker
        self.defender = defender
        self.stepHooks = []
        self.endHooks = []

        self.settings = settings
        self.state = CyberGameState(self) 

    def getAttackState(self):
        return AttackerGameState(self)

    def getDefenseState(self):
        return DefenderGameState(self)

    def gameEnd(self):
        self.defender.score -= self.settings.defUnitPunition * self.state.elapsedTime
        self.state.gameOverRecorded = True
        for hook in self.endHooks:
            hook()

    def isGameOver(self):
        return \
            self.network.totalPwnValue() / self.network.totalValue() \
            >= \
            self.settings.nodePwnThreshold \
                or \
            self.state.attackDetected == True

    def defenseStep(self):
        action = self.defender.act(self.getDefenseState())
        self.registerDefense(action)
        if random.randrange(100) < self.settings.inspectGameFrequencyDef:
            self.network.display()
            print(self.network.isPlayable())
        

    def attackStep(self):
        action = self.attacker.act(self.getAttackState())
        self.registerAttack(action)
        self.state.elapsedTime += 1
        if random.randrange(100) < self.settings.inspectGameFrequencyAtq:
            self.network.display()

    def addStepHook(self, hook):
        self.stepHooks.append(hook)

    def addEndHook(self, hook):
        self.endHooks.append(hook)

    def run(self):
        while not self.state.defenderIsDone:
            self.defenseStep()
        while not self.isGameOver() :
            self.attackStep()
            for hook in self.stepHooks:
                hook(self.state)
        self.gameEnd()
        return self.state



    def registerAttack(self, action):
        print("Received action", action["type"])
        if action["type"] == "attack":
            attackedNode = self.network.findNodeFromAttacker(action["target"])
            if attackedNode.defense[action["vector"]] > attackedNode.atqVectors[action["vector"]]:
                attackedNode.isPwned = True
                if random.randrange(100) < attackedNode.defense[action["vector"]]:
                    self.state.attackDetected = True
            else:
                attackedNode.atqVectors[action["vector"]] += random.randint(0, self.settings.maxAtqPower)
            self.attacker.score -= self.settings.attackCost
            

        else:
            raise RuntimeError("No such action " + action["type"] + " !")

    def registerDefense(self, action):
        print("Received action", action["type"])

        try:
            if action["type"] == "changeDefense":
                target = self.network.findNodeFromDefender(action["target"])

                old_value = target.defense[action["vector"]]
                new_value = action["value"] 

                punition_fct = lambda x : 1/(1-1/(x/100)) if x != 0 else 0
                punition = punition_fct(new_value) - punition_fct(old_value)

                target.defense[action["vector"]] = action["value"] 
                self.defender.score -= punition

            elif action["type"] == "changeDetection":
                target = self.network.findNodeFromDefender(action["target"])

                old_value = target.detection
                new_value = action["value"] 

                punition_fct = lambda x : 1/(1-1/(x/100)) if x != 0 else 0
                punition = punition_fct(new_value) - punition_fct(old_value)

                target.detection = action["value"] 
                self.defender.score -= punition

            elif action["type"] == "insertNode":
                self.network.insertNode(\
                    self.network.findNodeFromDefender(action["left"]),\
                    self.network.findNodeFromDefender(action["right"]))
                self.defender.score -= self.settings.insertNodePunition

            elif action["type"] == "removeNode": 
                self.network.removeNode(self.network.findNodeFromDefender(action["target"]))
                self.defender.score -= self.settings.removeNodePunition

            elif action["type"] == "endTurn":
                if self.network.isPlayable():
                    self.state.defenderIsDone = True
                else:
                    self.defender.score -= self.settings.wrongEndTurnPunition

            elif action["type"] == "insertLink":
                self.network.insertLink(\
                    self.network.findNodeFromDefender(action["left"]),\
                    self.network.findNodeFromDefender(action["right"]))
                self.defender.score -= self.settings.insertLinkPunition

            elif action["type"] == "removeLink":
                self.network.removeLink(\
                    self.network.findNodeFromDefender(action["left"]),\
                    self.network.findNodeFromDefender(action["right"]))
                self.defender.score -= self.settings.removeLinkPunition
            
            else:
                raise RuntimeError("No such action " + action["type"] + " !")
        except network.GraphError as e:
            self.defender.score -= self.settings.wrongGraphActionPunition


class CyberGameState:
    def __init__(self, game):
        self.elapsedTime = 0
        self.gameOverRecorded = False
        self.network = game.network
        self.attackDetected = False
        self.defenderIsDone = False


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
    def __init__(self, game):
        self.nodes = [network.NodeForDefender(node) for node in game.network.nodes()] 

        self.links = []
        for link in game.network.links():
            first = next(node for node in self.nodes if id(link[0]) == node.nid)  
            second = next(node for node in self.nodes if id(link[1]) == node.nid)
            self.links.append((first, second))  

    def changeDefense(self, node, vector, value):
        return {"type": "changeDefense", "target": node, "vector": vector, "value": value}

    def changeDetection(self, node, value):
        return {"type": "changeDetection", "target": node, "value": value}

    def insertNode(self, left, right):
        return {"type": "insertNode", "left": left, "right": right}

    def removeNode(self, node):
        return {"type": "removeNode", "target": node}

    def insertLink(self, left, right):
        return {"type": "insertLink", "left": left, "right": right}

    def removeLink(self, left, right):
        return {"type": "removeLink", "left": left, "right": right}

    def endTurn(self):
        return {"type": "endTurn"}