from NetworkEnvironment import game, actors, network
import numpy
import matplotlib.pyplot as plt
import copy

def maybeInspectState(state):
    pass

def maybeInspectActor(actor):
    pass

def maybeInspectResults(result):
    print("Time spent : ", results.elapsedTime)
    gameResults.append(True if results.attackDetected else False)
    pass

class QGameSettings(CyberGameSettings):
    def __init__(self):
        super().__init__()
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
        self.inspectGameFrequencyAtq = 0 # %
        self.inspectGameFrequencyDef = 0 # %
        self.attackerDetectedPunition = 1000
        self.attackerDetectedReward = 100

class QDefender(actors.CyberDefender, alpha, epsilon, gamma):
    
    def __init__(self):
        super().__init__()
        self.alpha = alpha     # learning rate
        self.epsilon = epsilon # exploration
        self.gamma = gamma     # "discount rate"

    def act(self, gameState):
        # gameState has nodes, links, timeElapsed
        # self has score
        pass

    def get_value(self, state): 
        pass

    def get_bestaction(self, state):
        pass 

    def get_action(self, action):
        pass 

    def uptdate(self, state, action):
        pass 
        

attacker = actors.RandomAttacker()
defender = QDefender()

net = network.fromYedGraphML("./entry.graphml")
net.insertLink(net.nodes()[4], net.nodes()[6])
net.display()

nbGames = 0
last10times = []
gameResults = []
timeThreshold = 1500
gamesThreshold = 1000
#while nbGames < gamesThreshold or np.mean(last10times) < timeThreshold :
while nbGames < 200:
    print("New game starting ... ", nbGames)
    thisGame = game.CyberGame(attacker, defender, copy.deepcopy(net), QGameSettings())
    thisGame.addStepHook(lambda state : maybeInspectState(state))
    results = thisGame.run()
    maybeInspectResults(results)
    if len(last10times) == 10:
        last10times.pop(0)
    last10times.append(results.elapsedTime)
    maybeInspectActor(defender)
    nbGames += 1

window_size = 10
i = 0
moving_averages = []
while i < len(gameResults) - window_size + 1:
    this_window = gameResults[i : i + window_size]
    window_average = sum(this_window) / window_size
    moving_averages.append(window_average)
    i += 1

plt.plot(moving_averages)
plt.show()

