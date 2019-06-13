from standard.graph.frontiers.searcher import Searcher
from standard.graph.bidictionary_tree import BidictionaryTree
from standard.collections.priority_queue import PriorityQueue
from standard.graph.array_sequence import ArraySequence

def PrioritySearchTree(BidictionaryTree, PriorityQueue, Searcher):

    def __init__(self, root, target, priority_function, aggregation_function):
        """
        `priority_function(pro, epi, arc)`

        `aggregation_function(p1, p1)`
        """
        self._target = target
        self._complete = False
        self._active = root
        self._priority_function = priority_function
        self._aggregation_function = aggregation_function
        BidictionaryTree.__init__(self, root)
        PriorityQueue.__init__(self, ((0, root),))

    def complete(self):
        return self._complete

    def priority(self, node):
        return self.arc(node, self.parent(node))

    def add(self, node, epi, arc):
        if epi not in self._nodes:
            BidictionaryTree.add_node(self, epi)
            BidictionaryTree.add_arc(self, node, epi, arc)
            priority = self.priority_function(node, epi, arc)
            priority = self.aggregation_function(self.priority(node), priority)
            PriorityQueue.add(self, (priority, epi))
            if epi is self._target:
                self._complete = True

    def pop(self):
        priority, node = PriorityQueue.pop(self)
        self._active = node
        return node

    def result(self):
        return self.path(self._target, ArraySequence)
