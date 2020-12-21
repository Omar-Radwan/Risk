from game import Game


class Action:
    def __init__(self, isRedPlayer: bool):
        self.isRedPlayer = isRedPlayer

    def rollBack(self, game: Game):
        pass

    def apply(self, game: Game):
        pass


class BonusSoldiersAction(Action):
    def __init__(self, isRedPlayer: bool, cityId: int, soldiers: int):
        super().__init__(isRedPlayer)
        self.cityId = cityId
        self.soldiers = soldiers

    def rollBack(self, game: Game):
        game.addSoldiersToCity(self.cityId, -self.soldiers)

    def apply(self, game: Game):
        game.addSoldiersToCity(self.cityId, self.soldiers)


class AttackAction(Action):
    def __init__(self, isRedPlayer: bool, fromId: int, toId: int, attackers: int):
        super().__init__(isRedPlayer)
        self.isRedPlayer = isRedPlayer
        self.fromId = fromId
        self.toId = toId
        self.attackers = attackers

    def rollBack(self, game: Game):
        game.addSoldiersToCity(self.toId, -self.attackers)
        game.addSoldiersToCity(self.fromId, self.attackers)
        game.changeCityOwner(self.toId)
        game.addSoldiersToCity(self.toId, self.defenders)

    def apply(self, game: Game):
        self.defenders = game.cityList[self.toId].armyCount
        game.move(self.fromId, self.toId, self.attackers)


class ActionManager:
    def __init__(self, game: Game):
        self.game = game
        self.stack = []

    def applyAction(self, action: Action):
        self.stack.append(action)
        action.apply(self.game)

    def rollBackAction(self):
        if (len(self.stack) == 0):
            return
        action = self.stack.pop()
        action.rollBack()

    def rollBackTwoActions(self):
        if (len(self.stack) < 2):
            return
        self.rollBackAction()
        self.rollBackAction()

    """
        assumptions:
            1. bonus soldiers are added to one city only
            2. attack city y from city x with y.armyCount+1 (with least number of soldiers able to conquer y)
    """""

    def adjacentActions1(self, isRedPlayer: bool) -> []:
        myCitiesIds = self.myCities(self.game, isRedPlayer)
        bonusSoldiers = self.game.bonusSoldiers(isRedPlayer)
        result = []
        # O((myCities^2) * adjacentCities)
        for bonusArmyCityId in myCitiesIds:  # O(cities)
            bonusSoldiersAction = BonusSoldiersAction(isRedPlayer, bonusArmyCityId, bonusSoldiers)
            result.append((bonusSoldiersAction, []))
            for fromCityId in myCitiesIds:  # O(cities)
                for toCityId in self.game.map.graph[fromCityId]:  # O(adjacent)
                    if (self.game.cityList[fromCityId].isRedArmy != isRedPlayer
                            and self.game.cityList[fromCityId].armyCount > self.game.cityList[toCityId].armyCount + 1):
                        attackAction = AttackAction(isRedPlayer, fromCityId, toCityId,
                                                    self.game.cityList[toCityId].armyCount + 1)
                        result[len(result) - 1][1].append(attackAction)

        return result

    """
        assumptions:
            1. bonus soldiers are added to one city only
            2. attack city y from city x with [y.armyCount+1 ... x.armyCount-1]
    """

    def adjacentActions2(self, isRedPlayer: bool) -> []:
        myCitiesIds = self.myCities(self.game, isRedPlayer)
        bonusSoldiers = self.game.bonusSoldiers(isRedPlayer)
        result = []
        # O((myCities^2) * adjacentCities)
        for bonusArmyCityId in myCitiesIds:  # O(cities)
            bonusSoldiersAction = BonusSoldiersAction(isRedPlayer, bonusArmyCityId, bonusSoldiers)
            result.append((bonusSoldiersAction, []))
            for fromCityId in myCitiesIds:  # O(cities)
                for toCityId in self.game.map.graph[fromCityId]:  # O(adjacent)
                    if self.game.cityList[fromCityId].isRedArmy != isRedPlayer:
                        start, end = self.game.cityList[toCityId] + 1, self.game.cityList[fromCityId] - 1
                        for attackers in range(start, end, 1):
                            attackAction = AttackAction(isRedPlayer, fromCityId, toCityId, attackers)
                            result[len(result) - 1][1].append(attackAction)
        return result


    def myCities(self, game: Game, isRedPlayer: bool) -> []:
        result = []
        for city in game.cityList:
            if (city.isRedArmy == isRedPlayer):
                result.append(city.id)
        return result
