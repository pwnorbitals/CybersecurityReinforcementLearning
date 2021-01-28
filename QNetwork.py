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

    def Q(self, state):
        # return all the action-value for a possible state
        return QMatrix[state,:]  # QMatrix need to be defined :) 

    
    def setValue(self, state, action):

    def act(self, gameState):
        # gameState has nodes, links, timeElapsed
        # self has score
        action = self.get_action(gameState)



        print(self.score)



        pass

    def get_bestValue(self, state):
        numberOfActions = len(state.actions)
        bestValue = np.max(self.Q(state))
        return BestValue

    def get_bestAction(self, state): 
        numberOfActions = len(state.actions)
        bestAction = np.argmax(self.S(state))
        return bestAction

    def get_action(self, state):
        probabilityChoice = random.random()
        if probabilityChoice <= self.epsilon :
            chosen_action = random.choice(len(self.Q(state)))
        else : 
            chosen_action = self.get_bestAction(state)


    def update(self, state, action, reward, next_state):
        QOld = self.get_bestValue(state)
        Q = (1 - alpha) * QOld + alpha * (reward + gamma *self.get_bestValue(next_state) )
        self.Q(state)[action] = Q 
    

attacker = actors.RandomAttacker()
defender = QDefender(alpha=0.5, epsilon=0.3, gamma=0.7)

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

