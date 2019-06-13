
from bisect import insort

class PriorityQueue(list):

    def __init__(self, iterable=None):
        list.__init__(self, iterable)
        list.sort(self)

    def add(self, item):
        insort(self, item)

    def top(self):
        if list.__len__(self) > 0:
            return list.__getitem__(self, -1)

    def __hash__(self):
        return id(self)