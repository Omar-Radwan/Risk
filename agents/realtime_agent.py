#from Game import Game
#from Map import Map
import copy


class RtaAgent():
    def __init__(self, isRedPlayer: bool):
        self.isRedPlayer = isRedPlayer

    def calculateBonusArmy(self):
        return max(3,len(self.cityList)/3)



    def getBorderCities(self,Map,Game):
        borderCities =[]
        for city in self.cityList:
            for i in Map.graph[city.id]:
                if city.isRedArmy and not Game.cityList[i].isRedArmy and not borderCities.__contains__(city):
                    borderCities.append(city)
                elif not city.isRedArmy and Game.cityList[i].isRedArmy and not borderCities.__contains__(city):
                    borderCities.append(city)
        for i in borderCities:
             print(i.id)
        return borderCities



    def possibleAttacks(self,Map,Game):
        listOfPossibleAttacks=[]
        borderCities=self.getBorderCities(Map,Game)
        for city in borderCities:
            for i in Map.graph[city.id]:
                if city.isRedArmy and not Game.cityList[i].isRedArmy and city.armyCount - 1 > Game.cityList[i].armyCount:
                    listOfPossibleAttacks.append([city.id,Game.cityList[i].id])
                elif not city.isRedArmy and Game.cityList[i].isRedArmy and city.armyCount - 1 > Game.cityList[i].armyCount:
                    listOfPossibleAttacks.append([city.id, Game.cityList[i].id])

        for i in Game.cityList:
            print(i)
        return listOfPossibleAttacks

    def heuristic(self,Map,Game):
        listOfPossibleAttacks=self.possibleAttacks(Map,Game)
        print(listOfPossibleAttacks)
        if listOfPossibleAttacks == None:
            print("if od possible attacks")
            return
        for i in listOfPossibleAttacks:
            print(self.simulateAttack(i[0],i[1],Map,Game))
            if self.simulateAttack(i[0],i[1],Map,Game) :
                self.attack(i[0],i[1],Map,Game)
                return "attack"

        return "no attack"



    def simulateAttack(self,attackerId,defenderId,Map,Game):
        copyGame=copy.deepcopy(Game)
        #for i in copyGame.cityList:
           # print(i.id)
        movingArmy =  copyGame.cityList[defenderId].armyCount + 1
        print(movingArmy)
        copyGame.cityList[attackerId].armyCount = copyGame.cityList[attackerId].armyCount - movingArmy
        copyGame.cityList[defenderId].armyCount = movingArmy
        copyGame.cityList[defenderId].isRedArmy=copyGame.cityList[attackerId].isRedArmy
        for i in Map.graph[attackerId]:
            if copyGame.cityList[i].isRedArmy and not copyGame.cityList[attackerId].isRedArmy and copyGame.cityList[i].armyCount - 1 > copyGame.cityList[attackerId].armyCount:
                print("2wl if")
                print(i)
                print(copyGame.cityList[i].isRedArmy)
                print(copyGame.cityList[attackerId].isRedArmy)
                print(copyGame.cityList[i].armyCount - 1 )
                print(copyGame.cityList[attackerId].armyCount)

                return False
            elif not copyGame.cityList[i].isRedArmy and copyGame.cityList[attackerId].isRedArmy and copyGame.cityList[i].armyCount - 1 > copyGame.cityList[attackerId].armyCount:
                print("tany if")
                print(i)
                print(copyGame.cityList[i].isRedArmy)
                print(copyGame.cityList[attackerId].isRedArmy)
                print(copyGame.cityList[i].armyCount - 1)
                print(copyGame.cityList[attackerId].armyCount)
                return False
        for i in Map.graph[defenderId]:
            if copyGame.cityList[i].isRedArmy and not copyGame.cityList[defenderId].isRedArmy and copyGame.cityList[i].armyCount - 1 > copyGame.cityList[defenderId].armyCount:
                print("talt if")
                print(i)
                print(copyGame.cityList[i].isRedArmy)
                print(copyGame.cityList[attackerId].isRedArmy)
                print(copyGame.cityList[i].armyCount - 1)
                print(copyGame.cityList[attackerId].armyCount)
                return False
            elif not copyGame.cityList[i].isRedArmy and copyGame.cityList[defenderId].isRedArmy and copyGame.cityList[i].armyCount - 1 > copyGame.cityList[defenderId].armyCount:
                print("rabe3 if")
                print(i)
                print(copyGame.cityList[i].isRedArmy)
                print(copyGame.cityList[attackerId].isRedArmy)
                print(copyGame.cityList[i].armyCount - 1)
                print(copyGame.cityList[attackerId].armyCount)
                return False

        print("nehayt el heuristic")
        return True

    def attack(self,attackerId,defenderId,Map,Game):
        movingArmy = Game.cityList[defenderId].armyCount + 1
        Game.cityList[attackerId].armyCount = Game.cityList[attackerId].armyCount - movingArmy
        Game.cityList[defenderId].armyCount = movingArmy
        Game.cityList[defenderId].isRedArmy = Game.cityList[attackerId].isRedArmy
        self.cityList.append(Game.cityList[defenderId])


  #  def applyHeuristic(self, Map):
   #     chosenCity = None
    #    value = -50
     #   for city in self.cityList:
      #      print(f'\n hhhhhhhh +{ Map.graph[city.id] } + dfsdgs')
       #     for i in Map.graph[city.id]:
        #        neighbour=Map.cityList[i]
         #       if ((city.isRedArmy and not neighbour.isRedArmy) or (not city.isRedArmy and neighbour.isRedArmy)):
          #          print(f'gwa awl if + {city.isRedArmy} {city.id} {city.armyCount} {neighbour.isRedArmy}{neighbour.id}')
           #         print(f'{city.armyCount}')
            #        if ((city.armyCount - 1 > neighbour.armyCount) and (city.armyCount -1 - neighbour.armyCount > value)):
             #           print("tany if")
              #          chosenCity = neighbour
               #         value =city.armyCount -1 - neighbour.armyCount
                #        print(chosenCity.id)

      #  return chosenCity


