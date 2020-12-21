import copy




def tupleTest():
    a = (1, 2)
    b = (0, 4)
    a = min(a, b)
    print(a)
    a = (b[0] + 1, b[1] + 2)
    print(a)

tupleTest()
# some empty class to test deepcopy function
class dummy:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y
        self.arr = [x, y]

    def __str__(self):
        return f'x = {self.x}, y = {self.y}, a={self.arr}'


# deep copy of object
def objectDeepCopy():
    original = dummy(10, 15)
    copied = copy.deepcopy(original)
    original.arr[0] = 120
    original.x = 12
    print(original)
    print(copied)


# deep copy some list
def listDeepCopy():
    original = [1, 2, 3, 4, 5]
    copied = copy.deepcopy(original)
    copied[0] = 123123
    print(original)
    print(copied)


objectDeepCopy()

""" hash of custom objects"""


class MyThing:
    def __init__(self, name, location, length):
        self.name = name
        self.location = location
        self.length = length

    def __hash__(self):
        return hash((self.name, self.location))

    def __eq__(self, other):
        return (self.name, self.location) == (other.name, other.location)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)
