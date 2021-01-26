from NetworkEnvironment import game, actors, network

def MaybeInspectState(state):
    pass

def MaybeInspectActor(actor):
    pass

attacker = actors.randomAttacker()
defender = actors.humanDefender()

while defender.isNotTrainedEnough():
    thisGame = game.cyberGame(attacker, defender)
    thisGame.addStepHook(lambda state : maybeInspectState(state))
    thisGame.run()
    maybeInspectActor(defender)


