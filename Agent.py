class Agent:
    def __init__(self):
        self.cityList = []

    def applyHeuristic(self, map):
        pass
    
    def attachCity(self, city):
        self.cityList.append(city)

    #TODO: double check that this function is working correctly
    def removeCity(self, city):
        self.cityList.remove(city)

    # debugging function
    def __str__(self):
        s = ""
        for city in self.cityList:
            s += city.__str__() + '\n'
        return s
