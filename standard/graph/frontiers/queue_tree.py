from standard.graph.bidictionary_tree import BidictionaryTree
from standard.graph.bidictionary_graph import BidictionaryGraph
from standard.collections import Queue
from standard.graph.frontiers import Frontier

def _one_and_many(one, many):
    yield one
    if many is not None:
        for e in many:
            yield e

class QueueTree(BidictionaryTree, Queue, Frontier):
    """
    A `Tree` data structure that can return nodes like a queue with `.pop`
    based on the order nodes are added
    """

    def __init__(self, root, iterable=None):
        BidictionaryGraph.__init__(self)
        self._root = root
        Queue.__init__(self, _one_and_many(root, iterable))
        for node in _one_and_many(root, iterable):
            BidictionaryTree.add_node(self, node)
        self._active = root

    def active(self):
        return self._active

    def pop(self):
        self._active = Queue.pop(self)
        return self._active

    def complete(self):
        return self.__len__() == 0

    def add(self, node, epi=None, arc=True):
        if epi is None:
            epi = node
            node = self._active
        BidictionaryTree.add(self, node, epi, arc)
        Queue.add(self, epi)



    
