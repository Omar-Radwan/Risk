from City import City
from helping_functions import list2dToStr


class Map:
    # cityCount..graph..cityList

    def __init__(self, filename="map1.txt"):  # default loaded map is map1
        file = open(filename, 'r')
        lines = file.readlines()
        self.cityCount = len(lines)
        self.graph = [[] for i in range(self.cityCount + 1)]
        self.__readGraph(lines)
        self.__str__()  # for debugging ... remove it later
        self.map = {"0": [683.0, 414.5],
               "1": (503.0, 414.5),
               "2": (333.0, 414.5),
               "3": (203.0, 414.5),
               "4": (133.0, 494.5),
               "5": (663.0, 534.5),
               "6": (333.0, 584.5),
               "7": (433.0, 584.5),
               "8": (663.0, 664.5),
               "9": (783.0, 554.5),
               "10": (188.0, 114.5),
               "11": (168.0, 219.5),
               "12": (428.0, 164.5),
               "13": (618.0, 249.5),
               "14": (293.0, 254.5),
               "15": (438.0, 299.5),
               "16": (618.0, 159.5),
               "17": (718.0, 214.5),
               "18": (653.0, 344.5),
               "19": (763.0, 319.5),
               "20": (828.0, 249.5),
               "21": (1043.0, 604.5),
               "22": (793.0, 439.5),
               "23": (858.0, 389.5),
               "24": (865.0, 604.5),
               "25": (788.0, 614.5),
               "26": (918.0, 369.5),
               "27": (983.0, 394.5),
               "28": (973.0, 469.5),
               "29": (943.0, 539.5),
               "30": (1088.0, 659.5),
               "31": (988.0, 344.5),
               "32": (1083.0, 299.5),
               "33": (1093.0, 524.5),
               "34": (1168.0, 434.5),
               "35": (1133.0, 364.5),
               "36": (1063.0, 364.5),
               "37": (1163.0, 189.5),
               "38": (923.0, 239.5),
               "39": (1213.0, 149.5)
               }

    def __readGraph(self, lines):
        for currentLine in lines:
            ids = currentLine.strip().split(' ')
            u = int(ids[0])
            for i in range(1, len(ids)):
                v = int(ids[i])
                self.graph[u].append(v)

    # debugging functions
    def __str__(self):
        return f'graph:\n{list2dToStr(self.graph)} '


