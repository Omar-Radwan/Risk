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

    def __str__(self) -> str:
        return f'city_id={self.cityId}, soldiers={self.soldiers}'


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

    def __str__(self) -> str:
        return f'city_id={self.fromId}, soldiers={self.attackers}'


class ActionManager:
    def __init__(self, game: Game):
        self.game = game
        self.stack = []

    def applyAction(self, action: Action):
        """
        takes action applies it and stores it in the stack to be able to roll it back later
        :param action: move in the game either bonus army placement or attack move
        :return:
        """
        self.stack.append(action)
        action.apply(self.game)

    def rollBackAction(self):
        """
        rollback the last action and removes it from the stack -if it exists-
        :return:
        """
        if (len(self.stack) == 0):
            return
        action = self.stack.pop()
        action.rollBack(self.game)

    def rollBackTwoActions(self):
        """
        rollback the last two actions and removes them from the stack -if they exist-
        :return:
        """
        if (len(self.stack) < 2):
            return
        self.rollBackAction()
        self.rollBackAction()

    # def adjacentActions1(self, isRedPlayer: bool) -> [(Action, [Action])]:
    #     """
    #     assumptions:
    #         1. bonus soldiers are added to one city only
    #         2. attack city y from city x with y.armyCount+1 (with least number of soldiers able to conquer y)
    #     :param isRedPlayer: true if the current player is red player and false is green player
    #     :return: list of tuples where each tuple contains (bonusArmyAction, list of attack actions)
    #     """
    #     myCitiesIds = self.game.citiesOf(isRedPlayer)
    #     bonusSoldiers = self.game.bonusSoldiers(isRedPlayer)
    #     result = []
    #     # O((myCities^2) * adjacentCities)
    #     for bonusArmyCityId in myCitiesIds:  # O(cities)
    #         bonusSoldiersAction = BonusSoldiersAction(isRedPlayer, bonusArmyCityId, bonusSoldiers)
    #         self.applyAction(bonusSoldiersAction)
    #         result.append((bonusSoldiersAction, []))
    #         for fromCityId in myCitiesIds:  # O(cities)
    #             for toCityId in self.game.map.graph[fromCityId]:  # O(adjacent)
    #                 if (self.game.cityList[fromCityId].isRedArmy != self.game.cityList[toCityId].isRedArmy
    #                         and self.game.cityList[fromCityId].armyCount > self.game.cityList[toCityId].armyCount + 1):
    #                     attackAction = AttackAction(isRedPlayer, fromCityId, toCityId,
    #                                                 self.game.cityList[toCityId].armyCount + 1)
    #                     result[-1][1].append(attackAction)
    #         self.rollBackAction()
    #     return result
    #
    # def adjacentActions2(self, isRedPlayer: bool) -> [(Action, [Action])]:
    #     """
    #     assumptions:
    #         1. bonus soldiers are added to one city only
    #         2. attack city y from city x with [y.armyCount+1 ... x.armyCount-1]
    #     :param isRedPlayer: true if the current player is red player and false is green player
    #     :return: list of tuples where each tuple contains (bonusArmyAction, list of attack actions)
    #     """
    #     myCitiesIds = self.game.citiesOf(isRedPlayer)
    #     bonusSoldiers = self.game.bonusSoldiers(isRedPlayer)
    #     result = []
    #     # O((myCities^2) * adjacentCities)
    #     for bonusArmyCityId in myCitiesIds:  # O(cities)
    #         bonusSoldiersAction = BonusSoldiersAction(isRedPlayer, bonusArmyCityId, bonusSoldiers)
    #         self.applyAction(bonusSoldiersAction)
    #         result.append((bonusSoldiersAction, []))
    #         for fromCityId in myCitiesIds:  # O(cities)
    #             for toCityId in self.game.map.graph[fromCityId]:  # O(adjacent)
    #                 if (self.game.cityList[fromCityId].isRedArmy != self.game.cityList[toCityId].isRedArmy
    #                         and self.game.cityList[fromCityId].armyCount > self.game.cityList[toCityId].armyCount + 1):
    #                     start, end = self.game.cityList[toCityId].armyCount + 1, self.game.cityList[
    #                         fromCityId].armyCount
    #                     step = max(int((end - start) / 3), 1)
    #                     for attackers in range(start, end, step):
    #                         attackAction = AttackAction(isRedPlayer, fromCityId, toCityId, attackers)
    #                         result[-1][1].append(attackAction)
    #         self.rollBackAction()
    #     return result

    def adjacentActions1(self, isRedPlayer: bool) -> [([Action], [Action])]:
        return self.__adjActions(isRedPlayer, self.__adj1)

    def adjacentActions2(self, isRedPlayer: bool) -> [([Action], [Action])]:
        return self.__adjActions(isRedPlayer, self.__adj2)

    def __adj1(self, isRedPlayer: bool, fromCityId: int, toCityId: int, container: [Action]):
        attackAction = AttackAction(isRedPlayer, fromCityId, toCityId,
                                    self.game.cityList[toCityId].armyCount + 1)
        container.append(attackAction)

    def __adj2(self, isRedPlayer: bool, fromCityId: int, toCityId: int, container: [Action]):
        start, end = self.game.cityList[toCityId].armyCount + 1, self.game.cityList[
            fromCityId].armyCount
        step = max(int((end - start) / 3), 1)
        for attackers in range(start, end, step):
            attackAction = AttackAction(isRedPlayer, fromCityId, toCityId, attackers)
            container.append(attackAction)

    def __onAttackPairs(self, isRedPlayer: bool, myCitiesIds: [], conatiner: [Action], adjFunc) -> [Action]:
        for myCityId in myCitiesIds:
            for adjCityId in self.game.map.graph[myCityId]:
                if self.game.canAttack(myCityId, adjCityId):
                    adjFunc(isRedPlayer, myCityId, adjCityId, conatiner)

    def __adjActions(self, isRedPlayer: bool, adjFunc) -> [([Action], [Action])]:
        myCitiesIds = self.game.citiesOf(isRedPlayer)
        bonusSoldiers = self.game.bonusSoldiers(isRedPlayer)
        result = []
        for bonusArmyCityId in myCitiesIds:
            bonusSoldiersAction = BonusSoldiersAction(isRedPlayer, bonusArmyCityId, bonusSoldiers)
            self.applyAction(bonusSoldiersAction)
            result.append(([bonusSoldiersAction], []))
            self.__onAttackPairs(isRedPlayer, myCitiesIds, result[-1][1], adjFunc)
            self.rollBackAction()
        return result

