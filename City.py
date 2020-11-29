class City:

    def __init__(self, id):
        self.id = id
        self.isRedArmy = False
        self.armyCount = 0

    #debugging function
    def __str__(self):
        return f'id={self.id}, redArmy={self.isRedArmy}, armyCount={self.armyCount}'
