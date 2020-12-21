from agent import Agent
from agents.agressive_agent import AggressiveAgent
from game import Game
from map import Map
from passive_agent import PassiveAgent
from city import City
from a_star_agent import AStarAgent
from game_controller import GameController
from agents.realtime_agent import realtime_agent
# code that attaches map to a game and starts the game


# code that attaches map to a game and starts the game
from agents.greedy_agent import GreedyAgent

map = Map(filename="map1.txt")
print(map)
game = Game(map)
game.prepare()
redPlayer = Agent(game)
greenPlayer = Agent(game)
game.redPlayer = redPlayer
game.greenPlayer = greenPlayer
# for trial to debug A star agent.
cityOne = City(1)
cityTwo = City(2)
cityOne.armyCount = 10
cityTwo.armyCount = 5
aStarAgent = AStarAgent(map)
aStarAgent.cityList = [cityOne, cityTwo]
aStarAgent.AStarHeuristic(game)
# for trial to debug passive agent.
passiveAgent = PassiveAgent()
cityOne = City(1)
cityTwo = City(2)
cityOne.armyCount = 2
cityTwo.armyCount = 12
# passiveAgent.cityList=[cityOne,cityTwo]
# passiveAgent.passiveAgentHeuristic()
# print(game)
# print(greenPlayer)

game.cityList[1].isRedArmy = True
game.cityList[1].armyCount += 5
game.cityList[1].adjacentcities.append(3)
game.cityList[1].adjacentcities.append(6)
game.cityList[1].adjacentcities.append(7)
game.cityList[3].isRedArmy = False
game.cityList[3].armyCount = 5
game.cityList[6].isRedArmy = False
game.cityList[6].armyCount = 3
game.cityList[7].isRedArmy = False
game.cityList[7].armyCount = 8

# aggressiveAgent = AggressiveAgent(game,(255,0,0))
# aggressiveAgent.AggressiveAgentHeuristic()
greedyAgent = GreedyAgent(game, (255, 0, 0))
greedyAgent.GreedyMode()


#real time
print("lllllllllllll")
realtime= realtime_agent(True)
realtime.heuristic(map,game)

