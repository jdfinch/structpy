from collections import deque

class Queue(deque, object):

    def __init__(self, iterable=None):
        if iterable is not None:
            deque.__init__(self, iterable)
        else:
            deque.__init__(self)

    def pop(self):
        return deque.popleft(self)

    def top(self):
        if deque.__len__(self) > 0:
            return deque.__getitem__(self, 0)

    def add(self, item):
        return deque.append(self, item)

    def popleft(self):
        raise AttributeError()

    def appendleft(self):
        raise AttributeError()

    def __hash__(self):
        return id(self)