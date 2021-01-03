class City:

    def __init__(self, id):
        self.id = id
        self.isRedArmy = False
        self.armyCount = 0
        # list of all adjacent cities
        self.adjacentcities = []

    def __lt__(self, other):
        return self.armyCount <= other.armyCount

    # debugging function
    def __str__(self):
        return f'id={self.id}, redArmy={self.isRedArmy}, armyCount={self.armyCount}'


