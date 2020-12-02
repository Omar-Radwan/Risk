from Game import Game


class Agent:
    def __init__(self,game: Game):
        self.cityList = []
        self.game = game

    def applyHeuristic(self, game: Game, bonusPlayers: int):
        pass

    def attachCity(self, city):
        self.cityList.append(city)

    # TODO: double check that this function is working correctly
    def removeCity(self, city):
        self.cityList.remove(city)

    # TODO: get rid of loop in this function
    def countArmy(self) -> int:
        sum = 0
        for city_id in self.cityList:
            sum += self.game.cityList[id].armyCount
        return sum

    # debugging function
    def __str__(self):
        s = ""
        for city in self.cityList:
            s += city.__str__() + '\n'
        return s
