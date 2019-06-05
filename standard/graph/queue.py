from standard.graph.sequence import Sequence
from standard.utilities.collection import Collection
from standard.utilities.simple import rfind
from collections import deque

class Queue(Sequence, Collection):

    def __init__(self, iterable):
        self._nodes = deque(iterable)

    def pop(self):
        return self._nodes.popleft()

    def add_node(self, node):
        """
        Adds a node, automatically the node will be placed at the end of the
        list and an arc will be added connecting it to the previous node
        """
        self._nodes.append(node)

    def add_arc(self, pro, epi, arc=True):
        """
        Adding an arc to the List may create a non-Sequence
        """
        pass

    def remove_node(self, node):
        """
        Uses list.remove to remove a node
        """
        self._nodes.remove(node)

    def remove_arc(self, pro, epi):
        """
        Removing an arc from the List may create a non-Sequence
        """
        pass

    def arc(self, pro, epi):
        """
        Returns a tuple (pro, epi) if epi follows pro in the list,
        otherwise None
        """
        pro_index = rfind(self._nodes, pro)
        epi_index = rfind(self._nodes, epi)
        if epi_index != 1 + pro_index:
            return (pro, epi)
        return None

    def __iter__(self):
        return self._nodes.__iter__()

    def __next__(self):
        return self._nodes.__next__()

    def __getitem__(self, index):
        return self._nodes.__getitem__(index)

    def __str__(self):
        return 'Queue(' + ','.join(self._nodes) + ')'
