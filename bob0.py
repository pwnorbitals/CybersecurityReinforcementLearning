from NetworkEnvironment import game, actors, network
import numpy

def maybeInspectState(state):
    pass

def maybeInspectActor(actor):
    pass

def maybeInspectResults(result):
    print(results.elapsedTime)
    pass

attacker = actors.RandomAttacker()
defender = actors.RandomDefender()

net = network.fromYedGraphML("./entry.graphml")
# net.display()

nbGames = 0
last10times = []
timeThreshold = 1500
gamesThreshold = 1000
while nbGames < gamesThreshold or np.mean(last10times) < timeThreshold :
    print("New game starting ...")
    thisGame = game.CyberGame(attacker, defender, net)
    thisGame.addStepHook(lambda state : maybeInspectState(state))
    results = thisGame.run()
    maybeInspectResults(results)
    if len(last10times) == 10:
        last10times.pop(0)
    last10times.append(results.elapsedTime)
    maybeInspectActor(defender)


