from standard.graph.pointer_tree import PointerTree
from standard.graph.pointer_graph import PointerGraph
from standard.graph.frontiers.queue import Queue

def _one_and_many(one, many):
    yield one
    for e in many:
        yield e

class QueueTree(PointerTree):
    """
    A `Tree` data structure that can return nodes like a queue with `.pop`
    based on the order nodes are added
    """

    def __init__(self, root, iterable=None):
        PointerGraph.__init__(self)
        self._root = root
        self._nodes[root] = set()
        self._queue = None
        if iterable is not None:
            self._queue = Queue(_one_and_many(root, iterable))
        else:
            self._queue = Queue((root,))
        self._active = root

    def queue(self):
        return self._queue

    def top(self):
        return self._queue.top()

    def pop(self):
        active = self._queue.pop()
        self._active = active
        return active

    def complete(self):
        return self._queue.complete()

    def add(self, node, epi=None, arc=None):
        if node not in self._nodes:
            self._nodes[node] = set()
        if epi is None:
            self._nodes[self._active].add(node)
            self._queue.add(node)
        else:
            self._nodes[node].add(epi)
            self._queue.add_node(epi)


    def add_node(self, node):
        self._queue.add_node(node)
        if node not in self._nodes:
            self._nodes[node] = set()
        self._nodes[self._active].add(node)


    
