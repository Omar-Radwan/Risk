from agent import Agent
from city import City
from game import Game


class NearlyPacifistAgent(Agent):

    def compareCity(self, x: City, y: City) -> bool:
        return x.armyCount < y.armyCount if x.armyCount != y.armyCount else x.id < y.id

    def myMinArmyCityId(self, game: Game, myCities: []) -> int:
        myMinCityId = myCities[0]
        for cityId in myCities:
            if (self.compareCity(game.cityList[cityId], game.cityList[myMinCityId])):
                myMinCityId = cityId
        return myMinCityId

    def hisMinArmyCityToAttack(self, game: Game, myCities: []) -> ():
        bestUId, bestVId, graph = -1, -1, game.map.graph
        for uId in myCities:
            uCity = game.cityList[uId]
            for vId in graph[uId]:
                vCity = game.cityList[vId]
                if uCity.armyCount > vCity.armyCount + 1:
                    if bestVId == -1:
                        bestUId, bestVId = uId, vId
                else:
                    if (self.compareCity(game.cityList[vId], game.cityList[bestVId])):
                        bestUId, bestVId = uId, vId
        return (bestUId, bestVId)

    def applyHeuristic(self, game: Game):
        myCities = game.citiesOf(self.isRedPlayer)
        myMinArmyCityId = self.myMinArmyCityId(game, myCities)
        game.addSoldiersToCity(myMinArmyCityId, game.bonusSoldiers(self.isRedPlayer))

        uId, vId = self.hisMinArmyCityToAttack(game, myCities)
        if uId != -1 and vId != -1:
            game.move(uId, vId, game.cityList[vId].armyCount + 1)

