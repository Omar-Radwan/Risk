from agent import Agent
from city import City
from game import Game


class HumanAgent(Agent):

    def compareCity(self, x: City, y: City) -> bool:
        """
            given two cities x and y the function returns true if number of soldiers in x is less than number of soldiers in y
            if both cities have the same number of soldiers the function true if id of x is less than id of y
        """
        return x.armyCount < y.armyCount if x.armyCount != y.armyCount else x.id < y.id

    def minArmyCityId(self, game: Game, citiesIds: []) -> int:
        """
            returns id of the city with min army count from list of cities
        """
        minArmyCityId = citiesIds[0]
        for cityId in citiesIds:
            if (self.compareCity(game.cityList[cityId], game.cityList[minArmyCityId])):
                minArmyCityId = cityId
        return minArmyCityId

    def hisMinArmyCityToAttack(self, game: Game, myCitiesIds: []) -> ():
        """
        returns tuple(bestUId, bestVId), where:
           bestVId is the id of enemy city with least number of soldiers that can be attacked
           bestUId is the id of my city that can attack enemy city with id = bestVId
           if multiple (bestUId,bestVId) exist the one with minimum bestVId is returned
        """
        bestUId, bestVId, graph = -1, -1, game.map.graph
        for uId in myCitiesIds:
            uCity = game.cityList[uId]
            for vId in graph[uId]:
                vCity = game.cityList[vId]
                if uCity.isRedArmy != vCity.isRedArmy and uCity.armyCount > vCity.armyCount + 1:
                    if bestVId == -1:
                        bestUId, bestVId = uId, vId
                    elif (self.compareCity(game.cityList[vId], game.cityList[bestVId])):
                        bestUId, bestVId = uId, vId
        return (bestUId, bestVId)

    def applyHeuristic(self, game: Game) -> Game:
        """
            the actions taken are:
                1. place all bonus army in my city with minimum number of soldiers
                2. attack enemy city with minimum number of soldiers that can be attacked
        """
        myCities = game.citiesOf(self.isRedPlayer)
        myMinArmyCityId = self.minArmyCityId(game, myCities)
        game.placeBonusSoldiers(myMinArmyCityId, game.bonusSoldiers(self.isRedPlayer))
        bestUId, bestVId = self.hisMinArmyCityToAttack(game, myCities)
        if bestUId != -1 and bestVId != -1:
            game.move(bestUId, bestVId, game.cityList[bestVId].armyCount + 1)
        return game
