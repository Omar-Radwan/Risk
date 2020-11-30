from Agent import Agent
from Game import Game
from Map import Map

# code that attaches map to a game and starts the game
redPlayer = Agent()
greenPlayer = Agent()
map = Map(filename="map1.txt")
print(map.__str__())
game = Game(map, False, redPlayer, greenPlayer)
game.prepare()
# print(game)
# print(greenPlayer)


