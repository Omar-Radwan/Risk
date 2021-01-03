class Map:
    # cityCount..graph..cityList

    def __init__(self, filename):  # default loaded map is USmap
        filename = f'assets/{filename}'
        file = open(filename, 'r')
        lines = file.readlines()
        self.cityCount = len(lines)
        self.graph = [[] for i in range(self.cityCount)]
        self.__readGraph(lines)
        self.__str__()  # for debugging ... remove it later
        self.worldMap = {"0": [119, 118],
                    "1": (1203, 454),
                    "2": (164, 272),
                    "3": (238, 237),
                    "4": (242, 144),
                    "5": (423, 499),
                    "6": (364, 466),
                    "7": (622, 420),
                    "8": (803, 158),
                    "9": (906, 147),
                    "10": (1104, 109),
                    "11": (1231, 109),
                    "12": (1161, 244),
                    "13": (1044, 290),
                    "14": (896, 288),
                    "15": (476, 72),
                    "16": (712, 580),
                    "17": (719, 502),
                    "18": (724, 421),
                    "19": (839, 566),
                    "20": (1188, 540),
                    "21": (1289, 571),
                    "22": (805, 473),
                    "23": (314, 602),
                    "24": (1245, 314),
                    "25": (585, 171),
                    "26": (591, 99),
                    "27": (751, 201),
                    "28": (401, 183),
                    "29": (1071, 545),
                    "30": (567, 305),
                    "31": (945, 364),
                    "32": (417, 375),
                    "33": (1101, 690),
                    "34": (869, 686),
                    "35": (474, 683),
                    "36": (237, 356),
                    "37": (275, 298),
                    "38": (725, 91),
                    "39": (820, 379),
                    "40": (704, 266),
                    "41": (659, 220),
                    "42": (1087, 385),
                    "43": (1114, 449),
                    "44": (803, 310),
                    "45": (596, 251),
                    "46": (307, 424),
                    "47":(1043,228)
                         }
        self.USmap = {"0": [683.0, 414.5],
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
