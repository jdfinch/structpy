from standard.graph.tree import Tree
from standard.graph.frontiers.queue import Queue

class QueueTree(Tree):
    """
    A `Tree` data structure that can return nodes like a queue with `.pop`
    based on the order nodes are added
    """

    def __init__(self, root, iterable=None):
        Tree.__init__(self, root)
        self._queue = Queue(iterable)

    def queue(self):
        return self._queue

    def top(self):
        return self._queue.top()

    def pop(self):
        return self._queue.pop()

    def complete(self):
        return self._queue.complete()

    def add_node(self, node):
        pass

    
