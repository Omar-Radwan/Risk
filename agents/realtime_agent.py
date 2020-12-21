#from Game import Game
#from Map import Map
import copy


class realtime_agent():
    def __init__(self, isRedPlayer: bool):
        self.isRedPlayer = isRedPlayer

# it returns list of border cities
    def getBorderCities(self,Map,game):
        borderCities =[]
        for city in game.citiesOf(self.isRedPlayer):
            print(city)
            for i in Map.graph[city]:
                if game.cityList[city].isRedArmy and not game.cityList[i].isRedArmy and not borderCities.__contains__(city):
                    borderCities.append(game.cityList[city])
                elif not game.cityList[city].isRedArmy and game.cityList[i].isRedArmy and not borderCities.__contains__(city):
                    borderCities.append(game.cityList[city])
        for i in borderCities:
             print(i.id)
        return borderCities



    def possibleAttacks(self,map,game):
        listOfPossibleAttacks=[]
        borderCities=self.getBorderCities(map,game)
        for city in borderCities:
            for i in map.graph[city.id]:
                if city.isRedArmy and not game.cityList[i].isRedArmy and city.armyCount - 1 > game.cityList[i].armyCount:
                    listOfPossibleAttacks.append([city.id,game.cityList[i].id])
                elif not city.isRedArmy and game.cityList[i].isRedArmy and city.armyCount - 1 > game.cityList[i].armyCount:
                    listOfPossibleAttacks.append([city.id, game.cityList[i].id])

        for i in game.cityList:
            print(i)
        return listOfPossibleAttacks

    def heuristic(self,map,game):
        listOfPossibleAttacks=self.possibleAttacks(map,game)
        print(listOfPossibleAttacks)
        if listOfPossibleAttacks == None:
            print("if od possible attacks")
            return
        for i in listOfPossibleAttacks:
            print(self.simulateAttack(i[0],i[1],map,game))
            if self.simulateAttack(i[0],i[1],map,game) :
                self.attack(i[0],i[1],game)
                return "attack"

        return "no attack"



    def simulateAttack(self,attackerId,defenderId,map,game):
        copyGame=copy.deepcopy(game)
        #for i in copyGame.cityList:
           # print(i.id)
        movingArmy =  copyGame.cityList[defenderId].armyCount + 1
        print(movingArmy)
        #copyGame.cityList[attackerId].armyCount = copyGame.cityList[attackerId].armyCount - movingArmy
        #copyGame.cityList[defenderId].armyCount = movingArmy
        #copyGame.cityList[defenderId].isRedArmy=copyGame.cityList[attackerId].isRedArmy
        copyGame.move(attackerId,defenderId,movingArmy)
        for i in map.graph[attackerId]:
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
        for i in map.graph[defenderId]:
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

    def attack(self,attackerId,defenderId,game):
        movingArmy = game.cityList[defenderId].armyCount + 1
        #Game.cityList[attackerId].armyCount = Game.cityList[attackerId].armyCount - movingArmy
        #Game.cityList[defenderId].armyCount = movingArmy
        #Game.cityList[defenderId].isRedArmy = Game.cityList[attackerId].isRedArmy
        #self.cityList.append(Game.cityList[defenderId])
        game.move(attackerId,defenderId,movingArmy)

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


