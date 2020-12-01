import copy


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
