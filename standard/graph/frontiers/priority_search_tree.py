from standard.graph.frontiers.searcher import Searcher
from standard.graph.bidictionary_tree import BidictionaryTree
from standard.collections.priority_queue import PriorityQueue
from standard.graph.array_sequence import ArraySequence

class PrioritySearchTree(BidictionaryTree, PriorityQueue, Searcher):

    def __init__(self, root, target, priority_function, aggregation_function):
        """
        `priority_function(pro, epi, arc)`

        `aggregation_function(p1, p2)`
        """
        self._target = target
        self._complete = False
        self._active = root
        self._priority_function = priority_function
        self._aggregation_function = aggregation_function
        BidictionaryTree.__init__(self, root)

    def complete(self):
        return self._complete

    def priority(self, node):
        parent = self.parent(node)
        return self._priority_function(node, parent, self.arc(node, parent))

    def add(self, node, epi=None, arc=None):
        if epi is None:
            epi = node
            node = self._active
        priority = self._priority_function(node, epi, arc)
        priority = self._aggregation_function(self.priority(node), priority)
        PriorityQueue.add(self, (priority, epi))

    def pop(self):
        try:
            priority, node = PriorityQueue.pop(self)
            while node in self._nodes:
                priority, node = PriorityQueue.pop(self)
        except IndexError:
            return
        BidictionaryTree.add(self, self._active, node, priority)
        self._active = node
        if node is self._target:
            self._complete = True
        return node

    def result(self):
        return self.path(self._target, ArraySequence)
