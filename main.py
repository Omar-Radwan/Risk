from Game import Game
from Map import Map

#code that attaches map to a game and starts the game
map = Map(filename="map1.txt")
game = Game(map,False)
game.prepare()
print(game.__str__())


