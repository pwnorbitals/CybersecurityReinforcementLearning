db = [
    {}
]

companyTools = [
    {
        "name" : "LittleBrother", 
        "commandLine" : "littleBrother $1", 
        "args" : [["phone", "email", "name", "address", "username"], ]
    },
    {}
]

class OSINTAttacker():
    def __init__(self):
        pass

    def act(self, gameState):
        pass

class OSINTGameSettings:
    def __init__(self):
        self.unitPunition = 1
        self.tools = companyTools

class OSINTGame:
    def __init__(self, attacker, database, settings=OSINTGameSettings()):
        self.attacker = attacker
        self.database = database
        self.stepHooks = []
        self.endHooks = []

        self.settings = settings
        self.state = OSINTGameState(self) 

    def getAttackState(self):
        return AttackerGameState(self)

    def gameEnd(self):
        self.defender.score -= self.settings.defUnitPunition * self.state.elapsedTime
        self.state.gameOverRecorded = True
        for hook in self.endHooks:
            hook()

    def isGameOver(self):
        #print(self.network.totalPwnValue(), self.network.totalValue(), self.settings.nodePwnThreshold, self.state.attackDetected)
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
        print("Defender is done, score : ", self.defender.score)
        #self.network.display()
        #print("Is game already over", self.isGameOver())
        while not self.isGameOver() :
            self.attackStep()
            for hook in self.stepHooks:
                hook(self.state)
        print("Attacker is done, score : ", self.attacker.score)
        self.gameEnd()
        return self.state

    def registerAttack(self, action):
        if action["type"] == "attack":
            attackedNode = self.network.findNodeFromAttacker(action["target"])
            if attackedNode.defense[action["vector"]] > attackedNode.atqVectors[action["vector"]]:
                attackedNode.isPwned = True
                if random.randrange(100) < attackedNode.defense[action["vector"]]:
                    self.state.attackDetected = True
                    self.attacker.score -= self.settings.attackerDetectedPunition
                    self.defender.score += self.settings.attackerDetectedReward
            else:
                attackedNode.atqVectors[action["vector"]] += random.randint(0, self.settings.maxAtqPower)
            self.attacker.score -= self.settings.attackCost
            

        else:
            raise RuntimeError("No such action " + action["type"] + " !")

class OSINTGameState:
    def __init__(self, game):
        self.elapsedTime = 0
        self.gameOverRecorded = False
        self.network = game.network
        self.attackDetected = False
        self.defenderIsDone = False

class AttackerGameState():
    def __init__(self, game):
       pass

    def attack(self, node, vector):
        return {"type": "attack", "target": node, "vector": vector}