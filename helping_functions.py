# functions that takes 2d list and returns a string containing the content of the 2d list in readable way
def list2dToStr(list2d):
    s = ""
    for i in range(1, len(list2d)):
        s += f'{i}->{list2d[i].__str__()}\n'
    return s
