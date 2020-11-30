from City import City


class Map:
    #cityCount..graph..cityList

    def __init__(self, filename="map1.txt"):  # default loaded map is map1
        file = open(filename, 'r')
        lines = file.readlines()
        self.cityCount = len(lines)
        self.graph = [[] for i in range(self.cityCount + 1)]
        self.cityList = [City(i) for i in range(self.cityCount + 1)]
        self.__readGraph(lines)
        self.__str__()  # for debugging ... remove it later

    def __readGraph(self, lines):
        for currentLine in lines:
            ids = currentLine.strip().split(' ')
            u = int(ids[0])
            for i in range(1, len(ids)):
                v = int(ids[i])
                self.graph[u].append(v)

    # debugging functions
    def __str__(self):
        return f'graph:\n{self.list2dToStr(self.graph)} ' \
               f'cities:\n{self.list2dToStr(self.cityList)}'

    def list2dToStr(self, list2d):
        s = ""
        for i in range(1, self.cityCount + 1):
            s += f'{i}->{list2d[i].__str__()}\n'
        return s
