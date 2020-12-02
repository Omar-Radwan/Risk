from Map import Map

class AStarAgent:
    def __init__(self,map):
        self.cityList = []
        self.map=map

    def calculateBonusArmy(self):
        return max(3,len(self.cityList)/3)

    #assume I have neighbours of the city.
    def AStarHeuristicPickHighestAdjacentCity(self):
        for city in self.cityList:
            for neighbourId in self.map.graph[city.id]:
                neighbour=self.map.cityList[neighbourId]
                if(city.armyCount>neighbour.armyCount+1 and city.isRedArmy!=neighbour.isRedArmy):
                    print("city id : ",city.id," with ",city.armyCount," armies",
                          " and red color is ",city.isRedArmy,"can attack ","neighbour id : ",
                          neighbour.id," with armies ",neighbour.armyCount," armies"," and red color is : ",
                          neighbour.isRedArmy)


