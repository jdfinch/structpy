from standard.graph.frontiers.queue_tree import QueueTree
from standard.graph.frontiers.searcher import Searcher

class SearchTree(QueueTree, Searcher):
    """
    Search tree frontier that searches for a specific node `target`
    """

    def __init__(self, root, target):
        QueueTree.__init__(self, root)
        self._target = target
        self._complete = False

    def complete(self):
        return self._complete

    def result(self):
        """
        Returns the path of the tree that is the solution to the search, with
        the target node as the top of the returned `Sequence`
        """
        pass

    def add(self, node, epi=None, arc=None):
        if epi is None:
            epi = node
            node = self._active
        if epi is self._target:
            self._complete = True
        QueueTree.add(self, node, epi, arc)
        