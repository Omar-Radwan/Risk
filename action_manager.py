from city import City
from game import Game
from heuristics import HeuristicsManager


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

    def __repr__(self):
        return self.__str__()


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
        self.heuristicsManager = HeuristicsManager()

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
        step = max(int((end - start) / 2), 1)
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

    def compareCity(self, x: City, y: City) -> bool:
        """
            given two cities x and y the function returns true if number of soldiers in x is less than number of soldiers in y
            if both cities have the same number of soldiers the function true if id of x is less than id of y
        """
        return x.armyCount < y.armyCount if x.armyCount != y.armyCount else x.id < y.id

    def minArmyCityId(self, citiesIds: []) -> int:
        """
            returns id of the city with min army count from list of cities
        """
        minArmyCityId = citiesIds[0]
        for cityId in citiesIds:
            if (self.compareCity(self.game.cityList[cityId], self.game.cityList[minArmyCityId])):
                minArmyCityId = cityId
        return minArmyCityId



    def applyListOfActions(self, actionList: [Action]):
        for action in actionList:
            self.applyAction(action)

    def rollBackNAction(self, numberOfActions: int):
        for i in range(numberOfActions):
            self.rollBackAction()

    def attackAdjacentActions(self, currentIsRed: bool, maxiIsRed):

        optimalBonusSoldiersActionList = self.optimalSoldiersPlacement(currentIsRed, maxiIsRed,
                                                                       self.heuristicsManager.defensiveAndAttacking)
        self.applyListOfActions(optimalBonusSoldiersActionList)

        attackActionList = []
        self.__onAttackPairs(currentIsRed, self.game.citiesOf(currentIsRed), attackActionList, self.__adj2)
        self.rollBackNAction(len(optimalBonusSoldiersActionList))

        return [(optimalBonusSoldiersActionList, attackActionList)]

    def optimalSoldiersPlacement(self, currentIsRed: bool, maxiIsRed: bool, heuristicFunction) -> [Action]:
        better = max
        NEUTRAL = int(-1e9)
        if (currentIsRed != maxiIsRed):
            better = min
            NEUTRAL = int(1e9)

        baseValue = heuristicFunction(maxiIsRed, self.game)
        myCitiesId = self.game.citiesOf(currentIsRed)
        bonusSoldiers = self.game.bonusSoldiers(currentIsRed)

        def moveValue(currentIsRed: bool, maxiIsRed: bool, cityId, soldiers):
            bonusSoldiers = BonusSoldiersAction(currentIsRed, cityId, soldiers)
            self.applyAction(bonusSoldiers)
            currentValue = heuristicFunction(maxiIsRed, self.game)
            value = currentValue - baseValue
            self.rollBackAction()
            return value

        n, m = len(myCitiesId), bonusSoldiers
        dp = [[NEUTRAL for i in range(m + 1)] for i in range(n + 1)]  # 1 based
        for i in range(0, n + 1):
            dp[i][0] = 0

        addedToEachCityIndex = [0 for i in range(n + 1)]  # 1 based
        for i in range(1, n + 1):
            for s in range(1, m + 1):
                dp[i][s] = dp[i - 1][s]
                for j in range(1, s + 1):
                    v = moveValue(currentIsRed, maxiIsRed, myCitiesId[i - 1], j)
                    dp[i][s] = better(dp[i][s], v + dp[i - 1][s - j])

        i, s = n, m
        while i > 0 and s > 0:
            if dp[i][s] == dp[i - 1][s]:
                i -= 1
            else:
                for j in range(1, s + 1):
                    v = moveValue(currentIsRed, maxiIsRed, myCitiesId[i - 1], j)
                    if dp[i][s] == v + dp[i - 1][s - j]:
                        addedToEachCityIndex[i] = j
                        i -= 1
                        s -= j
                        break
        actions = []

        for i in range(1, n + 1):
            if (addedToEachCityIndex[i] != 0):
                bonusSoldiersAction = BonusSoldiersAction(currentIsRed, myCitiesId[i - 1], addedToEachCityIndex[i])
                actions.append(bonusSoldiersAction)

        return actions
