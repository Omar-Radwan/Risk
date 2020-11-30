from Agent import Agent
from AggressiveAgent import AggressiveAgent
from Game import Game
from Map import Map
from PassiveAgent import PassiveAgent
from City import City

# code that attaches map to a game and starts the game
redPlayer = Agent()
greenPlayer = Agent()
map = Map(filename="map1.txt")
print(map)
game = Game(map, False, redPlayer, greenPlayer)
game.prepare()
#for trial to debug passive agent.
passiveAgent=PassiveAgent()
cityOne=City(1)
cityTwo=City(2)
passiveAgent.cityList=[cityOne,cityTwo]
passiveAgent.passiveAgentHeuristic()
# print(game)
# print(greenPlayer)

aggressiveAgent = AggressiveAgent()
aggressiveAgent.cityList=[cityOne,cityTwo]
aggressiveAgent.AggressiveAgentHeuristic()


