
from functools import partial


class Node:

    def __init__(self, value, graph):
        self.value = value
        self._graph = graph

    def __getattr__(self, function):
        fptr = self._graph.__getattribute__(function)
        return partial(fptr, self.value)

