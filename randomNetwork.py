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

attacker = actors.RandomAttacker()
defender = actors.RandomDefender()

net = network.fromYedGraphML("./entry.graphml")
net.display()

nbGames = 0
last10times = []
gameResults = []
timeThreshold = 1500
gamesThreshold = 1000
#while nbGames < gamesThreshold or np.mean(last10times) < timeThreshold :
while nbGames < 200:
    print("New game starting ... ", nbGames)
    thisGame = game.CyberGame(attacker, defender, copy.deepcopy(net))
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

